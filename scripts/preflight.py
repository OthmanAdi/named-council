#!/usr/bin/env python3
"""Council preflight: report what this machine can give a council.

Read-only by default. It starts nothing, stops nothing, installs nothing and
never touches a running process. With --init it creates the empty council
folder layout and nothing else.

Usage:
  python preflight.py [--project PATH] [--url URL ...] [--council-dir PATH]
                      [--skills a,b,c] [--init] [--json]

What it cannot see: the lead's own tools. Whether you can start subagents,
pick a model per seat or drive a browser is visible only in your tool list,
so the report ends with the questions you answer yourself.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

HOME = pathlib.Path.home()
SKILL_ROOTS = [HOME / ".agents" / "skills", HOME / ".codex" / "skills", HOME / ".claude" / "skills"]


def run(cmd: list[str], cwd: str | None = None, timeout: int = 10) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
        return p.returncode, (p.stdout or p.stderr or "").strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, str(exc)


def find_playwright(project: pathlib.Path | None) -> dict:
    found = {}
    start = project or pathlib.Path.cwd()
    for folder in [start, *list(start.parents)[:3]]:
        for name in ("playwright", "playwright-core", "@playwright/test"):
            manifest = folder / "node_modules" / name / "package.json"
            if manifest.is_file() and name not in found:
                try:
                    version = json.loads(manifest.read_text(encoding="utf-8")).get("version", "?")
                except (OSError, ValueError):
                    version = "?"
                found[name] = {"version": version, "require_from": str(folder / "node_modules")}
    env = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    candidates = [pathlib.Path(env)] if env else []
    local = os.environ.get("LOCALAPPDATA")
    if local:
        candidates.append(pathlib.Path(local) / "ms-playwright")
    candidates += [HOME / ".cache" / "ms-playwright", HOME / "Library" / "Caches" / "ms-playwright"]
    if project:
        candidates += [project / "private" / "tools" / "ms-playwright", project.parent / "private" / "tools" / "ms-playwright"]
    browsers = []
    for c in candidates:
        if c.is_dir():
            names = sorted(p.name for p in c.iterdir() if p.is_dir() and p.name.split("-")[0].split("_")[0] in ("chromium", "firefox", "webkit"))
            if names:
                browsers.append({"path": str(c), "installed": names[:8]})
    return {"packages": found, "browser_folders": browsers}


def check_url(url: str) -> dict:
    try:
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": "council-preflight"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return {"url": url, "ok": True, "status": resp.status}
    except urllib.error.HTTPError as exc:
        return {"url": url, "ok": exc.code < 500, "status": exc.code}
    except (urllib.error.URLError, OSError, ValueError) as exc:
        return {"url": url, "ok": False, "status": None, "error": str(getattr(exc, "reason", exc))}


def git_facts(project: pathlib.Path | None, council: pathlib.Path | None) -> dict:
    facts: dict = {"repo": None}
    if not shutil.which("git"):
        return facts
    where = project or (council.parent if council else None)
    if not where:
        return facts
    probe = where
    while not probe.exists() and probe != probe.parent:
        probe = probe.parent
    code, top = run(["git", "-C", str(probe), "rev-parse", "--show-toplevel"])
    if code != 0:
        return facts
    facts["repo"] = top
    facts["branch"] = run(["git", "-C", top, "branch", "--show-current"])[1]
    facts["uncommitted_paths"] = len([line for line in run(["git", "-C", top, "status", "--porcelain"])[1].splitlines() if line.strip()])
    if council:
        try:
            inside = pathlib.Path(top).resolve() in council.resolve().parents or pathlib.Path(top).resolve() == council.resolve()
        except OSError:
            inside = False
        facts["council_dir_inside_repo"] = inside
        if inside:
            facts["council_dir_git_ignored"] = run(["git", "-C", top, "check-ignore", "-q", str(council)])[0] == 0
    return facts


def find_skills(names: list[str]) -> list[dict]:
    out = []
    for name in names:
        if ":" in name:
            out.append({"skill": name, "found": None, "note": "plugin skill: only the Skill tool can load it, not checked here"})
            continue
        hit = next((root / name / "SKILL.md" for root in SKILL_ROOTS if (root / name / "SKILL.md").is_file()), None)
        out.append({"skill": name, "found": str(hit) if hit else None})
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Report what this machine offers a council. Read-only unless --init.")
    parser.add_argument("--project", help="Folder of the thing under review (repo or working folder).")
    parser.add_argument("--url", action="append", default=[], help="Address a hands-on seat must reach, for example a running dev server. Repeatable.")
    parser.add_argument("--council-dir", help="Where this council's brief, reports and evidence will live.")
    parser.add_argument("--skills", default="", help="Comma-separated skill names you plan to hand to seats.")
    parser.add_argument("--init", action="store_true", help="Create the council folder layout (evidence, round1, round2, seats).")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            reconfigure(encoding="utf-8")

    project = pathlib.Path(args.project) if args.project else None
    council = pathlib.Path(args.council_dir) if args.council_dir else None
    report: dict = {"python": sys.version.split()[0], "platform": sys.platform, "consequences": []}
    report["tools"] = {name: shutil.which(name) for name in ("node", "npx", "git", "ffmpeg", "claude", "codex")}
    if report["tools"]["node"]:
        report["node_version"] = run(["node", "--version"])[1]
    if project and not project.is_dir():
        report["consequences"].append(f"Project folder not found: {project}. Seats cannot read it.")
        project = None
    report["playwright"] = find_playwright(project)
    report["urls"] = [check_url(u) for u in args.url]
    report["git"] = git_facts(project, council)
    report["skills"] = find_skills([s.strip() for s in args.skills.split(",") if s.strip()])

    if council:
        if args.init:
            for sub in ("evidence", "round1", "round2", "seats"):
                (council / sub).mkdir(parents=True, exist_ok=True)
        nearest = council
        while not nearest.exists() and nearest != nearest.parent:
            nearest = nearest.parent  # the folder may not exist yet: test the closest ancestor that does
        report["council_dir"] = {"path": str(council), "exists": council.is_dir(), "writable": nearest.is_dir() and os.access(nearest, os.W_OK)}

    c = report["consequences"]
    pw = report["playwright"]
    if args.url:  # a seat has to reach a page, so browser automation matters
        if not report["tools"]["node"] or not pw["packages"]:
            c.append("No Node Playwright package found near the project. Seats cannot drive a browser from their own script: either give them captured evidence only (screens, recordings, numbers the lead gathered) or point them at a folder that has Playwright, and say in the report that the hands-on part was reduced.")
        elif not pw["browser_folders"]:
            c.append("Playwright is installed but no browser folder was found. Set PLAYWRIGHT_BROWSERS_PATH in the brief or seats will fail on launch.")
    for u in report["urls"]:
        if not u["ok"]:
            c.append(f"{u['url']} did not answer ({u.get('error') or u['status']}). Start the app yourself before the council and tell seats never to start, stop or restart it.")
    if not report["tools"]["ffmpeg"]:
        c.append("ffmpeg not on PATH: motion seats cannot build frame sheets or luminance traces from recordings; they must read values from the page instead.")
    g = report["git"]
    if g.get("council_dir_inside_repo") and not g.get("council_dir_git_ignored"):
        c.append("The council folder is inside the repository and not ignored by git. Reports, screenshots and prompts would show up in git status. Use an ignored folder or a folder outside the repository.")
    if g.get("uncommitted_paths"):
        c.append(f"The repository has {g['uncommitted_paths']} uncommitted path(s). Tell seats what is not part of the work under review, or they will report someone else's edits.")
    for s in report["skills"]:
        if s["found"] is None and "note" not in s:
            c.append(f"Skill '{s['skill']}' was not found in the skill folders. Do not name it in a seat prompt.")
    if council and not report["council_dir"]["writable"]:
        c.append("The council folder cannot be written. Pick another location before launching.")

    report["answer_yourself"] = [
        "Can I start subagents here, and can I choose a model for each one? If not, run seats one after another in this context, write every round 1 answer before reading any of them, and label the run as single-context.",
        "Does each hands-on seat have a way to use the real thing that it does not share with other seats (its own script or browser instance)? Shared browser tools collide when seats run in parallel.",
        "Did the owner name a model limit, a size or a deadline for this council? Their words win over the defaults.",
        "Do I have the owner's own words about what they want and like? The owner's seat quotes them and must not invent any.",
    ]

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    print("Council preflight")
    print(f"- Python {report['python']} on {report['platform']}; node {report.get('node_version', 'not found')}")
    print("- On PATH: " + ", ".join(f"{k} {'yes' if v else 'NO'}" for k, v in report["tools"].items()))
    if pw["packages"]:
        for name, info in pw["packages"].items():
            print(f"- {name} {info['version']}: require from {info['require_from']}")
    else:
        print("- Playwright package: not found near the project")
    for b in pw["browser_folders"]:
        print(f"- Browsers at {b['path']}: {', '.join(b['installed'])}")
    for u in report["urls"]:
        print(f"- {u['url']}: {'answers, HTTP ' + str(u['status']) if u['ok'] else 'NO ANSWER'}")
    if g.get("repo"):
        print(f"- Git repository {g['repo']}, branch {g.get('branch') or '?'}, {g.get('uncommitted_paths', 0)} uncommitted path(s)")
    if council:
        cd = report["council_dir"]
        ignored = g.get("council_dir_git_ignored")
        state = "outside any repository" if not g.get("council_dir_inside_repo") else ("ignored by git" if ignored else "NOT ignored by git")
        print(f"- Council folder {cd['path']}: {'exists' if cd['exists'] else 'not created yet'}, {'writable' if cd['writable'] else 'NOT writable'}, {state}")
    for s in report["skills"]:
        print(f"- Skill {s['skill']}: {s['found'] or s.get('note') or 'NOT FOUND'}")
    print("\nConsequences")
    for line in c or ["Nothing missing among the things this script can check."]:
        print(f"- {line}")
    print("\nAnswer these yourself (the script cannot see your tools)")
    for line in report["answer_yourself"]:
        print(f"- {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
