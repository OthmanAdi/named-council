#!/usr/bin/env python3
"""Tally a council from its seat reports. Arithmetic only, no judgement.

Every seat report ends with one fenced block like this (see references/briefs.md):

    ```council
    seat: Tomás
    round: 1
    scores: real=6, physical=5, light=4, touch=5, keep_using=5
    position: B
    confidence: 70
    evidence: B
    counts: blocker=0, should-fix=2, nit=1
    findings: TM-01=fixed, TM-02=better, TM-03=unchanged
    changed_because: the dual-write plan does not exist
    ```

Only `seat` and `round` are required; use the lines the council type needs.
Usage:  python tally.py <council-folder> [--json] [--out tally.md]
The script reads every .md file under the folder, keeps the last council block
of each, and prints tables plus flags. It decides nothing: the lead reads the
flags, checks the evidence and writes the verdict.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import statistics
import sys

BLOCK = re.compile(r"```+\s*council\s*\r?\n(.*?)```", re.S | re.I)
STATUSES = ("fixed", "better", "unchanged", "worse")


def pairs(text: str) -> dict[str, str]:
    """'a=1, b = two' -> {'a': '1', 'b': 'two'}"""
    out: dict[str, str] = {}
    for part in re.split(r"[,;]", text):
        if "=" in part:
            key, value = part.split("=", 1)
            if key.strip():
                out[key.strip()] = value.strip()
    return out


def number(value: str) -> float | None:
    match = re.search(r"-?\d+(?:\.\d+)?", value or "")
    return float(match.group()) if match else None


def parse_file(path: pathlib.Path) -> dict | None:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    blocks = BLOCK.findall(text)
    if not blocks:
        return None
    fields: dict[str, str] = {}
    for line in blocks[-1].splitlines():
        line = line.split("#", 1)[0] if re.match(r"\s*#", line) else line
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip().lower().replace(" ", "_")] = value.strip()
    round_no = number(fields.get("round", ""))
    if round_no is None:
        hint = re.search(r"round[\s_-]?(\d)", str(path).lower())
        round_no = float(hint.group(1)) if hint else 1.0
    scores = {k.lower(): number(v) for k, v in pairs(fields.get("scores", "")).items()}
    return {
        "seat": fields.get("seat") or path.stem,
        "round": int(round_no),
        "file": str(path),
        "scores": {k: v for k, v in scores.items() if v is not None},
        "position": fields.get("position", ""),
        "confidence": number(fields.get("confidence", "")),
        "evidence": fields.get("evidence", "").upper()[:1],
        "counts": {k.lower(): int(number(v) or 0) for k, v in pairs(fields.get("counts", "")).items()},
        "findings": {k: v.lower() for k, v in pairs(fields.get("findings", "")).items()},
        "changed_because": fields.get("changed_because", ""),
    }


def fmt(value: float | None) -> str:
    if value is None:
        return "-"
    return str(int(value)) if float(value).is_integer() else f"{value:.1f}"


NOT_REPORTS = ("brief", "prompts", "plan", "verdict", "tally", "readme", "runlog")


def report_files(folder: pathlib.Path) -> list[pathlib.Path]:
    """Seat reports only. Briefs and prompt records quote the example block and must not count as seats."""
    files = [p for p in sorted(folder.rglob("*.md")) if not p.name.lower().startswith(NOT_REPORTS)]
    in_rounds = [p for p in files if any(re.fullmatch(r"round[\s_-]?\d+", part.lower()) for part in p.parts[len(folder.parts):-1])]
    return in_rounds or files


def build(folder: pathlib.Path) -> dict:
    reports = [r for r in (parse_file(p) for p in report_files(folder)) if r and "<" not in r["seat"]]
    rounds = sorted({r["round"] for r in reports})
    by: dict[str, dict[int, dict]] = {}
    for r in reports:
        by.setdefault(r["seat"], {})[r["round"]] = r
    flags: list[str] = []
    first, last = (rounds[0], rounds[-1]) if rounds else (1, 1)

    axes: list[str] = []
    for r in reports:
        for axis in r["scores"]:
            if axis not in axes:
                axes.append(axis)

    score_rows = []
    for seat, per in by.items():
        row = {"seat": seat, "axes": {}}
        for axis in axes:
            a = per.get(first, {}).get("scores", {}).get(axis)
            b = per.get(last, {}).get("scores", {}).get(axis) if last != first else None
            row["axes"][axis] = {"first": a, "last": b}
            if a is not None and b is not None and b < a:
                flags.append(f"{seat}: {axis} went down ({fmt(a)} to {fmt(b)}). Read that seat's reason before reporting progress.")
        score_rows.append(row)

    # With two rounds, compare medians only across seats that answered both,
    # otherwise a seat that did not return would shift the number on its own.
    medians = {}
    for axis in axes:
        col_first = [per[first]["scores"][axis] for per in by.values() if first in per and axis in per[first]["scores"]]
        both = [per for per in by.values() if first in per and last in per and axis in per[first]["scores"] and axis in per[last]["scores"]]
        paired = last != first and bool(both)
        medians[axis] = {
            "first": statistics.median([p[first]["scores"][axis] for p in both]) if paired else (statistics.median(col_first) if col_first else None),
            "last": statistics.median([p[last]["scores"][axis] for p in both]) if paired else None,
            "spread_first": (max(col_first) - min(col_first)) if len(col_first) > 1 else None,
        }
    spreads = [m["spread_first"] for m in medians.values() if m["spread_first"] is not None]
    if axes and spreads and len(by) >= 3 and max(spreads) <= 1:
        flags.append("Round 1 scores sit within one point on every axis. Agreement between seats on one model is weak evidence: check that the seats really did different jobs.")

    if last != first:
        missing = [seat for seat, per in by.items() if first in per and last not in per]
        if missing:
            flags.append("No round " + str(last) + " report from: " + ", ".join(missing) + ". Their round 1 scores are not comparable progress.")

    recheck = []
    for seat, per in by.items():
        found = per.get(last, {}).get("findings", {}) if last != first else {}
        if not found:
            continue
        tally = {s: 0 for s in STATUSES}
        other = []
        for fid, status in found.items():
            if status in tally:
                tally[status] += 1
            else:
                other.append(f"{fid}={status}")
        open_ids = [fid for fid, status in found.items() if status in ("unchanged", "worse")]
        recheck.append({"seat": seat, **tally, "still_open": open_ids, "unreadable": other})
        if tally["worse"]:
            flags.append(f"{seat}: {tally['worse']} finding(s) got worse after the fixes.")

    positions = {}
    for rnd in rounds:
        votes: dict[str, dict] = {}
        for seat, per in by.items():
            r = per.get(rnd)
            if r and r["position"]:
                v = votes.setdefault(r["position"], {"seats": [], "confidence": 0.0})
                v["seats"].append(seat)
                v["confidence"] += r["confidence"] or 0
        if votes:
            positions[rnd] = votes
    flips = []
    if last != first and first in positions:
        ranked = sorted(positions[first].items(), key=lambda kv: -len(kv[1]["seats"]))
        majority = ranked[0][0] if ranked else ""
        for seat, per in by.items():
            a = per.get(first, {}).get("position", "")
            b = per.get(last, {}).get("position", "")
            if a and b and a != b:
                reason = per[last].get("changed_because", "")
                has_reason = bool(reason) and reason.lower() not in ("none", "n/a", "-")
                flips.append({"seat": seat, "from": a, "to": b, "reason": reason, "toward_first_majority": b == majority, "has_reason": has_reason})
        bare = [f for f in flips if not f["has_reason"]]
        if bare:
            flags.append("Changed position without a stated new argument: " + ", ".join(f["seat"] for f in bare) + ". Treat these as following the room and weigh the round 1 positions instead.")
        if flips and all(f["toward_first_majority"] for f in flips) and len(flips) > 1:
            flags.append("Every change of position moved toward the round 1 majority. That pattern looks like conformity, so compare with the blind round 1 positions before trusting the final count.")
    if first in positions and len(positions[first]) == 1 and len(by) >= 3:
        flags.append("Round 1 positions are unanimous. Make sure the dissenting seat argued the best alternative at full strength before calling this settled.")

    counts: dict[str, int] = {}
    for per in by.values():
        r = per.get(last) or per.get(first) or {}
        for key, value in (r.get("counts") or {}).items():
            counts[key] = counts.get(key, 0) + value

    return {
        "folder": str(folder), "rounds": rounds, "seats": list(by), "axes": axes,
        "scores": score_rows, "medians": medians, "recheck": recheck,
        "positions": {str(k): v for k, v in positions.items()}, "flips": flips,
        "counts": counts, "flags": flags,
    }


def render(t: dict) -> str:
    out: list[str] = [f"# Council tally", "", f"Folder: {t['folder']}", f"Seats with a council block: {len(t['seats'])}. Rounds found: {', '.join(map(str, t['rounds'])) or 'none'}.", ""]
    if not t["seats"]:
        out.append("No report with a ```council block was found. Ask each seat to end its report with one (see references/briefs.md).")
        return "\n".join(out)
    two = len(t["rounds"]) > 1
    if t["axes"]:
        out += ["## Scores" + (" (first round, then last round)" if two else ""), "", "| Seat | " + " | ".join(t["axes"]) + " |", "|---|" + "---|" * len(t["axes"])]
        for row in t["scores"]:
            cells = []
            for axis in t["axes"]:
                a, b = row["axes"][axis]["first"], row["axes"][axis]["last"]
                if two and a is not None and b is not None:
                    delta = b - a
                    change = "=" if delta == 0 else (f"{delta:+.0f}" if float(delta).is_integer() else f"{delta:+.1f}")
                    cells.append(f"{fmt(a)} → {fmt(b)} ({change})")
                elif two and b is not None:
                    cells.append(f"- → {fmt(b)}")
                else:
                    cells.append(fmt(a))
            out.append(f"| {row['seat']} | " + " | ".join(cells) + " |")
        med = []
        for axis in t["axes"]:
            m = t["medians"][axis]
            med.append(f"{fmt(m['first'])} → {fmt(m['last'])}" if two and m["last"] is not None else fmt(m["first"]))
        out += ["| **median" + (", seats in both rounds" if two else "") + "** | " + " | ".join(med) + " |", ""]
    if t["recheck"]:
        out += ["## Re-check of round 1 findings", "", "| Seat | fixed | better | unchanged | worse | still open |", "|---|---|---|---|---|---|"]
        for r in t["recheck"]:
            out.append(f"| {r['seat']} | {r['fixed']} | {r['better']} | {r['unchanged']} | {r['worse']} | {', '.join(r['still_open']) or 'none'} |")
        out.append("")
    if t["positions"]:
        out += ["## Positions", ""]
        for rnd, votes in t["positions"].items():
            out.append(f"Round {rnd}:")
            for option, v in sorted(votes.items(), key=lambda kv: -len(kv[1]["seats"])):
                out.append(f"- {option}: {len(v['seats'])} seat(s), confidence sum {fmt(v['confidence'])} ({', '.join(v['seats'])})")
        for f in t["flips"]:
            out.append(f"- Changed: {f['seat']} from {f['from']} to {f['to']}. Reason given: {f['reason'] or 'none'}")
        out.append("")
    if t["counts"]:
        out += ["## Findings by severity (latest round)", "", ", ".join(f"{k}: {v}" for k, v in t["counts"].items()), ""]
    out += ["## Flags", ""]
    out += [f"- {flag}" for flag in t["flags"]] or ["- None raised by the arithmetic. This says nothing about whether the findings are true."]
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Tally council seat reports (scores, re-check status, positions).")
    parser.add_argument("folder", help="Council folder that holds the seat reports (searched recursively).")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    parser.add_argument("--out", help="Also write the Markdown tally to this file.")
    args = parser.parse_args()
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            reconfigure(encoding="utf-8")  # Windows consoles default to cp1252 and choke on names like Tomás
    folder = pathlib.Path(args.folder)
    if not folder.is_dir():
        print(f"Not a folder: {folder}", file=sys.stderr)
        return 2
    tally = build(folder)
    text = render(tally)
    if args.out:
        pathlib.Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(json.dumps(tally, ensure_ascii=False, indent=2) if args.json else text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
