# Geografia pubblica

La cartografia pubblica dell'edizione Umbria comprende:

- `atlas_region.geojson`: confine regionale ISTAT 2026 (codice 10);
- `atlas_provinces.geojson`: 2 province ISTAT 2026: Perugia (PG 054) e Terni (TR 055);
- `atlas_municipalities.geojson`: 92 comuni ISTAT al 1/1/2026.

I file sono letti in UTF-8 dal DBF ISTAT.

Gli studi della letteratura curata stanno in layer distinti sotto `public/data/`. Le strutture nominate sono geocodificate tramite OSM Nominatim (vedi `raw/nominatim/NOTE.md`). Gli studi con città o province nominate usano i poligoni ISTAT corrispondenti; gli studi regionali usano il contorno regionale. Nessuna RSA, azienda agricola, canile, depuratore non nominato o struttura non nominata è localizzata. I distretti sanitari del Rapporto ISTISAN 26/7 non hanno un confine ISTAT: restano in tabella (`public/data/istisan_26_7_umbria_2024.json`) senza poligono.
