---
name: presentation-video-pipeline
description: Turn a recorded talk, lecture, webinar, or screen-shared presentation video into reusable artifacts such as a downloaded local video, extracted slide PDF, audio-only MP3, subtitles, and a cleaned Markdown transcript. Use when given a presentation URL or video file and asked to do any combination of video download, slide extraction with slide-extractor, audio extraction with ffmpeg, subtitle download with yt-dlp, transcription with parakeet-mlx, transcript cleanup, or output renaming based on inferred presenter/title metadata.
---

# Presentation Video Pipeline

## Overview

Use this skill to process a presentation recording into stable local files with a single shared basename. Prefer a local-video workflow even when the input starts as a URL so that download, slides, audio, subtitles, and transcript all stay synchronized and predictably named.

## Workflow

1. Determine which outputs the user wants: local video, slide PDF, MP3, subtitles, transcript Markdown, or a subset.
2. Normalize the working basename before doing downstream work.
3. Inventory the working directory before doing anything expensive. Reuse existing video, audio, subtitle, PDF, and transcript files when they already satisfy the request.
4. If the input is a URL, download the video and any available subtitles only when the local artifacts do not already exist or when the user explicitly asks for a fresh download.
5. Extract slides from the local video, not from the URL, unless there is a compelling reason not to.
6. Extract audio from the local video with `ffmpeg` only if the needed MP3 does not already exist.
7. Prefer downloaded subtitles when they exist and are good enough; otherwise transcribe the MP3 with a user-approved ASR tool.
8. Convert subtitle or ASR output into Markdown, apply terminology corrections, remove filler/false-start noise, and add topic-shift headers when the user asked for a polished transcript.
9. Rename outputs so the final set shares the same basename.

## Reuse Existing Artifacts

Do not redo completed steps by default.

- If the video is already downloaded locally, reuse it.
- If subtitles already exist, reuse them unless the user asks for a new download or a different language.
- If the MP3 already exists, reuse it for transcription work.
- If a slide PDF already exists and the user is not asking for a rerun with different settings, reuse it.
- If the user wants to tweak only slide extraction settings such as sampling frequency or similarity sensitivity, rerun only the slide step.
- If a rerun needs isolation for comparison, write outputs into a separate comparison folder or use a different suffix, but do not redownload the source video unless necessary.
- If redoing work would overwrite an existing artifact, ask only when the overwrite has non-obvious consequences; otherwise prefer a new suffix or subfolder.

## Naming

Infer a human-readable label and a filesystem-safe basename from the source.

- Use the presenter name from uploader, channel, event metadata, or filename when available.
- Use the talk title from the video title, page title, or filename stem.
- Prefer `presenter-title` in lowercase kebab case for the shared basename.
- Prefer a human-readable title like `Presenter - Title` inside the Markdown transcript H1.
- Keep every artifact aligned to the same basename, for example:
  - `presenter-title.video.mp4`
  - `presenter-title.audio.mp3`
  - `presenter-title.slides.pdf`
  - `presenter-title.subtitles.srt`
  - `presenter-title.transcript.md`
  - `presenter-title.info.json`

If the original filename is already good, preserve it and add only the suffixes above.

## Input Handling

If the user gives a URL:

- Read exact command templates in [references/commands.md](./references/commands.md).
- Download once with `yt-dlp`, including info JSON and subtitles when available.
- Prefer an MP4 output container for the local saved video so downstream artifacts match the naming convention and are easier to reuse outside this workflow.
- Prefer MP4-compatible format selection first, then fall back only when the source does not offer a usable MP4-compatible pair.
- When high quality and reliable MP4 output both matter, prefer the bundled helper to download the best source and then normalize the saved local artifact to MP4.
- After a successful MP4 normalization, delete the temporary downloaded video container such as `.download.mkv` so the run folder keeps only the final local video artifact by default.
- Prefer this route over passing `-u` directly to `slide-extractor`, because the direct-URL mode produces generic output names and relies on an older embedded YouTube stack.

If the user gives a local video file:

- Keep the original untouched.
- Create derived files beside it or in a dedicated output folder.
- Use the local file as the source of truth for slide extraction and MP3 creation.

## Slide Extraction

Use `slide-extractor` through the `slide_extractor` conda environment when available.

- Prefer an interactive shell that explicitly sources Conda before activation:
  - `source "$(conda info --base)/etc/profile.d/conda.sh" && conda activate slide_extractor`
