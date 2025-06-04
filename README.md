# 2025-c-qgis-ski-slope-plugin
Skupina C (akademický rok 2024/2025)
členové skupiny: Tomáš Mlejnek, Jana Tomášková


# SCRIPT/MODEL
Model pro identifikaci vhodných míst pro stavbu sjezdovky

## Popis projektu
 Tento projekt slouží k nalezení vhodných lokalit pro výstavbu sjezdovky na základě digitálního modelu terénu a dalších prostorových omezení. Hlavním výstupem je vektorová vrstva, která označuje území vhodné pro stavbu sjezdovky dle definovaných kritérií.

## Vstupní data
> LiDAR data ve formátu **.laz**
> Vektorové vrstvy:
   - komunikace
   - železnice
   - vodní toky
   - chráněné území
   - budovy

## Popis modelu / skriptu
> zpracování LiDAR dat:
- Načtení **.laz** souboru
- Výpočet sklonu, následné vyselektování ploch se sklonem 15° - 45°
- vytvoření konvexního obalu kolem ploch za účelem sjednocení překrývajících se malých plošek
- vyselektování ploch s výměrou větší než 1500m^2 
- Výběr ploch s vhodným sklonem pro sjezdovku
> práce s vektorovými daty:
 - Načtení omezení z vektorových vrstev (komunikace, železnice, vodní toky, chráněné území a budovy)
- Vytvoření ochranných pásem kolem těchto objektů
- Odstranění nevhodných oblastí ze sklonové vrstvy
> výstup:
- vektorová vrstva vytipovaných ploch s vhodným sklonem pro výstavbu sjezdovky
- Vektorová vrstva s vhodnými lokalitami pro stavbu sjezdovky 

