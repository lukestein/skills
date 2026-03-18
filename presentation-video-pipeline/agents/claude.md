---
display_name: "Presentation Video Pipeline"
short_description: "Extract slides, audio, and transcript from a presentation recording"
invocation: "/presentation-video-pipeline"
install:
  skill_file: ../SKILL.md
  target: ~/.claude/skills/presentation-video-pipeline.md
---

## Claude Code Integration

The skill definition lives in `SKILL.md` at the root of this folder. Claude Code skill
files are standalone Markdown files placed in `~/.claude/skills/`. Install by copying:

```bash
cp presentation-video-pipeline/SKILL.md ~/.claude/skills/presentation-video-pipeline.md
```

Once installed, invoke via the slash command:

```
/presentation-video-pipeline
```

Or mention it naturally in a prompt — Claude Code will trigger it based on the
`description` field in the frontmatter when the context matches (presentation URL,
local video file, slide extraction request, etc.).

## Default Prompt

> Use /presentation-video-pipeline to process this presentation recording into slides, audio, and a cleaned transcript.
