# SEO-standard avstamning - Maja's Delikatess

Datum: 2026-03-01
Projekt: `F:\Majas_delikatess_AJ\Hemsida`
Kalla: `F:\Standarder_AJ\SEO\seo-standard-playbook.md`

## Bedomning av aterkopplingen du fick
Den aterkopplingen stammer i stort. Den ar tekniskt rimlig och i linje med playbooken:
- Koddelarna ar i stor grad implementerade.
- Flera krav ar fortfarande "oppna" tills de ar verifierade i produktion och i verktyg.

## Statusoversikt (Del A) - uppdaterad och fortydligad

### A1) Crawl & index
- A1.1 HTTPS + en URL-version: **Delvis**.
  - Gjort: canonical mot `https://majasdelikatess.se/`.
  - Bevis: `src/pages/index.astro:81`.
  - Kvar: verifiera i prod att `http->https` och `www/non-www` ar 301 enligt vald canonical.
- A1.2 HTTP-statuskoder: **Ej verifierad i prod**.
  - Kvar: bekrafta 200 pa giltiga URL:er och riktig 404/410 pa ogiltiga URL:er.
- A1.3 robots.txt: **Klar i kod, ej verifierad i prod**.
  - Bevis: `src/pages/robots.txt.ts:1-17`.
- A1.4 Meta robots + X-Robots-Tag: **Delvis**.
  - Gjort: `meta name="robots"` pa sidan.
  - Bevis: `src/pages/index.astro:80`.
  - Kvar: X-Robots-Tag for filtyper/staging om behov.
- A1.5 XML sitemap: **Klar i kod, ej verifierad i prod**.
  - Bevis: `src/pages/sitemap.xml.ts:1-23`.
  - Kvar i prod: 200-status, korrekt content-type, endast kanoniska/indexerbara URL:er.
- A1.6 Canonical: **Klar for startsidan `/`, delvis for framtida sidstruktur**.
  - Bevis: `src/pages/index.astro:81`.
  - Kvar: per-sida canonical-rutin nar fler URL:er byggs.
- A1.7 Interna lankar crawlbara: **Klar**.
  - Bevis: `src/pages/index.astro:1676-1678`.
- A1.8 Mobile-first paritet: **Delvis**.
  - Kvar: live-verifiering via URL Inspection/Search Console.
- A1.9 JavaScript SEO: **Delvis**.
  - Kvar: live-renderingskontroll i prod.
- A1.10 Lazy loading / infinite scroll: **Delvis**.
  - Gjort: lazy loading finns.
  - Kvar: fortsatt QA i prod.
- A1.11 URL-borttagning: **Ej tillamplig just nu**.

### A2) URL-struktur & IA
- A2.1 Enkel URL-struktur: **Klar for nuvarande scope**.
- A2.2 Sidhierarki baseline: **Delvis**.
  - One-page finns; separata landningssidor for fler intent saknas.

### A3) On-page
- A3.1 Title: **Klar**.
- A3.2 Meta description: **Klar**.
- A3.2.1 Snippet-kontroller: **Delvis**.
- A3.3 Rubriker/semantik: **Delvis**.
- A3.4 Bilder (alt/lazy): **Delvis**.
- A3.5 Favicon och "site name": **Delvis (viktig forandring)**.
  - Favicon: klar.
  - Google site name: delvis. `og:site_name` ar bra for social delning men inte samma som Googles site name-funktion.
  - Forbattrat: `WebSite` schema har nu `name` + `alternateName`.
  - Bevis: `src/pages/index.astro` i `structuredData`.
  - Notering: Google kan fortfarande visa annat site name i SERP; verifieras efter indexering.
- A3.6 Utgaende lankar rel-attribut: **Delvis**.
- A3.7 Datum i SERP: **Ej tillamplig nu**.

### A4) Strukturerad data
- A4.1 Grundregler: **Delvis**.
- A4.2 Bas-schema foretagssajt: **Klar i kod**.
- A4.3 Validering: **Ej verifierad i verktyg**.

### A5) Video SEO
- **Ej tillamplig nu**.

### A6) Core Web Vitals
- A6.1 Good pa faltdata: **Ej verifierad**.

