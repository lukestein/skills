# Commands

Use these as starting templates, then adjust paths, subtitle languages, and filenames for the specific task.

## Dependency Setup

### Core dependencies

Install these without asking the user. They are small and required for the main workflow:

```bash
brew install ffmpeg yt-dlp
```

For slide extraction, prefer a dedicated Conda environment:

```bash
conda create -n slide_extractor python=3.11 -y
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate slide_extractor
uv pip install --upgrade slide-extractor
```

If not using Conda, install `slide-extractor` into any Python environment you manage:

```bash
uv pip install --upgrade slide-extractor
```

Fallback if `uv` is unavailable:

```bash
python -m pip install --upgrade slide-extractor
```

For interactive use, activation via Conda's shell hook is often more reliable:

```bash
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate slide_extractor
```

### Transcription (optional — ask first)

`parakeet-mlx` involves a large model download. Do not install it without confirming with the user. If the user agrees:

```bash
uv tool install parakeet-mlx
```

## Inspect URL Metadata

Use `yt-dlp` to inspect metadata before choosing the final basename:

```bash
yt-dlp --dump-single-json --no-playlist "$URL" > raw-video-info.json
```

Useful lightweight fields:

```bash
yt-dlp --print "%(uploader)s" --print "%(title)s" --no-playlist "$URL"
```

## Reuse Policy

Before running any command, check what already exists in the working folder.

- Reuse an existing local video instead of downloading again.
- Reuse an existing MP3 instead of extracting audio again.
- Reuse existing subtitles unless the user asks for a fresh download or different languages.
- If you are comparing slide extraction settings, reuse the same video and write the alternate PDF to a separate folder or filename.

Example inventory check:

```bash
find . -maxdepth 1 -type f | sort
```

## Download Video and Subtitles

Prefer an MP4 container for saved local videos. This is usually more convenient for reuse and matches the skill's naming examples.

For the most reliable high-quality MP4 result, use the bundled helper. It downloads the best available source, then normalizes the saved local artifact to MP4 while keeping the video stream untouched whenever possible:

```bash
python3 /path/to/presentation-video-pipeline/scripts/download_presentation_video.py \
  "$URL" \
  --basename presenter-title \
  --workdir /absolute/path/to/output-folder
```

Behavior:

- Downloads the best available source video plus metadata and subtitles.
- Writes the final saved video as `presenter-title.video.mp4`.
- Copies the video stream when possible.
- Re-encodes audio to AAC only when needed for MP4 compatibility.
- Removes the temporary downloaded video container after the final MP4 is in place.

First try an MP4-compatible video/audio pair:

```bash
yt-dlp \
  --no-playlist \
  --write-info-json \
  --write-description \
  --write-subs \
  --write-auto-subs \
  --sub-langs "en.*,en" \
  -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]" \
  -o "%(title)s [%(id)s].video.%(ext)s" \
  "$URL"
```

After download, rename the outputs to the shared basename you want to keep.

If the source does not offer a usable MP4-compatible pair, you have two reasonable fallbacks:

- Compatibility-first: download an MP4-only fallback, accepting that it may be lower quality than the best available stream.
- Quality-first: download the best available streams even if they merge to `.mkv`, then optionally convert afterward.

Quality-first fallback:

```bash
yt-dlp \
  --no-playlist \
  --write-info-json \
  --write-description \
  --write-subs \
  --write-auto-subs \
  --sub-langs "en.*,en" \
  -f "bv*+ba/b" \
  -o "%(title)s [%(id)s].video.%(ext)s" \
  "$URL"
```

Prefer this over `slide-extractor -u "$URL"` because:

- `yt-dlp` gives better metadata and subtitle control.
- You can name all derived artifacts consistently.
- The current `slide-extractor` package writes generic filenames when invoked with a URL.

Tradeoff note:

- Forcing MP4 too aggressively can fail or reduce quality when YouTube offers the best audio only as WebM/Opus.
- Preferring MP4-compatible streams first is usually the safest default for presentation videos.

## Extract Slides

Run slide extraction from a local video file with the raw package CLI only when you specifically need its interactive preview behavior:

```bash
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate slide_extractor
slide-extractor \
  -p /absolute/path/to/presenter-title.video.mp4 \
  -s 1 \
  -d 0.008
```

Prefer the bundled helper for normal extraction work:

```bash
python /path/to/presentation-video-pipeline/scripts/headless_slide_extractor.py \
  /absolute/path/to/presenter-title.video.mp4 \
  --skip 3 \
  --diff 0.008
```

By default, the helper assumes a Zoom-style speaker thumbnail on the right side. Use `--layout full-frame` when no side exclusion is needed, or `--layout speaker-left` when the speaker is on the left.

Parameter meanings:

- `--skip` matches the package's `-s/--skip` and defaults to `1`.
- `--diff` matches the package's `-d/--diff` and defaults to `0.008`.

How to tune them from plain-language feedback:

