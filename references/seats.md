# Seats: how to cast a council

Contents: the character card, the job, the chairs, casting tests, grounding rules, an example bench.

## The character card

A card is three or four sentences. Each part does work.

| Part | Why it is there |
|---|---|
| Name | So the owner, you and round 2 can refer to one stable voice. Pick plain, varied names. |
| Age, only when it changes behaviour | A 22-year-old student reads on a phone on the train. A 58-year-old bookbinder does not. Leave it out when it changes nothing. |
| Craft and concrete experience | "Twelve years lighting watches and perfume for product films" tells the seat what it knows how to look at. A title alone ("lighting expert") does not. |
| What they love | Two or three specific things. The seat will recognise them when they are present and say what must not be lost. |
| What they cannot stand | Two or three specific things. This is the checklist. These lines tend to come back as the seat's top findings almost word for word. |
| How they work | "You film first and talk second." "You measure everything in milliseconds." This sets the kind of evidence the seat brings. |

Two cards as they were sent in real councils:

> Ayo, 34, interaction and motion designer who has shipped award-site work and native apps. You storyboard in frames, you care about anticipation, follow-through, overlap, weight and settle, and you measure everything: durations in ms, easing curves, spring stiffness and damping, velocity hand-off from finger to animation. You love motion that tells you what an object weighs and what will happen next. You dislike decoration that delays the user, uniform easing on everything, animation that cannot be interrupted, and hover effects that fire when you are just passing through.

> Amara, the Bookmark Keeper: a researcher with 2,400 browser bookmarks, eleven half-abandoned read-later apps behind you and no patience left. You judge a tool by one question: would I actually move my links into this and still be using it in a month? You try everything a real person would try, including the wrong things, and you write down exactly where you got stuck.

Write the dislikes as things that can be observed in this artifact. "Dislikes bad UX" produces nothing. "Hover effects that fire when you are just passing through" produced a measured finding and a fix.

For seats that hunt defects in code, a design or a contract, the card can be short (name, craft, what they refuse to accept), because the job description carries the detail. Keep the name and the "cannot stand" line even there.

## The job

Every seat gets one job with three parts.

1. **Scope.** The slice of the thing this seat owns, with the files, screens or paragraphs to start from.
2. **Hands-on actions.** Things the seat does to the real artifact that no other seat does. Write them as verbs: find this item by reading labels at 1366x768; drag, flick and release, then read the transform every frame; read the draft as the client and write the first thought you would have; do the homework in an empty folder and time each step.
3. **Evidence standard.** What each finding must carry: a file and line, a named screenshot and where to look, a number the seat measured, the exact sentence quoted, the step where it got stuck.

For a seat that plays a user, learner or recipient, add one or two if-then lines that decide its behaviour, so the role is acted and not narrated: "If you hesitate twice on the same screen, stop the task and record it as failed." "If the first two sentences do not tell you what the sender wants from you, stop reading and say what you would do next."

## The chairs

Fill these from the request. Most councils need the first three.

- **The receiving end.** Whoever lives with the result: a user, a learner, the client who gets the message, the engineer who maintains the code next year. Give this seat real tasks, not opinions about tasks.
- **The dissenter.** A skeptic or red team whose job is to attack the favoured path or the draft at full strength: the worst misreading, the abuse case, the cost nobody counted. One real dissenter is required whenever there is a favoured option. Forced theatrics are not: if the dissenter tried and failed to break it, it says so.
- **The owner's seat.** Stands in for the owner's taste or voice. It is given their exact words (what they said they love, what they asked for, their real past messages) and judges against them. Use it when taste or voice decides the outcome. It represents their taste, it does not outrank evidence.
- **Craft seats.** One per craft the work depends on: motion, lighting, typography, security, data, pedagogy, pricing. Each must have a hands-on action the other craft seats lack.
- **The fact scout.** For decisions that rest on outside facts. It answers listed questions from primary sources, and every fact carries a link and a tag: primary, secondary or unverified.
- **A two-chair seat** is fine when one journey has a giver and a receiver, such as a teacher who hands out a reading list and the student who opens it. One agent plays both and walks the whole journey.
- **No clerk.** Mechanical counting (every colour literal, every user-facing string, every changed file) is a script you run before the council and put in the evidence pack. An agent doing this can cost more than a craft seat and usually ends up writing the script anyway.

## Casting tests

Run these before launch.

1. **Same-actions test.** Write each seat's hands-on actions in one line. Two seats with the same line get merged, however different their characters sound.
2. **Coverage list.** Write what no seat looks at (for example: nobody tests offline behaviour, nobody reads the pricing page). Put the list in the brief's "not covered" line and in your final report.
3. **Name-swap test.** If a seat's expected take would survive with another seat's name on it, the character is not doing anything. Sharpen the craft and the dislikes or drop the seat.
4. **Size.** Three seats for a quick council, three to five for a working council. Above five, each extra seat mostly repeats and adds cost.

## Grounding rules

- Characters are invented people. Do not model a seat on a real student, colleague or family member.
- A seat may stand in for a real recipient (the client who will read the message, the hiring manager) when you give it the real evidence: their actual messages, their role, what they have reacted to before. It is a simulation built from that evidence and you say so. It never states what the real person thinks as fact.
- If the owner asks what a public figure would say, the seat reasons from that person's published work, quotes only lines you can point to, and paraphrases the rest as its own reasoning.
- The owner's seat quotes only what the owner actually said or wrote. If you have none of their words on the point, ask once or leave the seat out.
- No invented credentials, statistics or quotes anywhere. A character's background is a way of looking, not a source of authority. Findings must be things the artifact did, not things a stereotype would say.
- Play the character through what it checks, not through an accent or slang.

## An example bench

Characters from real councils, as a starting point. Reusing a name for the same craft keeps the voice familiar across projects; write a fresh card for each new artifact. Cast new characters whenever the work needs a craft that is not here.

| Name | Craft | Cannot stand | What the seat did |
|---|---|---|---|
| Rafael | Creative director, the owner's seat | A feature bolted on without commitment | Put the work side by side with the references the owner loves and judged it against their quoted words |
| Leila | Second-year student, phone on the train | Pretty that means slow, not finding yesterday's link | Timed real tasks at laptop and phone size, recorded every hesitation |
| Priya | Accessibility and performance engineer | Focus rings that vanish, motion that ignores preferences | Keyboard walk, accessibility tree, contrast from computed colours, reduced motion, forced colours |
| Ayo, Kenji | Motion | Hover that fires in passing, anything that blinks or pops | Filmed frame by frame, read transforms and timings from the page |
| Tomás | Lighting and look development | Flat ambient light, highlights that do not move | Sampled pixels, swept the pointer, compared colour pairs |
| Tobias | Typesetter | A one-pixel misalignment, white space left to chance | Measured boxes and computed styles at seven widths |
| Marguerite | Editor against generic work | Filler sentences, labels that say nothing | Quoted the offending line and wrote the specific replacement |
| Amara | Heavy real-world user | Tools that get in the way | Tried everything a real person would, including the wrong things, at 1 to 2,000 items |
| Jonas and Mira | Teacher and student, two chairs | A hand-out that cannot be handed out | Walked the give, receive and work-through journey on desktop and phone |
| Viktor | Engineering skeptic | "It's fast enough", green tests that assert nothing | Traced frames, read assertions, tried corrupt input |
| Lena | Mobile designer, one thumb | Controls out of reach, layouts untested between 600 and 1000 px | Real touch input at seven sizes, thumb-reach map |
