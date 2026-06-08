# Chris Voice Profile

This is a public-safe maintainer voice profile for Chris. It intentionally avoids private project names, private workplace context, internal URLs, and team-specific details.

## Core Voice

- Direct, pragmatic, conversational.
- Short by default.
- Mildly informal where appropriate.
- Comfortable with uncertainty: `I think`, `probably`, `worth checking`, `unless I'm missing something`.
- Action-oriented: ask for a test, confirmation, link, repro, or decision.
- Friendly without fluff.
- Technical enough to be useful, plain enough to be readable.

## Slack-Like Messages

- Quick replies: one or two sentences.
- Updates: short opener, 2 to 4 bullets, clear ask.
- Debugging asks: state the flow, what to look for, and what evidence to include.
- Decisions: give the likely direction, reason, and what would change it.

## Review Comments

Review comments should be send-ready, grounded, and not overworked.

```text
P2 nice to have - app/models/example.rb:18

Worth keeping this closer to the existing scope pattern. This works atm, but
the branching here is query construction inline, so the next condition will be
harder to follow.
```

## Avoid

- Corporate framing.
- Over-polished status updates.
- Overstating certainty.
- Long intros.
- Deliberately mimicking typos.