- Prefer the bundled [scripts/headless_slide_extractor.py](./scripts/headless_slide_extractor.py) for actual extraction work, even outside headless environments, because it also corrects the package's BGR-to-RGB color issue before PDF generation.
- Use the raw `slide-extractor` CLI only when you explicitly need to interact with its preview window behavior for crop discovery.
- `conda run -n slide_extractor ...` may work for some environments, but it is less reliable for this package when GUI interaction is required.
- Use `-c` coordinates when only part of the shared screen contains the slide deck.
- Unless the user says otherwise, assume a Zoom-style recording with a speaker thumbnail on the right side.
- For common Zoom-style recordings with the speaker video on the right side, a useful starting crop is to exclude roughly the rightmost `225 / 1280`, or about `17.6%`, of the frame from comparison.
- Treat speaker-thumbnail cropping as configurable. With this extractor, the meaningful distinction is left side versus right side; top versus bottom does not change the crop because the comparison region spans the full frame height.
- The package writes `<video-stem>.pdf` next to the local video, so rename it afterward if the desired basename is different.
- The package opens an OpenCV preview window on the first detected slide and waits for interaction. Run it in an interactive desktop session with GUI access, not a headless shell.
- In agent or sandboxed terminal environments, it may appear to hang after printing `Please check the preview image for the area you want to be compared`. Treat that as a likely GUI-blocked state, not as proof that slide detection is broken.
- Sending a space or Enter to terminal stdin may not unblock this step. The installed package uses OpenCV window interaction, so confirmation likely has to reach the preview window itself.
- Prefer [scripts/headless_slide_extractor.py](./scripts/headless_slide_extractor.py), which imports the package, bypasses the preview-window pause when needed, and fixes the package's color-channel issue before writing the PDF.
- The helper defaults to `speaker-right`, which matches the usual Zoom-style thumbnail layout.
- The helper's `speaker-right` and `speaker-left` layouts scale to the actual video width rather than assuming a fixed 720p crop.
- The helper also accepts `--exclude-width-fraction` so the same left/right layouts can handle both narrow Zoom thumbnails and wider split-screen speaker panels.
- A good default for Zoom thumbnails is about `225 / 1280`, or `0.176`.
- A good starting point for a full left-half or right-half speaker panel is `0.5`.
- Start with the package defaults: `skip=1` second and `diff=0.008`.
- `skip` controls how often the video is sampled.
  - Smaller `skip` catches brief slides and fast transitions better, but takes longer.
  - Larger `skip` runs faster, but can miss slides that appear only briefly.
- `diff` controls how different a sampled frame must be from the previous accepted slide before it is captured.
  - Smaller `diff` is more sensitive and helps catch slides that look similar to the previous slide.
  - Larger `diff` is stricter and can reduce duplicate captures, but may miss slides whose visual changes are modest.
- Translate user feedback into these controls even if the user never mentions parameter names:
  - “We missed slides that appeared quickly” means decrease `skip`.
  - “We missed slides that looked too similar” means decrease `diff`.
  - “We got too many duplicates” means increase `diff`, and sometimes increase `skip`.

## Audio Extraction

Use `ffmpeg` to create a high-quality MP3 from the local video.

- Prefer the command templates in [references/commands.md](./references/commands.md).
- Keep the audio basename aligned with the video basename.
- If the user asked only for transcript work, still keep the MP3 because it is the durable input for re-transcription later.

## Subtitle and Transcript Strategy

Choose the cheapest trustworthy text source first.

1. Use manually uploaded subtitles if they exist.
2. Otherwise use auto-generated YouTube subtitles if they are available and acceptable.
3. Otherwise transcribe the MP3 with an ASR tool.

Before reaching step 3, ask the user how they want to handle transcription. Do not install or run any transcription tool without confirmation. Suggested prompt:

> No subtitles are available. To generate a transcript I would need to transcribe the audio. I can use `parakeet-mlx` (Apple Silicon / MLX, large model download) or another tool you prefer. How would you like to proceed?

If the user confirms `parakeet-mlx`:

- Use the `transcribe` subcommand and write results into the working output folder.
- Prefer `srt` or `json` output when you plan to post-process into Markdown.
- Note that this installation may crash in a headless terminal when MLX cannot initialize Metal. If that happens, say so clearly and instruct the user to rerun on a local interactive Mac session.

If the user names a different tool, use that instead and adapt the output to whatever format `clean_transcript.py` accepts (`.srt`, `.vtt`, `.txt`, `.md`, or Parakeet `.json`).

## Transcript Cleanup

Use [scripts/clean_transcript.py](./scripts/clean_transcript.py) for the deterministic first pass, then do a final editorial pass in prose when needed.

- The script accepts `.srt`, `.vtt`, `.txt`, `.md`, or Parakeet `.json`.
- It removes subtitle timestamps and index lines.
- It applies conservative filler-word cleanup and de-duplicates immediate repeated words.
- It applies glossary replacements from a tab-separated file when provided.
- It writes Markdown with an H1 title and a default H2 section.

After the script runs, do the higher-judgment cleanup yourself when the user asked for a polished transcript:

- Correct likely phonetic/domain errors such as terminology names.
- Remove obvious false starts and stutters without changing the speaker's meaning.
- Preserve the speaker's critiques, claims, and tone.
- Add H2 topic-shift headings based on the actual structure of the talk. Do not summarize away substantive detail.

See [references/transcript-cleanup.md](./references/transcript-cleanup.md) for the expected editing standard.

## Dependency Setup

Core dependencies — install these without asking:

- `yt-dlp` for video and subtitle download
- `ffmpeg` for audio extraction
- `slide-extractor` in a Python or conda environment (small package, required for slide extraction)

Optional heavy dependency — ask before installing:

- `parakeet-mlx` for ASR transcription on Apple Silicon / MLX-compatible setups. This is a large model download. Confirm with the user before installing it, and offer to use their preferred transcription tool instead.

For installation examples and command templates, read [references/commands.md](./references/commands.md).

## Environment Notes

Use the demo lessons from this skill carefully:

- `parakeet-mlx` may crash in some headless shells before transcription starts because MLX initializes Metal eagerly.
- `slide-extractor` may require a normal desktop terminal session on macOS because it tries to display an OpenCV preview window.
- When a workflow works in the user's local terminal but not in an agent shell, prefer explaining the environment mismatch over assuming the tool itself is broken.

## OCR Extension

If the user later asks for OCR on extracted slides, treat that as an extension to this workflow:

- Reuse the extracted slide PDF or image sequence as the OCR input.
- Use OCR text to improve speaker terminology, names, citations, and slide titles in the transcript.
- Keep OCR instructions in a separate reference or script rather than bloating this skill until that workflow is actually needed.
