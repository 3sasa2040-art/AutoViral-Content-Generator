# Productiehandleiding

## Eerste keer

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Drafts genereren

```bash
python -m app.production generate --niche technology --count 3
```

Dit downloadt geen creators' video’s en publiceert niets. Het maakt lokale drafts, scripts, thumbnails en een review queue.

## Review openen

Windows: dubbelklik `start_windows.bat`.

Of:

```bash
python -m app.approval_gui
```

Keur alleen inhoud goed die origineel, feitelijk en platformconform is.

## Accounts koppelen

Gebruik de browser-loginmodules. Log handmatig in op accounts die je bezit of mag beheren. Bewaar geen wachtwoorden in JSON of `.env`; Playwright-profielen bevatten gevoelige sessiegegevens en horen niet in Git.

```bash
python -m app.youtube_uploader login
python -m app.tiktok_uploader login
```

## Rapport bekijken

```bash
python -m app.production queue
python -m app.production report
```

De uploadmodules moeten per platform worden gecontroleerd voordat je ze inschakelt; selectors, CAPTCHAs, 2FA en platformvoorwaarden kunnen veranderen. Gebruik de officiële publicatiemogelijkheden wanneer beschikbaar en houd de reviewstap actief.
