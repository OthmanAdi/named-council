# Council for business, career and messages

Three shapes. Before advice that touches money, time or commitments, read whatever record of the owner's real constraints exists (a budget, a calendar, signed agreements) and prefer dated corrections over older lines. If two records disagree and the outcome depends on it, say so in one line.

Put the bold option on the table and argue it properly, even if the cautious one wins.

## 1. Decision council

"Should I take this contract, raise the rate, build this product, accept this offer?" Three to five seats, each with a different job.

| Seat | Job | Evidence |
|---|---|---|
| Fact scout | Answers the factual questions the decision rests on (market rates, terms, deadlines, what the other party has published) | Each fact with a source and a tag: primary, secondary, unverified |
| The operator | Works out what saying yes means in the owner's real week and bank account: hours, dates, cash, what it displaces | Numbers from the records, stated assumptions |
| Receiving end | The customer, employer or partner. Reads the offer or plan as they would and says what they would do next | The sentence or number that decides it for them |
| Dissenter | Attacks the favoured option: the worst realistic outcome, what would be regretted in six months, the cost nobody counted | One failure scenario per risk, and what would reduce it |
| Strategist | Bold path first. Names the move with the most advantage per hour and what a competitor would need to match it | A ranked recommendation, including a better move if one exists |

Run round 1 blind. Each seat commits to an option (no "it depends": caveats go under assumptions), gives two to four grounded arguments, grades its own evidence A to D, states what would change its mind, and gives a confidence from 0 to 100. Always include "do nothing" or "keep doing what you do now" as an option.

A second round is optional and only for a real split. Show each seat the others' positions without names (Position 1, Position 2), ask it to state the strongest opposing case before answering, and require any change of position to cite the new argument or fact that caused it. `scripts/tally.py` flags changes with no reason and changes that only follow the first majority; when it does, weigh the blind round 1 positions instead. Stop after that round.

If there are no options yet, use round 1 to produce them: each seat proposes one or two options from where it sits, plus one idea nobody asked for. You group them into A, B and C, and the seats then score those blind.

Your verdict: the decision in one line, up to five reasons, the strongest opposing view kept in one line, the assumption that would break it, the cheapest test of that assumption, and the first step the owner can take today.

## 2. Message council

A reply to a client, a negotiation step, an outreach mail, a follow-up to a recruiter, a difficult message to a partner.

What you prepare, in one brief file:

- The incoming message, word for word, with time and channel.
- The timeline and facts, each with where it comes from. Mark what is inferred.
- Real samples of how the owner writes to this person (greeting, length, sign-off).
- What the message should achieve, in the owner's words.
- Two or three candidate drafts, V1 to V3. Seats attack drafts far better than they fill a blank page.

| Seat | Job | Returns |
|---|---|---|
| The recipient | Thinks as the person receiving it, not as the sender's friend. Built from their real messages and role | Ranked readings of what they meant, with rough likelihoods and the one piece of evidence behind each. What they need to read to feel it is handled. What would make them roll their eyes. A yes or no on each thing the reply might contain. Their own version of the reply |
| The sender's voice | Reads the owner's real messages and builds a voice card: greeting, sentence length, the verbs and phrases actually used, how commitment is shown without grovelling, sign-off, and a "never" list | The drafts rewritten in that voice, and which now sounds most like the sender |
| Red team | Hunts the worst misreading by a tired reader: anything defensive, any promise that cannot be kept, anything that reads as hurt or as an exit, anything a third party could contradict, language that sounds written by a machine | Each draft scored out of 10, its two worst lines with a replacement each, a merged best version, and one line on what was left out and why |

These are brief seats: each reads the brief file, uses at most 10 tool calls and about 500 words, and has its own deliverable, so they do not overlap. The prompt for each lens and the judge-pass prompt are in `briefs.md` ("Seat prompt, message council"). Do not shrink this into a quick council that only scores drafts A, B and C: the recipient's ranked readings, the voice card and the red team's worst lines are what you merge from.

Then merge the seats' work into one candidate and send it through one judge pass on a stronger model. That pass replaces round 2. Run a second round only if the owner changes what the message should achieve.

If you have no real samples of how the owner writes to this person, say so, build the voice seat on their stated intent instead, and name the missing samples in your report.

Your report: the final text in a code block, why it looks the way it does in a few lines, and **what sending it commits the owner to**, as a numbered list they can refuse before it goes out. Breaking a promise in the message is worse than any wording.

Rules:

- Nothing is typed or sent until the owner says go for that exact text. After go, send it as approved, once.
- Write in the recipient's language.
- Keep the report short and give the text. People often ask for this while upset; do not lecture.

## 3. Career and public-profile pieces

A CV, a cover letter, a pitch, a talk abstract, a profile page.

| Seat | Job |
|---|---|
| Hiring reader | Scans the first screen for ten seconds, says which role this person is for and the first thing they would click, and names one missing or misleading signal |
| Engineering peer | Checks the strongest claims against the public source (repository, release, registry) and flags any number or ownership claim it cannot verify |
| First-time visitor | Finds one thing to try or read, and names the first word or click that confused them |
| Owner's seat | Holds the piece against what the owner said they want to be hired or known for |

Every personal claim needs a source. Never round a number up or invent a date.
