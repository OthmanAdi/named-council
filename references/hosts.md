# Hosts: running a council in Claude Code and in Codex

The method is the same on both. Only the mechanics differ. Model names change, so read the list your own spawn tool shows before choosing, and treat the names below as the state in November 2026.

## Claude Code

- **Launch:** one `Agent` call per seat, all in the same message. `subagent_type: general-purpose`, `description: "Council: <seat>"`, `model` set per seat, the seat prompt as `prompt`. No custom system prompt is needed: the character lives in the first message. Seats can run in the background; their reports arrive as notifications, so do not poll.
- **Models:** `haiku` is the small model, `sonnet` the mid one and `opus` the top one. If your account lists a tier above `opus`, that is "the most expensive tier" in the skill. A sensible default is the mid model for most seats, the stronger one where the judgement decides the outcome, and the most expensive tier rarely. A model the owner names for a run wins.
- **Reports:** the harness often refuses a subagent that tries to write a report file. Ask for the whole report as the final message and file it yourself under `round1/`. Do not tell a seat to route around a refusal. Seats can still save scripts and captures in their own folder.
- **Skills:** seats inherit the skill list and can use the Skill tool. Give the file path too, as a fallback.
- **Browser:** each seat runs its own headless script. Shared browser tools (any Playwright or Chrome MCP server) hold one browser for everyone and collide when seats run in parallel.
- **Round 2:** start a new agent and point it at its own round 1 report. `SendMessage` to a finished seat also works and keeps its memory, but it re-reads that whole context on every step, so use it only for a short follow-up question.

## Codex

- **Launch:** `spawn_agent` per seat with a `task_name` such as `council_leila`, the seat prompt as `message`, and `fork_turns: "none"`. Without that setting the seat inherits your whole conversation, which makes it both expensive and no longer blind. Leave `agent_type` unset unless a configured role fits exactly: configured roles can carry a fixed model.
- **Models:** take them from the spawn tool's own list. Small, mid and top map to the cheapest, the everyday and the strongest regular model there; a frontier model priced above those is "the most expensive tier". Use the fast, affordable model for walkthroughs and plain measurement, the everyday models for most seats, and the frontier model for at most one seat or one final judge pass.
- **Waiting and filing:** `wait_agent` until the mailbox reports a final answer, file it, then close the seat so its thread is freed. `list_agents` shows what is still live.
- **Round 2:** `followup_task` to a seat that is still open, or a new `spawn_agent` with the seat's own round 1 report. Prefer the new agent when the first one's context is large.
- **Skills:** a seat loads a skill by reading its `SKILL.md` from the skills folder.

## Without subagents

Run the same method in one context and say so in the first line of your report: "Ran single-context: the seats were not independent."

1. Do the hands-on work once yourself and put it in the evidence pack.
2. Cast at most three seats.
3. Write every seat's round 1 answer before comparing any of them. Finish one card, then start the next from the brief, not from the previous answer.
4. Skip round 2 debate. A re-check after fixes is still worth doing: go back to each seat's own findings and mark them.

## Things that are true on both

- Seats run in parallel only if their folders and tools do not overlap. One folder per seat.
- If you are yourself a subagent, keep seats on small or mid models, cap how many run at once, and allow none below them. Launch in waves if you must. Blindness is kept as long as no seat is shown another's report.
- You start anything that must be running (an app, a database) before launch and you stop only what you started. Seats start and stop nothing.
- Each seat's first message is saved, as sent, in `PROMPTS.md`.
- Every subagent begins with a fixed block of context before its task (tens of thousands of tokens in a typical setup with many tools and skills). That block is re-read on every step, which is one more reason to keep step counts low.
- If a seat fails or returns nothing, report it as missing. Do not fill its chair from your own head, and do not relaunch it more than once.
