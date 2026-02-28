# Facebook Photo Scraper - Majas Delikatess

Selenium-baserad scraper som laddar ner alla foton, inlaggstexter och kommentarer fran en Facebook-sida.

## Forutsattningar

- Python 3.10+
- Google Chrome installerat
- Facebook-konto med tillgang till sidan

### Python-paket

```bash
pip install selenium webdriver-manager beautifulsoup4 requests
```

## Filer

| Fil | Beskrivning |
|-----|-------------|
| `majas_backup.py` | Huvudskriptet - kor detta |
| `cookies.json` | Sparade Facebook-cookies (fran Puppeteer/annan session) |
| `majas_delikatess_backup/` | Nedladdad data (bilder + info) |
| `majas_delikatess_facebook.zip` | ZIP med allt |

## Hur det fungerar

1. Startar Chrome via Selenium (headless-agtigt, med `--no-sandbox`)
2. Laddar Facebook-cookies fran `cookies.json` for att vara inloggad
3. For varje foto-ID:
   - Gar till `facebook.com/photo.php?fbid=<ID>`
   - Hamtar bilden fran DOM (`<img>` med `scontent`-URL)
   - Klickar "Visa inlagg" for att fa inlaggstexten
   - Hamtar kommentarer
   - Laddar ner bilden via `requests` med session-cookies
4. Kor i **batchar om 25 foton** med 10 min paus mellan (undviker FB-blockering)
5. Skapar en ZIP nar allt ar klart

## Anvandning

### Kor scrapern

```bash
cd F:\Majas_delikatess_AJ\Hemsida\scraper
python majas_backup.py
```

Skriptet hoppar automatiskt over redan nedladdade foton, sa det ar sakert att kora om.

### Output-struktur

```
majas_delikatess_backup/
  bilder/
    photo_918771860663533.jpg
    photo_918771853996867.jpg
    ...
  bildinfo/
    info_918771860663533.txt    <- inlaggstext + kommentarer
    info_918771853996867.txt
    ...
```

### Info-filformat

```
FOTO ID: 918771860663533
URL: https://www.facebook.com/photo.php?fbid=918771860663533&...
Alt-text: Kan vara en bild av ost och text...

INLAGGSTEXT:
Hej alla glada goda.
Har kommer en fantastisk ost fran...
Vi syns pa Maja's

KOMMENTARER (2 st):
  1. Anna Svensson
     Ser gott ut!
  2. Maja's Delikatess i Fritsla
     Tack Anna! Valkommen in och smaka.

Bild-URL: https://scontent-arn2-1.xx.fbcdn.net/v/...
```

## Foto-ID:n

Skriptet kraver en lista av Facebook foto-ID:n i `PHOTO_IDS`-variabeln. Dessa kan hamtas pa olika satt:

### Manuellt fran Facebook
1. Ga till Facebook-sidans fotoalbum
2. Oppna ett foto - URL:en innehaller `fbid=XXXXXXXX`
3. Det numret ar foto-ID:t

### Via Facebook Graph API (om du har tillgang)
```
GET /{page-id}/photos?fields=id&limit=500
```

### Via scrollning + DOM-extraktion
Oppna sidans fotoalbum, skrolla igenom alla, och kor i browserkonsolen:
```javascript
[...document.querySelectorAll('a[href*="/photo"]')]
  .map(a => a.href.match(/fbid=(\d+)/))
  .filter(Boolean)
  .map(m => m[1])
```

## Cookies

Skriptet anvander `cookies.json` for Facebook-inloggning. Om cookies gar ut:

1. Logga in pa Facebook i Chrome
2. Exportera cookies med ett tillsgg som "EditThisCookie" (JSON-format)
3. Spara som `cookies.json` i scraper-mappen

Minsta nodvandiga cookies: `c_user`, `xs`, `fr`, `datr`

## Batch-konfiguration

I toppen av `majas_backup.py`:

```python
BATCH_SIZE = 25              # Foton per batch
BATCH_PAUSE = 600            # Sekunder mellan batchar (10 min)
CONSECUTIVE_FAIL_LIMIT = 5   # Max fel i rad innan batch avbryts
```

- **Oka BATCH_PAUSE** om Facebook blockerar (t.ex. 1200 = 20 min)
- **Minska BATCH_SIZE** om det gar for fort (t.ex. 15)
- Skriptet pausar 3-7 sekunder mellan varje foto

## Felskning

| Problem | Losning |
|---------|---------|
| `SessionNotCreatedException` | Kolla att Chrome ar installerat och att ChromeDriver matchar versionen |
| Cookies fungerar inte | Exportera nya cookies fran Chrome |
| Facebook blockerar | Oka BATCH_PAUSE, minska BATCH_SIZE |
| Tomma info-filer | Session har gatt ut - starta om |
| `--no-sandbox` kravs | Normal pa Windows - behalls |
