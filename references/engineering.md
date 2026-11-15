# Council for engineering

Four shapes. In engineering the seats are split by failure class, and the rigour is in the evidence format: every finding traced to a file and line, marked CONFIRMED or PLAUSIBLE, with a concrete failure scenario. Give each seat a name and a short card anyway. The "cannot stand" line still aims the review ("assumes every green test suite is hiding something until they have read the assertions").

Before any of them: read the repository's own instruction files (`AGENTS.md`, `CLAUDE.md`, contributing rules) and paste the rules that bind a reviewer into the brief.

## 1. Quick architecture choice

Three reasoning seats, no tools, evidence pasted in, under 450 words each (template in `briefs.md`). One seat per competing concern, for example visual fidelity, interaction and accessibility, product engineering. Each scores the options on its own criteria, names its two biggest risks with a way to reduce each, and predicts where the other seats will disagree. If all three pick the same option for different reasons, record the decision and move on.

## 2. Design review before building

Three seats read the design document and the code it builds on.

| Seat | Attacks the design as | Returns |
|---|---|---|
| Security and abuse | A hostile user, a hostile recipient of shared data, hostile text inside the data, a careless admin | For each finding: blocker, should-fix or note; the concrete attack; the smallest design change that closes it |
| Feasibility and correctness | Someone who must make it compile and survive restarts, cancels and concurrency in this codebase | The exact files, functions and tests that must change, with file and line |
| Product fit | The person who wrote the acceptance text | Requirement by requirement: covered, partly covered, missing, and the smallest addition that turns each gap into covered or into an honest "not in this version" |

Give each a word limit (900 to 1,000), sorted by severity, and forbid restating the design.

## 3. Close-out before a merge

Three seats, each owning one way the change could hurt, using the defect-hunt template in `briefs.md`.

- **Data safety:** could this lose data, write where it must not, weaken isolation, hang or crash.
- **User story:** what the person does, in which state, and what then goes wrong on screen. Include the paths you could not click through yourself as "trace these".
- **Contract and claims:** do the layers agree (what one side sends and the other reads), does the documentation say what the code does, do the new tests fail when the behaviour is removed, is anything unfinished left in the diff. List the pull request's own claims and have the seat mark each "holds" or name where it breaks.

What you prepare: the diffs as files in the council folder, a plain-words list of what the change does, the "already known, do not report" list, and a warning about any uncommitted work by other people in the same tree. "NO FINDINGS" with a "checked and fine" list is a valid answer. Merge only after each confirmed finding is fixed or consciously deferred by the owner.

## 4. Technology or platform decision

When the owner asks "would X give us a real advantage?". Four seats.

| Seat | Job | Format |
|---|---|---|
| Fact scout | Answer listed questions from primary sources as of today | Every fact with a link and a tag: primary, secondary or unverified. Open questions answered or "not found" |
| Architect | Say from the actual code what adopting X would mean and the smallest sound design | Verdict with file and line, files to touch, risks, hours |
| Security red team | Find every way this could hurt customers or the vendor | Risks ranked with a one-line failure scenario and a mitigation each, and a verdict per option: ship now, ship with conditions, do not ship |
| Strategist | Bold path first: is this a real advantage or a distraction, who benefits, what a competitor must do to match, and which move gives the most advantage per hour | Ranked recommendation, including a better move if one exists |

Write each prompt with a stretch goal, an observable acceptance line, a word limit and a tool-call limit. The fact scout may use the web; the others read code. Verdicts are given per option, so the seats can disagree usefully ("buildable now" against "wait until browsers ship it").

## Verification is your job

- Trace or reproduce every blocker yourself before acting on it.
- In the report, separate what you verified from what rests on a seat's word ("the seats cite a security fix in version 151; I did not check that one").
- A finding marked PLAUSIBLE is a lead for you to finish, not a fact.

## Round 2

After the fixes, the seat that raised a finding re-traces only its own findings and marks each fixed, better, unchanged or worse, quoting the new line. For a close-out this is usually one short seat run, not the whole council.

## Rules that belong in the brief

- Read-only. No builds, no installs, no git commands that change anything. If a build is needed, you run it once and put the result in the evidence pack.
- Check every claim against the working tree as it is, not only against the diff.
- Never report other people's uncommitted work as part of the change.
- No web requests about private code. Only the fact scout researches, and only public facts.