- If some slides appeared only briefly and were missed, reduce `--skip`.
- If a slide stayed on screen but still was missed because it looked too similar to the previous slide, reduce `--diff`.
- If too many near-duplicate slides are captured, increase `--diff`.
- If extraction is too slow and the deck changes slowly, increase `--skip`.

If the slide region is smaller than the whole frame, crop the comparison area:

```bash
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate slide_extractor
slide-extractor \
  -p /absolute/path/to/presenter-title.video.mp4 \
  -c '[[120,80],[1820,1030]]'
```

For a common 1280x720 recording where a speaker thumbnail sits on the right side, try:

```bash
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate slide_extractor
slide-extractor \
  -p /absolute/path/to/presenter-title.video.mp4 \
  -s 3 \
  -c '[[0,0],[720,1055]]'
```

That crop excludes the rightmost 225 pixels of a 1280-pixel-wide frame, which is about 17.6% of the width. For other resolutions, scale that fraction rather than reusing `225` literally.

The helper script supports the same idea without the GUI dependency:

```bash
python /path/to/presentation-video-pipeline/scripts/headless_slide_extractor.py \
  /absolute/path/to/presenter-title.video.mp4 \
  --skip 3 \
  --layout speaker-right
```

For a speaker thumbnail on the left side, use:

```bash
python /path/to/presentation-video-pipeline/scripts/headless_slide_extractor.py \
  /absolute/path/to/presenter-title.video.mp4 \
  --skip 3 \
  --layout speaker-left
```

For a split-screen recording where the speaker occupies roughly the full left or right half, keep the same layout name and increase the excluded fraction:

```bash
python /path/to/presentation-video-pipeline/scripts/headless_slide_extractor.py \
  /absolute/path/to/presenter-title.video.mp4 \
  --skip 3 \
  --layout speaker-left \
  --exclude-width-fraction 0.5
```

Use `speaker-right` instead when the speaker occupies the right half.

Notes:

- The current package writes the PDF next to the input video as `<video-stem>.pdf`.
- The package opens an OpenCV preview window on the first slide; use it in an interactive desktop session with GUI access.
- The raw package path can produce incorrect slide colors because OpenCV frames are BGR; the bundled helper corrects that before saving the PDF.
- In this demo, the command started successfully in an interactive shell and printed `Please check the preview image for the area you want to be compared`, but failed to show the preview because macOS GUI services were unavailable inside the agent environment.
- If the command seems to stall before any PDF appears, suspect that it is blocked on the preview window.
- Sending a space to the terminal did not unblock the preview step in this environment. This suggests the confirmation is tied to the OpenCV window event loop rather than plain terminal stdin.
- In testing, importing the package and monkeypatching `cv2.imshow`, `cv2.waitKey`, and `cv2.destroyAllWindows` allowed extraction to proceed normally in a headless shell. The bundled helper script wraps that approach.
- The helper's speaker-layout presets exclude a resolution-scaled fraction of the left or right edge, based on Zoom's typical 225-of-1280 thumbnail width, instead of hard-coding 225 pixels.
- You can override that default with `--exclude-width-fraction` when the speaker pane is much wider than a Zoom thumbnail.
- With the current extractor, top-right and bottom-right are the same practical crop, and top-left and bottom-left are the same practical crop, because the kept comparison region spans the full frame height.
- If the deck changes slowly and duplicate frames are being captured, increase `-s` or `-d`.
- If slide changes are being missed, decrease `-s` or `-d`.

## Extract MP3

Create a good-quality MP3:

```bash
ffmpeg -i presenter-title.video.mp4 -vn -c:a libmp3lame -q:a 2 presenter-title.audio.mp3
```

## Transcribe With Parakeet MLX

Create SRT output:

```bash
parakeet-mlx transcribe \
  presenter-title.audio.mp3 \
  --output-dir . \
  --output-format srt \
  --output-template "{filename}"
```

Create JSON output when you want sentence-level structure for later processing:

```bash
parakeet-mlx transcribe \
  presenter-title.audio.mp3 \
  --output-dir . \
  --output-format json \
  --output-template "{filename}"
```

Useful options from the installed CLI include:

- `--chunk-duration`
- `--overlap-duration`
- `--max-words`
- `--silence-gap`
- `--max-duration`
- `--fp32`
- `--local-attention`
- `--verbose`

Troubleshooting:

- On this machine, importing `parakeet-mlx` in a headless shell can crash before help text appears because MLX initializes Metal eagerly.
- If transcription fails with an MLX or Metal initialization error, rerun from a normal interactive Mac session.

## Clean Transcript Into Markdown

Use the bundled helper:

```bash
python3 scripts/clean_transcript.py \
  presenter-title.subtitles.srt \
  --title "Presenter - Title" \
  --output presenter-title.transcript.md
```

Optionally apply a terminology glossary:

```bash
python3 scripts/clean_transcript.py \
  presenter-title.parakeet.json \
  --title "Presenter - Title" \
  --glossary terminology.tsv \
  --output presenter-title.transcript.md
```

Glossary format:

```text
hetero skedastic	heteroskedastic
sharp ratio	Sharpe ratio
```
