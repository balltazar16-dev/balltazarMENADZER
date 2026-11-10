"""Offline YouTube pregled i deterministički Suno predlog; bez zavisnosti."""

import argparse
import json
import math
from pathlib import Path


def number(value, name, maximum=None, integer=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}: očekivan broj")
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name}: očekivan konačan nenegativan broj")
    if maximum is not None and value > maximum:
        raise ValueError(f"{name}: maksimum je {maximum}")
    if integer and not isinstance(value, int):
        raise ValueError(f"{name}: očekivan ceo broj")


def load_data(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("Ulaz mora biti JSON objekat")
    for key in ("channel", "period"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f"Nedostaje tekst: {key}")
    if not isinstance(data.get("demo"), bool):
        raise ValueError("demo mora biti true ili false")
    videos = data.get("videos")
    if not isinstance(videos, list) or not videos:
        raise ValueError("videos mora sadržati najmanje jedan video")
    for index, video in enumerate(videos, 1):
        if not isinstance(video, dict):
            raise ValueError(f"Video {index}: očekivan objekat")
        for key in ("title", "style"):
            if not isinstance(video.get(key), str) or not video[key].strip():
                raise ValueError(f"Video {index}: nedostaje {key}")
        number(video.get("views"), "views", integer=True)
        number(video.get("duration_seconds"), "duration_seconds")
        if video["duration_seconds"] == 0:
            raise ValueError("duration_seconds mora biti veći od nule")
        for key in ("impressions", "ctr_percent", "average_view_seconds"):
            if video.get(key) is not None:
                number(video[key], key, 100 if key == "ctr_percent" else None,
                       integer=key == "impressions")
    return data


def retention(video):
    seconds = video.get("average_view_seconds")
    return None if seconds is None else 100 * seconds / video["duration_seconds"]


def percent(value):
    return "nije uneto" if value is None else f"{value:.1f}%"


def clean(value):
    return " ".join(value.split()).replace("|", "\\|")


def render(data):
    videos = data["videos"]
    leader = max(videos, key=lambda video: video["views"])
    measured = [video for video in videos if retention(video) is not None]
    lines = [
        f"# {clean(data['channel'])} — pregled",
        f"Period: {clean(data['period'])}",
        "DEMO: svi brojevi su izmišljeni." if data["demo"] else
        "Izvor: ručni unos korisnika; podaci nisu nezavisno provereni.",
        "",
        "| Video | Stil | Pregledi | CTR | Prosečan odgledani deo |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for video in videos:
        lines.append(
            f"| {clean(video['title'])} | {clean(video['style'])} | "
            f"{video['views']} | {percent(video.get('ctr_percent'))} | "
            f"{percent(retention(video))} |"
        )
    lines += [
        "",
        f"Ukupno pregleda u unetom uzorku: {sum(v['views'] for v in videos)}.",
        f"Najviše pregleda: {clean(leader['title'])} ({leader['views']}).",
    ]
    if measured:
        best = max(measured, key=retention)
        lines.append(f"Najveći prosečan odgledani deo: {clean(best['title'])} "
                     f"({percent(retention(best))}).")
    lines += [
        "",
        "Ovo je opis uzorka, ne dokaz da određeni stil bolje prolazi. "
        "Kod izjednačenja prikazuje se prvi uneti video. "
        "Poredi isti period, sličnu starost objava i isti format (Shorts odvojeno).",
        "CTR se preuzima iz Studija, ne računa iz ukupnih pregleda. "
        "Prosečan odgledani deo = prosečno gledanje / trajanje × 100; "
        "to nije kriva zadržavanja i može preći 100% pri ponovljenom gledanju.",
        "",
        "## Test za sledeću objavu",
        "Uvedi prepoznatljiv vokalni ili instrumentalni hook u prvih 5 sekundi. "
        "Uporedi zadržavanje na 30. sekundi sa prethodnom sličnom objavom "
        "posle jednakog broja dana. Ručno proveri u Studiju; ovaj modul nema tu krivu.",
        "",
        "## Suno — početni kreativni predlog",
        "Naslov: Ostani dok grad spava",
        "Fiksni BALLTAZAR šablon, nije AI zaključak iz metrike. "
        "Prilagodi ga pre generisanja; Suno ne mora tačno pratiti sve instrukcije.",
        "",
        "### STYLE",
        "```text",
        "Dark trip-hop, alt R&B, 88 BPM, D minor. Serbian lyrics. "
        "Intimate low female contralto, deep male spoken responses, "
        "warm sub bass, sparse drums, felt piano, smoky analog pads. "
        "Vocal hook within 5 seconds, behind-the-beat phrasing, "
        "layered chorus harmonies, spacious intimate mix.",
        "```",
        "",
        "### LYRICS",
        "```text",
        "[Intro — low male whisper]",
        "Još si tu... dok grad spava.",
        "",
        "[Verse — intimate female vocal]",
        "Na tvom dlanu ostaje mi trag,",
        "iza stakla nestaje nam grad.",
        "Ne pitaj me kuda vodi mrak,",
        "tvoj me dodir vraća korak nazad.",
        "",
        "[Chorus — layered harmonies]",
        "Ostani dok grad spava,",
        "dok nas jutro ne prepozna.",
        "Neka noć nas zadržava,",
        "još mi koža tebe dozva.",
        "```",
    ]
    return "\n\n".join(lines[:3]) + "\n" + "\n".join(lines[3:]) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON sa metrikama")
    parser.add_argument("--output", type=Path, default=Path("reports/report.md"))
    args = parser.parse_args()
    try:
        report = render(load_data(args.input))
        if args.input.resolve() == args.output.resolve():
            raise ValueError("Ulaz i izlaz moraju biti različiti fajlovi")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    except (OSError, ValueError, TypeError, OverflowError) as error:
        parser.exit(1, f"Greška: {error}\n")
    print(f"Izveštaj: {args.output.resolve()}")


if __name__ == "__main__":
    main()