### A7) Search appearance / AI features
- **Processpunkter** (ej en engangs-kodfix).

### A8) Policy / spam
- **Ej verifierad i verktyg**.

### A9) Verktyg & drift
- A9.1 Search Console: **Ej klart** (utforande kvar).
- A9.2 Crawl budget: **Lag prioritet for liten sajt**.
- A9.3 Site moves: **Ej tillamplig nu**.

## Hreflang-status
- Nuvarande implementation: self-referencing `hreflang="sv-SE"` pa en svensksprakig sajt.
- Bedomning: tekniskt OK, men inte nodvandigt om ni inte har flera sprak/regionversioner.
- Rekommendation: behall self-reference eller ta bort; viktigast ar att undvika felaktiga flera hreflang-varianter.

## Staging / preview-skydd (saknades i tidigare rapport)
- Status: **Krav definierat, implementation kvar**.
- Rekommendation enligt playbook-princip:
  - Preview/staging ska inte indexeras (t.ex. auth, IP-begransning eller noindex/X-Robots).

## Exakt vad som ar gjort i kod
- Canonical + robots meta + OG + Twitter + hreflang.
  - `src/pages/index.astro:78-95`
- JSON-LD (`WebSite` + `GroceryStore`) inkl. `alternateName`.
  - `src/pages/index.astro` i `structuredData`
- Dynamisk robots.
  - `src/pages/robots.txt.ts:1-17`
- Dynamisk sitemap.
  - `src/pages/sitemap.xml.ts:1-23`
- Default-doman satt till `https://majasdelikatess.se`.
  - `src/pages/index.astro:11`
  - `src/pages/robots.txt.ts:1`
  - `src/pages/sitemap.xml.ts:1`

## QA-bevis (testbar checklista med pass/fail)
Kors mot live-doman efter deploy.

1. Redirect-policy
- Kommando:
```powershell
curl.exe -I http://majasdelikatess.se/
curl.exe -I https://www.majasdelikatess.se/
```
- Pass: slutlig URL ar `https://majasdelikatess.se/` med 301-kedja max 1 steg.

2. Statuskoder
- Kommando:
```powershell
curl.exe -I https://majasdelikatess.se/
curl.exe -I https://majasdelikatess.se/denna-finns-inte-12345
```
- Pass: startsida 200, ogiltig sida 404 (eller 410 om avsiktligt).

3. robots + sitemap
- Kommando:
```powershell
curl.exe -I https://majasdelikatess.se/robots.txt
curl.exe -I https://majasdelikatess.se/sitemap.xml
```
- Pass: 200 pa bada; robots innehaller sitemap-URL; sitemap har korrekt XML content-type.

4. Schema
- Verktyg: Rich Results Test + Schema Validator pa live-URL.
- Pass: inga kritiska fel i `WebSite`/`GroceryStore`.

5. GSC
- Steg: koppla egendom och skicka `https://majasdelikatess.se/sitemap.xml`.
- Pass: sitemap mottagen och URL:er borjar upptackas/indexeras.

6. CWV
- Verktyg: PageSpeed Insights + CrUX/GSC Core Web Vitals.
- Pass: inga kritiska regressionsvarningar; tydlig handlingslista om varningar finns.

7. Head-kontroll (canonical, hreflang, robots)
- Kommando:
```powershell
curl.exe -sL https://majasdelikatess.se/ | Select-String -Pattern "canonical|hreflang|meta name=""robots"""
```
- Pass: alla tre finns i slutlig HTML.

8. robots/sitemap innehall
- Kommando:
```powershell
curl.exe -s https://majasdelikatess.se/robots.txt
curl.exe -s https://majasdelikatess.se/sitemap.xml | Select-String -Pattern "<loc>"
```
- Pass: robots visar korrekt sitemap-URL, sitemap innehaller korrekt `<loc>`.

## Del B (research) - sak som fortfarande behovs
For full SEO-effekt enligt playbooken behovs fortsatt kund/research-del:
- intentkartlaggning per sida
- konkurrens i SERP
- beslut om fler landningssidor (inte bara one-page)
- lokal prioritering mellan Fritsla/Mark/Boras
