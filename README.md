# 2025-c-qgis-ski-slope-plugin
Skupina C (akademický rok 2024/2025)


SCRIPT/MODEL

    Model pro identifikaci vhodných míst pro stavbu sjezdovky

    Popis projektu

    Tento projekt slouží k nalezení vhodných lokalit pro výstavbu sjezdovky na základě digitálního modelu terénu a dalších prostorových omezení. Hlavním výstupem je vektorová vrstva, která označuje území vhodné pro stavbu sjezdovky dle definovaných kritérií.

    Vstupní data

    - LiDAR data ve formátu `.laz` 
    - Vektorové vrstvy:
    - komunikace
    - železnice
    - vodní toky
    - chráněné území
    - budovy

    Popis modelu / skriptu

    1. pracování LiDAR dat:
   - Načtení `.laz` souboru
   - Výpočet sklonu
   - Výběr ploch s vhodným sklonem pro sjezdovku

    2. Práce s vektorovými daty:
   - Načtení omezení z vektorových vrstev (komunikace, železnice, vodní toky, chráněné území a budovy)
   - Vytvoření ochranných pásem kolem těchto objektů
   - Odstranění nevhodných oblastí ze sklonové vrstvy

    3. Výstup:
   - Vektorová vrstva s vyznačenými vhodnými lokalitami pro stavbu sjezdovky.

