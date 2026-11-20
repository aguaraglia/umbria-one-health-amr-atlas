# Ambito pubblico del Umbria One Health AMR Atlas

Edizione `umbria_amr_atlas`, pubblicata da Codex Vitae ETS. Il runtime carica soltanto le fonti `public_approved`.

La base pubblica comprende:

- confini ISTAT generalizzati al 1 gennaio 2026, letti in UTF-8: 92 comuni, 2 province (Perugia PG 054 e Terni TR 055) e la regione 10. I nomi con accento (Città di Castello, Città della Pieve) non sono ricodificati;
- sei indicatori AR-ISS 2024 (sangue e liquor), con numerosità, percentuale e intervallo di confidenza. Copertura 90,7%, rete regionale. Licenza CC BY 4.0. Nessun downscaling comunale;
- confezioni e spesa degli antibatterici J01 dagli Open Data AIFA 2024 (convenzionata e acquisti diretti, codreg 100), CC BY 4.0: consumo, non resistenza e non DDD;
- Rapporto ISTISAN 26/7, uso degli antibiotici nella Regione Umbria, dati 2024 (ISS, CC BY 4.0): Tabella 3 per i 12 distretti, Tabella 8 per USL e Tabella 29 per ospedale. I distretti non hanno un poligono ISTAT e non diventano un layer;
- due strutture nominate, georiferite con Nominatim il 20 novembre 2026 (ODbL 1.0, © OpenStreetMap contributors): AO di Perugia, Santa Maria della Misericordia, e AO Santa Maria di Terni. Per gli studi che citano genericamente l'ospedale universitario di Perugia il segnaposto è la sede di Santa Maria della Misericordia. L'Ospedale Veterinario Universitario di Perugia non ha un risultato Nominatim ed è mostrato sul poligono del comune di Perugia;
- 19 studi con collegamento territoriale esplicito (20 novembre 2026), nei sei layer di evidenza. 7 studi sono su una struttura, 1 su un comune, 1 su una provincia e 10 sulla regione. Il layer umano ha 2 elementi e 7 studi. Il veterinario ha 2 elementi e 6 studi. L'alimentare ha 1 elemento e 3 studi. L'ambientale non ha elementi. La fauna selvatica ha 2 elementi e 2 studi. Il contorno regionale raccoglie 1 studio umano. Un layer senza elementi è nessuna evidenza pubblicata, non resistenza zero. Il segnaposto indica dove è stato condotto lo studio, non una prevalenza.

Non sono pubblicati i materiali della Regione Umbria, dell'AO Santa Maria di Terni, dell'IZS dell'Umbria e delle Marche né il PDF OsMed: vedi `EXCLUDED_SOURCES.md`. Non ci sono record individuali, identificativi di paziente o campione, né coordinate di RSA, aziende agricole, canili, macelli o depuratori non nominati.
