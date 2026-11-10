# BALLTAZAR — AI Music Manager

Početni offline modul za pregled YouTube metrika i pripremu Suno STYLE/LYRICS
predloga. Python 3.10+, bez dodatnih biblioteka, API ključeva i plaćenih servisa.
Radi na Windowsu i Linuxu. Ne pristupa YouTube-u, Suno-u niti GitHub-u.

## Struktura

```text
balltazarMENADZER/
├── README.md
├── .gitignore
├── data/
│   └── example.json
└── src/
    └── manager.py
```

`data/` čuva ulazne podatke (input), `src/` kod, a `reports/` nastaje pri
pokretanju i čuva izlaz (output). Privatne podatke stavi u `data/private/`.
Izveštaji i privatni podaci isključeni su iz commita pomoću `.gitignore`.

## Pokretanje iz korena projekta

Windows:

```powershell
py -3 src/manager.py data/example.json
```

Linux:

```bash
python3 src/manager.py data/example.json
```

Otvori `reports/report.md`: tabela metrika, vodeći video po pregledima,
prosečan odgledani deo, jedan test i Suno predlog. Ponovno pokretanje
prepisuje isti izveštaj. Drugo odredište zadaj sa `--output reports/drugi.md`.

## Unos stvarnih podataka

Kopiraj `data/example.json` u `data/private/channel.json`, postavi `demo` na
`false` i zameni sve izmišljene brojeve. `period` neka sadrži tačan raspon
datuma; metrika svakog videa mora biti iz istog izabranog perioda.
Ne mešaj Shorts i duge video-snimke u jednom poređenju.

| Polje | Značenje |
| --- | --- |
| channel | Naziv kanala |
| period | Raspon datuma / opis uzorka |
| demo | true za demonstracione, false za sopstvene podatke |
| videos | Neprazna lista video-snimaka |
| title, style | Naslov i ručno unet muzički stil |
| views | Pregledi u periodu, nenegativan ceo broj |
| duration_seconds | Trajanje videa u sekundama, veće od nule |
| impressions | Prikazi thumbnaila iz Studija; ceo broj ili null |
| ctr_percent | CTR iz Studija, npr. 2.2 znači 2,2%; broj 0–100 ili null |
| average_view_seconds | Prosečno gledanje u sekundama; broj ili null |

Poslednja tri polja mogu se izostaviti. `null` znači nepoznato, a ne nulu.
CTR, impresije i prosečno gledanje uglavnom nisu javni: unesi ih iz
YouTube Studija ako ih imaš. Ne deli privatni JSON javno.

```powershell
py -3 src/manager.py data/private/channel.json
```

## Granice prve verzije

Analiza je opisna, bez automatskog preuzimanja i bez istorijskih poređenja.
Prosečan odgledani deo nije retention kriva. Različita starost objava,
publika i mali uzorak ograničavaju zaključke o stilovima.
Suno predlog je deterministički kreativni šablon: ne koristi jezički model,
ne menja se na osnovu metrike i ne troši Suno kredite. Kopiraj STYLE i LYRICS
ručno. Za sledeći korak: istorija nedeljnih snimaka podataka (snapshots),
zatim uvoz CSV-a i tek potom opciona API integracija.

## Prvi commit — ručno, kada kopiraš fajlove u svoj lokalni repo

```bash
git add README.md .gitignore data/example.json src/manager.py
git diff --cached
git commit -m "Add offline YouTube review and Suno starter"
```

Ovaj paket sam ne izvršava commit ili push. Nema izabrane licence;
pre preuzimanja tuđeg koda ili saradnje odredi odgovarajuću licencu.
