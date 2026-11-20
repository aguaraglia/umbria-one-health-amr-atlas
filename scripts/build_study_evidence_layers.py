#!/usr/bin/env python3
"""Build Umbria study evidence layers from the curated literature catalog.

Geometries come from the ISTAT 2026 boundaries of this edition or from named
facilities geocoded on OpenStreetMap Nominatim (1 req/s, 2026-11-20, raw
responses in raw/nominatim/). The geometry key of each included study is stored
in raw/curation/rows.json (geo_key). The script does not geocode farms, kennels,
shelters, unnamed wastewater plants or long-term care facilities and does not
invent a site the catalog does not name.
"""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = "Il segnaposto indica dove è stato condotto lo studio, non una prevalenza."
SECTOR = {"healthcare_amr": "AMR clinica", "human_antimicrobial_use": "Consumo di antimicrobici",
          "antimicrobial_stewardship": "Stewardship antimicrobica", "veterinary_amr": "AMR veterinaria",
          "companion_animal_amr": "AMR negli animali d'affezione", "environmental_amr": "AMR ambientale",
          "foodborne_amr": "AMR alimentare", "wildlife_amr": "AMR nella fauna selvatica"}
LAYER = {"healthcare_amr": "human", "human_antimicrobial_use": "human", "antimicrobial_stewardship": "human",
         "veterinary_amr": "veterinary", "companion_animal_amr": "veterinary", "environmental_amr": "environment",
         "foodborne_amr": "food", "wildlife_amr": "wildlife"}
# Strutture nominate geocodificate su Nominatim il 2026-11-20 (raw/nominatim/results_2026-11-20.json).
POINTS = {
    "smm": (12.3553973, 43.0792015, "AO di Perugia, Ospedale Santa Maria della Misericordia, Perugia",
            "Coordinate: OSM Nominatim, amenity=hospital 'Ospedale Santa Maria della Misericordia', Piazzale Giorgio Menghini 3, Perugia, 2026-11-20. Per gli studi che citano genericamente l'ospedale universitario di Perugia il segnaposto è questa sede."),
    "smt": (12.6562709, 42.5563226, "AO Santa Maria, Terni",
            "Coordinate: OSM Nominatim, amenity=hospital 'Azienda Ospedaliera Santa Maria', Via Vittorio Veneto, Terni, 2026-11-20."),
}

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def merge(geoms):
    if len(geoms) == 1:
        return geoms[0]
    polys = []
    for g in geoms:
        polys.extend([g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"])
    return {"type": "MultiPolygon", "coordinates": polys}

def main():
    catalog = load_json(ROOT / "public/data/literature-catalog.json")
    by_id = {r["id"]: r for r in catalog["records"]}
    rows = {f"pubmed_{r['pmid']}": r for r in load_json(ROOT / "raw/curation/rows.json") if r["decision"] == "include"}
    if set(rows) != set(by_id):
        raise SystemExit("Catalogo e righe incluse non coincidono")
    mun = {f["properties"]["name"]: f["geometry"] for f in load_json(ROOT / "public/geography/atlas_municipalities.geojson")["features"]}
    prov = {f["properties"]["name"]: f["geometry"] for f in load_json(ROOT / "public/geography/atlas_provinces.geojson")["features"]}
    region = load_json(ROOT / "public/geography/atlas_region.geojson")["features"][0]["geometry"]

    def organism(row):
        m = re.search(r"\(([^()]*)\)\s*$", row["place"])
        return m.group(1) if m else row["title"].rstrip(".")

    def card(sid):
        r = by_id[sid]; doi = r.get("doi") or ""
        return {"id": sid, "authors": r["authors"], "year": str(r["year"]), "title": r["title"].rstrip("."),
                "sector": SECTOR[r["scope"]], "organism": organism(rows[sid]),
                "doi": f"https://doi.org/{doi}" if doi else r["source_url"]}

    groups = {}
    for sid, row in rows.items():
        key = row["geo_key"]; layer = LAYER[by_id[sid]["scope"]]
        if key == "reg":
            layer = "regional" if layer == "human" else layer
        groups.setdefault((layer, key), []).append(sid)
    layers = {k: [] for k in ["human", "veterinary", "food", "environment", "wildlife", "regional"]}
    placed = set()
    for (layer, key), ids in sorted(groups.items()):
        ids.sort()
        kind, _, val = key.partition(":")
        if kind == "pt":
            lon, lat, label, basis = POINTS[val]
            geom = {"type": "Point", "coordinates": [round(lon, 6), round(lat, 6)]}; level = "struttura"; place = label
        elif kind == "com":
            names = val.split("|"); geom = merge([mun[n] for n in names]); level = "comune" if len(names) <= 2 else "area nominata"
            place = ", ".join(names); basis = "Poligono/i ISTAT 2026 del comune (o dei comuni) nominati nell'abstract o nel testo integrale."
        elif kind == "prov":
            names = val.split("|"); geom = merge([prov[n] for n in names]); level = "provincia"
            place = "Provincia di " + ", ".join(names) if len(names) == 1 else "Province di " + ", ".join(names)
            basis = "Poligono/i ISTAT 2026 delle province nominate o su cui ricade l'area nominata."
        elif kind == "reg":
            geom = region; level = "regione"; place = "Umbria"
            basis = "Studio su scala regionale (o luogo umbro non localizzabile oltre la regione). Il contorno regionale non è un punto di misura."
        else:
            raise SystemExit(f"geo_key sconosciuta: {key}")
        studies = [card(s) for s in ids]
        layers[layer].append({"type": "Feature", "geometry": geom, "properties": {
            "place": place, "geography_level": level, "geography_basis": basis,
            "study_count": len(studies), "study_ids": "; ".join(s["id"] for s in studies),
            "authors": " | ".join(s["authors"] for s in studies), "year": " | ".join(s["year"] for s in studies),
            "title": " | ".join(s["title"] for s in studies), "sector": " | ".join(s["sector"] for s in studies),
            "organism": " | ".join(s["organism"] for s in studies), "doi": " | ".join(s["doi"] for s in studies),
            "geography_note": NOTE}})
        placed.update(ids)
    if placed != set(by_id):
        raise SystemExit(f"Copertura incompleta: {sorted(set(by_id)-placed)}")
    names = {"human": "human_amr_evidence.geojson", "veterinary": "veterinary_amr_evidence.geojson",
             "food": "food_chain_amr_evidence.geojson", "environment": "environmental_amr_evidence.geojson",
             "wildlife": "wildlife_amr_evidence.geojson", "regional": "regional_study_outline.geojson"}
    for k, fn in names.items():
        (ROOT / "public/data" / fn).write_text(json.dumps({"type": "FeatureCollection", "features": layers[k]}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(fn, len(layers[k]), sum(f["properties"]["study_count"] for f in layers[k]))
    print("studi collocati:", len(placed))

if __name__ == "__main__":
    main()
