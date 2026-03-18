# Skills Repository

This repo contains shareable AI agent skills. Each skill lives in its own folder and
is defined primarily by its `SKILL.md`.

## Structure

```
<skill-name>/
  SKILL.md               # Authoritative skill definition (used by Claude Code directly)
  agents/
    openai.yaml          # OpenAI Codex interface config
    claude.md            # Claude Code interface config and install instructions
  scripts/               # Reusable helper scripts referenced by the skill
  references/            # Supplemental command templates and editorial guides
```

## Installing a Skill in Claude Code

Each `SKILL.md` is a valid Claude Code skill file (it has the required YAML frontmatter).
Copy it to your skills directory:

```bash
cp <skill-name>/SKILL.md ~/.claude/skills/<skill-name>.md
```

Then invoke with `/<skill-name>` or let Claude trigger it automatically based on context.
See each skill's `agents/claude.md` for skill-specific install notes.

## Available Skills

- `presentation-video-pipeline` — turn a presentation recording into a local video,
  slide PDF, MP3, subtitles, and a cleaned Markdown transcript.
