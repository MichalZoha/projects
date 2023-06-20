# Zadání

## Úvod

Naším častým úkolem je vytvářet datové [*pipeline*](https://dataengineering.wiki/Concepts/Data+Pipeline) pro zpracování a následnou analýzu dat. Na vstupu jsou často textové soubory, které pravidelně exportují různé interní systémy. Z těchto zdrojových souborů, uložených např. ve formátu [XML](https://en.wikipedia.org/wiki/XML) nebo [JSON](https://en.wikipedia.org/wiki/JSON), získáváme a ukládáme potřebné informace a zárověň tyto soubory dále archivujeme. Je zřejmé, že manuální zpracování je problematické, a proto chceme takové procesy zcela nebo částěčně automatizovat.  

Následující úloha by měla nastínit, s čím se budeme společně při naší spolupráci potýkat. Zkuste jednoduše vyřešit zadaný úkol a rozmyslete si, anebo rovnou  ukažte, jak byste takovou úlohu testovali.

## Úloha

Napište program s konzolovým rozhraním (*command-line interface*), který organizuje soubory podle uvedených požadavků. Dále proveťe jednoduchou analýzu dat.

### Úkol 1: příprava dat

Ze všeho nejdříve si vygenerujte testovací soubory pro zadanou úlohu pomocí [Python](https://www.python.org/) (verze 3.10+) skriptu [`prepare.py`](./prepare.py) umístěného v kořenovém adresáři projektu (repozitáře). Pokud jste v adresáři projektu, použijte následující postup pro Windows OS [^1].  

1. Vytvoř virtuální prostředí

   ```powershell
   py -3.10 -m venv .venv
   ```

2. Aktivuj virtuální prostředí

   ```powershell
    .\.venv\Scripts\activate
   ```

3. Aktualizujte `pip` a instaluje knihovny potřebné pro běh skriptu

   ```powershell
   python -m pip install --upgrade pip
   ```

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Spusťe skript a vygenerujte pracovní data

   ```powershell
   python prepare.py
   ```

Skript vytvoří v adresáři, ze kterého je volán, nový adresář  `source` [^2] s testovacími soubory ve formátu JSON. Očekávejte více než jeden dva tisíce souborů, kdy pro každý den od 1. ledna 2021 do aktuálního data vytvoří jeden až pět souborů.

[^1]: Postup jak pracovat s virtuálním protředím je popsán [zde](https://docs.python.org/3/library/venv.html).

[^2]: Pokud adresář `source` existuje, je vždy nejdříve smazán!

#### Příklad

```powershell
python prepare.py
Saving files...
2023-05-31_4.json saved: 2227it [00:04, 486.77it/s]
Saved 2227 files.
```

Název každého souboru obsahuje datum ve formátu `YYYY-MMM-DD` a pořadí v rámci jednoho dne tzn. čísla 1 až 5. Obsah každého souboru si můžete prohlédnout ve vašem programovém editoru nebo s ním pracovat na příkazové řádce např. pomocí programu [`jq`](https://jqlang.github.io/jq/).

```powershell
jq . .\source\2022-06-24_1.json
```

```json
{
  "count": 2,
  "date": "2022-06-24",
  "status": true,
  "text": "rabbit hits occasionally clueless"
}
```

Důležité jsou jen ukázané dva atributy `date` a `text`, ostatní můžete zcela ignorovat.

**Datum uvedené v názvu souboru by se mělo shodovat s obsahem v atributu `date`, nemusí tomu však být vždy!** Občas se stává v cca 10% případů, že se datum a název souboru neshodují. Potom musíme takový soubor dát stranou a později ručně zkontrolovat a případně soubory opravit.

A nyní již k důležitějším částem úlohy!

### Úkol 2: třídění dat

Vaším dalším úkolem je přemístit soubory ze zdrojového adresáře `source` do cílového adresáře `target`, ve kterém je uspořádáte podle roku a čísla týdne za pomoci JSON atributu `date`. Dále přejmenujte soubory tak, že odstraníte rok z názvu souboru např. z `2021-12-31_1.json` bude `12-31_1.json`.

- Program by měl na příkazové řádce přebírat následující dva argumenty:

  - `--input (-i)`: cesta k adresáři ze kterého chceme načítat soubory, např. `source`.
  
  - `--output (-o)`: cesta k adresáři do kterého chceme ukládat soubory, např. `target`.

  **Příklad**

  ```powershell
  program --input .\source --output \.target
  ```

  Pokud není argument zadán, zkontrolujte, jestli není nastavena proměnná prostředí (*environment variable*) s názvem `SOURCE_DIRECTORY` respektive `TARGET_DIRECTORY` a případně použijte jejich hodnotu. Jinak nastavte výchozí hodnotu na aktuální adresář, ze kterého je program volán.

- Program by měl po spuštění na začátku vypsat (*stderr*), kolik souborů bude zpracovávat.

  **Příklad**

  ```powershell
  program --input .\source --output \.target
  Processing 1234 files.
  ```

- Program by měl pro každý zpracovávaný soubor vypsat (*stdout*) JSON objekt s atributy obsahující cestu, odkud a kam se soubor přemisťuje.

  **Příklad**

  ```powershell
  program --input .\source --output \.target
  Processing 1234 files...
  {"source": "source/2021-01-01_1.json", "target":  "target/2021/W01/01-01_1.json" }
  ...
  ```

- Program by měl případnou chybu při přemístění souboru vypisovat (`stderr`), ale měl by pokračovat dále. Případně rozmyslete, co v takové situaci dělat.

- Program by měl po skončení vypsat (`stderr`) kolik celkem souborů přemístil.
  Pokud nezpracoval všechny soubory měl by vracet status kód různý od nuly (`1`).

  **Příklad**

  ```powershell
  program --input .\source --output \.target
  ...
  Success: processed 1034/1234 files.
  ```

  **Příklad**

  ```powershell
  program --input .\source --output \.target
  ...
  Failure: processed 1021/1234 files.
  ```

- Program by měl při zadání přepínače `--version (-v)` vypsat verzi programu.
  
  **Příklad**
  
  ```powershell
  program --version
  1.0.0
  ```

- Program by měl při zadání přepínače `--help (-h)` vypsat nápovědu.
  
- Program by měl ve výchozím stavu jen vypisovat, které změny udělá tzn. implementovat [*dry run*](https://en.wikipedia.org/wiki/Dry_run_(testing)). Pokud chceme změny opravdu provést, použijeme přepínač `--write (-w)`. Uživatele můžeme případně informovat o tom, v jakém módu program běží, při jeho startu.

  **Příklad**

  ```powershell
  program --input .\source --output \.target --write
  ```

#### Příklad

Příklad obsahu adresářů před a po běhu programu.

- Před spuštěním programu jsou data v adresáři `source`:

  ```powershell
  source/
    2021-01-01_1.json
    2021-01-01_2.json
    2021-01-01_3.json
    2021-01-01_4.json
    2021-01-01_5.json
    ...
    2023-05-27_1.json
    2023-05-27_2.json
    2023-05-28_1.json

  ```

- Po spuštění jsou data uložena podle let a týdnů v adresáři `target` a adresář `source` je prázdný:

  ```powershell
  target/
    2021/
      W01/
          01-01_1.json
          01-01_2.json
          01-01_3.json
          01-01_4.json
          01-01_5.json
          ...
      ...
    ...
    2023/
      ...
        W21/
          05-27_1.json
          05-27_2.json
          05-28_1.json
          ...
        ...
    ...
  ```

#### Poznámky

Pokud správně používáte `stderr` a `stdout`, mělo by být možně přesměřovat výstup programu do vstupu dalšího programu nebo souboru a při tom stále vidíme informativní výstupy v konzoli.

**Příklad**

```powershell
program --input .\source --output \.target --write > output.txt
Success: processed 1234/1234 files.
```

Důležité je si uvědomit, že adresář `target` již může obsahovat data, a tedy i podadresáře pro příslušné roky a týdny z předchozího běhu progamu. Adresáře pro týdny pojmenujte jako `W01` až `W52` (`W53`).

Adresáře pojmenované jako `source` a `target` jsou jen příklady. Vstupní i výstupní adresáře se mohou jmenovat libovolně.

Zkuste rozmyslet a případně ošetřit možné problémy:

- Obsah souboru nemusí být validní JSON.
- Formát data v názvu nebo obsahu souboru není validní.
- Datum v názvu souboru se liší od toho uvedeného v obsahu souboru.
- Soubory se nepodaří přesunout do cílového adresáře, např. nemáme oprávnění, soubor je zamknutý jiným procesem atd.

## Úkol 3: zpracování dat

- Pomocí grafu porovnejte počty příspěvků v jednotlivých týdnech každého roku i mezi roky vzájemně.
- Pomocí grafu porovnejte průměrnou délku textu (atribut `text`) příspěvků v jednotlivých týdnech každého roku i mezi roky vzájemně.

Tuto část  můžete lehce modifikovat podle vašeho úvážení a charakteru dat.
Data může zpracovat v libovolné technologii např. Excel, Pandas, R atd.
