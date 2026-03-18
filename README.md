# Skills Repository

This repository contains shareable Codex skills.

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

## Working With This Repo

- Review each skill's `SKILL.md` for usage guidance.
- Treat `references/` as supplemental detail and `scripts/` as reusable helpers.
- Before publishing, confirm that local artifacts such as `runs/`, `demo/`, `.DS_Store`, and `__pycache__/` are ignored or removed.
