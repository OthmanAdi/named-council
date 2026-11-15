# Council for products, interfaces and design

Use for a product pass, a new view or feature, a visual direction, a landing page, a profile or portfolio page, a video or figure.

## Evidence pack (you build it once)

- Stills of every state and look at the sizes that matter, phone sizes included, with an `index.md` saying what each shows.
- Frame recordings or contact sheets of each motion (open, close, drag, flick, first load).
- The references the owner loves, captured at the same sizes, so the owner's seat can compare side by side. Add a short written summary of how each reference works, with measured facts. Capture public reference pages yourself before launch and note the date; seats work from that snapshot unless a seat's job is to capture fresh frames.
- Anything countable, made by script: every colour, size, duration and user-facing string.
- How to run the thing: the address, how a script loads the browser automation, helper scripts for a screenshot and a hover or drag. If preflight finds no browser automation near the project, point `--project` at a folder that has it, or ask the owner before installing anything. Otherwise seats work from your captures and you say the hands-on part was reduced.

References are for ideas only. Say so in the brief: seats compare against them and never propose copying code, art or wording.

## Seats to consider

Pick three to five. Each line is a different job, so each passes the same-actions test.

| Seat | Hands-on job | Evidence it brings |
|---|---|---|
| Owner's seat (creative director with the owner's taste) | Puts the work beside each reference, fresh captures of both, and answers where it wins, where it loses and which few moves would close the gap | Paired frames, the owner's quoted words |
| Receiving end (the person who would use it daily, often on a phone) | Does real tasks and times them, at laptop and phone size, and notes every moment of hesitating, squinting or waiting. Checks what survives a reload | Task, what happened, the screenshot |
| Motion | Drives real mouse, touch and keys, records frames, reads transforms and timings from the page | Durations in ms, curves, overshoot, the frame where it breaks |
| Light and material, or typography and layout | Samples pixels, sweeps the pointer, measures boxes and computed styles at each width | Numbers: ratios, pixels, colour pairs |
| Accessibility and performance | Keyboard walk with the focused element logged, accessibility tree, contrast from computed colours, reduced motion, forced colours, zoom, idle rendering, load size | Reproduction steps, the measured value, the standard it fails |
| Heavy real-world user | Loads 1, 60, 300 and 2,000 items, tries wrong input, imports and exports, tries to find one thing among many | What broke at which size |
| Editor against generic work | Quotes every label, sentence and layout that reads as a default and writes the specific version | The exact string and its replacement |
| Engineering skeptic | Traces frame cost, reads what the tests assert, feeds corrupt and hostile input | Traces, the test that would still pass if the feature were broken |

For a small pass, three seats cover most of the value: the owner's seat, the receiving end, and the one craft the work lives or dies on.

## Axes

Take them from the owner's words for this piece of work. For a 3D product view they might be real, physical, light, touch, plus "would I keep using it". For a page they might be clear in five seconds, looks designed, believable, plus "would I click". Three to five axes, one of them about behaviour.

## Skills for seats

If you have skills installed that sharpen a seat's craft (an accessibility review, a motion performance audit, a writing or anti-generic-design checklist), hand a seat at most two, by path, and name the section to apply. A seat that loads five whole skills re-reads all of them on every step.

## Rules that belong in the brief

- Read-only on the product. No installs, no git writes, no builds into the product's own output folder.
- Headless browsers often render with a software GPU: judge the image and the behaviour, not the frame rate.
- Say what cannot be checked without a person or a device (a real screen reader, a real phone keyboard, pull-to-refresh) and list the manual checks as a short script.
- Features still being built are listed under "not finished yet": seats say what those must get right and do not report them as missing.
- Every report names what is good and must not be lost. Fix lanes read that list first.

## After round 1

Group verified findings into fix lanes by area (light, materials, motion, layout, flows) with one owner per lane and disjoint files. Fix the thing the owner complained about by name first. Then round 2 with the seats whose findings were worked on, and the before and after score table.
