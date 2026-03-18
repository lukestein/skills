# Skills Repository

This repository contains shareable AI agent skills, compatible with both OpenAI Codex and Claude Code.

## Structure

- Each skill lives in its own folder.
- Each skill is defined primarily by its `SKILL.md`.
- Optional `scripts/`, `references/`, and `assets/` folders support the skill when needed.

## Included Skills

- `presentation-video-pipeline`: turn a presentation recording into reusable artifacts such as a downloaded local video, extracted slides PDF, MP3 audio, subtitles, and a cleaned Markdown transcript.

## Distribution Notes

- Keep skill folders lean and portable.
- Do not commit local run outputs, caches, or ad hoc experiment folders.
- Prefer generic examples in docs over machine-specific paths.
- Put repo-level documentation here at the root rather than adding extra README files inside each skill folder unless there is a strong reason.

## Using With Claude Code

Each `SKILL.md` doubles as a Claude Code skill file — it already has the required YAML frontmatter. Install a skill by copying it to your Claude skills directory:

```bash
cp <skill-name>/SKILL.md ~/.claude/skills/<skill-name>.md
```

Then invoke with `/<skill-name>` in any Claude Code session. See each skill's `agents/claude.md` for details. A `CLAUDE.md` at the repo root provides project context when you open this repo directly in Claude Code.

## Using With OpenAI Codex

Each skill's `agents/openai.yaml` defines the Codex interface configuration. Refer to each skill's `SKILL.md` for the full workflow and `agents/openai.yaml` for the display name and default prompt.

## Working With This Repo

- Review each skill's `SKILL.md` for usage guidance.
- Treat `references/` as supplemental detail and `scripts/` as reusable helpers.
- Before publishing, confirm that local artifacts such as `runs/`, `demo/`, `.DS_Store`, and `__pycache__/` are ignored or removed.
