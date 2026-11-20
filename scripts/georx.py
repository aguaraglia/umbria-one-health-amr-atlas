import re
GEO=re.compile(r"\bUmbria\w*|\bUmbrian\b|\bPerugia\b|Perugian|\bTerni\b|Ternana|\bFoligno\b|\bSpoleto\b|Citt[àa] di Castello|\bGubbio\b|\bAssisi\b|\bOrvieto\b|\bTodi\b|\bNarni\b|Trasimen\w*|Valnerina|\bNorcia\b|Gualdo Tadino|\bUmbertide\b|\bMarsciano\b|\bBastia Umbra\b|\bAmelia\b|\bCascia\b|Santa Maria della Misericordia|Santa Maria (Hospital|Hosp)|\bIZSUM\b|Umbria e (delle )?Marche|Umbria and Marche|Tiber valley|Upper Tiber|Alta Valle del Tevere|\bNera river|\bPiediluco\b|Colfiorito|Monte Subasio",re.I)
WILD=re.compile(r"central Italy|Apennin\w*|Sibillini|\bTiber\b",re.I)
AFF=re.compile(r"Perugia|Terni|Foligno|Spoleto|Umbria|Gubbio|Orvieto|Citt[àa] di Castello|Assisi",re.I)
