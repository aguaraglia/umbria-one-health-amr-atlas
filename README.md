# Umbria One Health AMR Atlas

Edizione regionale `umbria_amr_atlas`, pubblicata da Codex Vitae ETS sulla stessa
base delle edizioni Toscana e Piemonte.

## Stato

La letteratura pubblicata con collegamento territoriale esplicito all'Umbria
è concentrata su Perugia (AO Santa Maria della Misericordia) e su Terni
(AO Santa Maria). Ne restano 19 inclusi (20 novembre 2026): 10 a scala
regionale, 7 di struttura, 1 sul comune di Perugia e 1 sulla provincia di
Perugia.

Due strutture nominate, georiferite con Nominatim (© OpenStreetMap
contributors, ODbL):

- AO di Perugia, Ospedale Santa Maria della Misericordia: 4 studi;
- AO Santa Maria di Terni: 3 studi.

Per gli studi che citano genericamente l'ospedale universitario di Perugia il
segnaposto è la sede di Santa Maria della Misericordia. L'Ospedale Veterinario
Universitario di Perugia non ha un risultato Nominatim ed è mostrato sul
poligono del comune di Perugia. Uno studio che tocca una provincia conta in
quella provincia: Perugia 6, Terni 3.

L'edizione pubblica AR-ISS 2024 (copertura 90,7%, rete regionale, CC BY 4.0),
AIFA Open Data 2024, antibatterici J01 (CC BY 4.0) e il Rapporto ISTISAN 26/7
sull'uso degli antibiotici in Umbria nel 2024 (ISS, CC BY 4.0). I 12 distretti
del rapporto non hanno un confine ISTAT: restano in tabella, senza poligoni,
con l'attribuzione del rapporto.

Sei layer (AMR umana, veterinaria, alimentare, ambientale, fauna selvatica,
contorno regionale):

- AMR umana: 2 elementi, 7 studi (AO Perugia e AO Terni);
- AMR veterinaria: 2 elementi, 6 studi (regione; provincia di Perugia);
- AMR alimentare: 1 elemento (regione), 3 studi;
- AMR ambientale: nessun elemento;
- AMR nella fauna selvatica: 2 elementi, 2 studi (comune di Perugia; regione);
- studi a scala regionale: 1 elemento, 1 studio umano.

I layer vuoti e le aree senza segnaposto sono nessuna evidenza pubblicata,
non resistenza zero. Ogni popup cita lo studio e il DOI (o il record PubMed
se il DOI non è assegnato) e ricorda che il segnaposto è il luogo dello
studio, non una prevalenza.

Confini ISTAT 2026 (92 comuni, 2 province, regione 10), letti in UTF-8.
Regione Umbria, AO Terni, IZSUM e il PDF OsMed sono esclusi: vedi
`metadata/EXCLUDED_SOURCES.md`.

Il conteggio in homepage e in pubblicazioni legge
`public/data/literature-catalog.json` (19).

## Pagine

Sorgente su `main`. Il sito statico è pubblicato dal branch `gh-pages`
(GitHub Pages, cartella `/`). Nessun file `CNAME`. Analitica: GoatCounter
`https://atlanteamr.goatcounter.com/count`, come le edizioni Toscana e
Piemonte.

## Build locale

```bash
python3 -m http.server 8000
```

Aprire `http://localhost:8000/`.

Per rigenerare i dati pubblici servono gli input in `raw/` e, per i confini,
l'archivio ISTAT indicato in `metadata/SNAPSHOTS.tsv`. I DBF ISTAT si leggono
in UTF-8:

```bash
pip install -r requirements-geodata.txt
python3 scripts/build_istat_geography.py --source-root <Limiti01012026_g> --output-root public/geography
python3 scripts/build_literature_catalog.py
python3 scripts/build_study_evidence_layers.py
```

## Directory

- `public/`: dati e asset approvati per il sito;
- `metadata/`: fonti, snapshot, ambito pubblico e fonti escluse;
- `raw/`: curatela, esummary e risposte Nominatim;
- `scripts/`: ricostruzione del catalogo e dei layer;
- `private/`: nessun dato riservato in questa edizione.
