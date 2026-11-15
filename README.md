# named-council

named-council is an agent skill for Claude Code and Codex. It convenes a small council of reviewer subagents to judge a piece of work before you ship, merge, send or teach it. Each reviewer gets a name, a craft, and a list of things they love and cannot stand. Each one also gets a different job to do on the real thing, so every report is based on something the reviewer measured or tried.

After you fix what they found, the same reviewers come back and check their own findings.

## What you type

```text
make a council and judge the new checkout page before I ship it, the dev server is on localhost:5173
council this pull request before I merge
I have to answer this client message, council it before I send
tomorrow I teach day 3, small council on the homework, cheap models only
```

## What you get

Three to five seats, cast for the task. A seat is a character like this one:

> Ayo, 34, interaction and motion designer who has shipped award-site work and native apps. You measure everything: durations in ms, easing curves, spring stiffness and damping. You love motion that tells you what an object weighs and what will happen next. You dislike decoration that delays the user, animation that cannot be interrupted, and hover effects that fire when you are just passing through.

The dislikes are the checklist. A seat tends to come back with exactly those problems, measured.

- Each seat works on the real artifact. One uses the app at phone size and times its tasks. Others read animation timings from the page, trace a code path, read your message as the person receiving it, or do the homework in an empty folder.
- One seat speaks for your taste and quotes your own words.
- The lead agent checks the important findings itself and reports what several seats found from different jobs, where they disagree, and what it could not verify. Scores are tallied by a script.
- After your fixes, each returning judge marks its own findings fixed, better, unchanged or worse and scores again.

A small edit or a lookup gets no council. The skill says so and does the work directly.

## Install

Claude Code:

```bash
git clone https://github.com/OthmanAdi/named-council ~/.claude/skills/named-council
```

Codex and other agents that read `~/.agents/skills`:

```bash
git clone https://github.com/OthmanAdi/named-council ~/.agents/skills/named-council
```

In Windows PowerShell, replace `~` with `$env:USERPROFILE`. Start a new session afterwards.

## Requirements

- An agent host that can start subagents. Without them the skill runs a reduced form in one context and says so in its report.
- Python 3 for two helper scripts (standard library only, tested on 3.14). `scripts/preflight.py` reports what the machine offers a council. `scripts/tally.py` builds the score tables from the seat reports.
- Seats that drive a web app use Playwright from your own project. The skill installs nothing.

Full councils have been run in Claude Code. In Codex the skill has been tested up to the point of launching seats.

## Cost

Most of the cost comes from the number of steps each seat takes. In the author's runs in Claude Code in November 2026, a seat that only reasons used about 50,000 tokens. A hands-on seat with a prepared evidence pack used 130,000 to 250,000, and seats without limits used up to 425,000. The skill gives every seat a step limit, a time limit and at most 8 findings, and it states the expected total before a large council starts.

## What is in the repository

- `SKILL.md`: the method.
- `references/`: how to cast seats, prompt and report templates, guides for product and design work, engineering, business and messages, and teaching, plus notes for Claude Code and Codex.
- `scripts/`: the two helper scripts.

## Credits

The blind first round, the rule that a judge who changes position must give the reason, and tallying by script come from [the-jury](https://github.com/tech-leads-club/agent-skills) by Felipe Rodrigues (CC BY 4.0). Other ideas come from [roast-room](https://github.com/nateherkai/roast-room), the council skill in [agentops](https://github.com/boshu2/agentops) and marketing-council in [marketingskills](https://github.com/coreyhaines31/marketingskills).

## License

MIT. See [LICENSE](LICENSE).
