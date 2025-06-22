# 2025-c-qgis-ski-slope-plugin

- **Název pluginu:**  Ski Slope Plugin
- **Skupina:** C (Tomáš Mlejnek, Jana Tomášková)
- **Licence:** GNU GPL 2.0
- **E-mail:** mlejntom@cvut.cz, tomasj15@cvut.cz
- Vytvořeno v rámci semestrálního projektu z předmětu 155 FGIS (akademický rok 2024/2025)

## Popis projektu
 Tento projekt slouží k nalezení vhodných lokalit pro výstavbu sjezdovky na základě digitálního modelu terénu a dalších prostorových omezení. Hlavním výstupem je vektorová vrstva, která označuje území vhodné pro stavbu sjezdovky dle definovaných kritérií.

# SCRIPT/MODEL
Model pro identifikaci vhodných míst pro stavbu sjezdovky


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


# PLUGIN

Název pluginu: Ski Slope plugin

## Aktivace pluginu

- V programu QGIS je nutné nastavit v Nastavené - Systém - Prostředí - nastavit cestu ke složce 2025-c-qgis-ski-slope-plugin (adresář se složkou s Ski_slope_plugin)
- Po nastavení této cesty je nutné restartovat QGIS
- Pro aktivaci pluginu je nutné obnovit plugin pomocí Plugin-Reloader
- Dialogové okno je možné znovu zobrazit v záložce Zobrazit - Panely - Ski Slope Plugin


## Popis pluginu

- Plugin implemetuje vytvořený model. Pro spuštění je nutné mít potřebná data viz. výše.
- Plugin se ovládá přes dialogové okno, kde se zvolí konkrétní vrstvy. Výpočet se spustí po kliknutí na tlačítko Start

> výstup:
- vektorová vrstva vytipovaných ploch s vhodným sklonem pro výstavbu sjezdovky
- Vektorová vrstva s vhodnými lokalitami pro stavbu sjezdovky 