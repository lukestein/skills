#!/usr/bin/env python3
"""
Download a presentation video plus metadata/subtitles and normalize the saved
video artifact to a high-quality MP4.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


VIDEO_EXTS = (".mp4", ".mkv", ".webm", ".mov", ".m4v")


def run(cmd: list[str], cwd: Path | None = None) -> None:
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def capture_json(cmd: list[str], cwd: Path | None = None) -> dict:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=cwd)
    return json.loads(result.stdout)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download a presentation video and normalize it to MP4."
    )
    parser.add_argument("url", help="Presentation URL to download")
    parser.add_argument(
        "--basename",
        required=True,
        help="Shared basename such as presenter-title",
    )
    parser.add_argument(
        "--workdir",
        type=Path,
        default=Path.cwd(),
        help="Output directory",
    )
    parser.add_argument(
        "--sub-langs",
        default="en.*,en",
        help='Subtitle languages passed to yt-dlp, default "en.*,en"',
    )
    return parser.parse_args()


def find_downloaded_video(prefix: str, workdir: Path) -> Path:
    candidates = [
        path
        for path in workdir.iterdir()
        if path.is_file()
        and (path.name == prefix or path.name.startswith(prefix + "."))
        and path.suffix.lower() in VIDEO_EXTS
    ]
    if not candidates:
        raise FileNotFoundError(f"No downloaded video found for prefix {prefix!r}")
    candidates.sort()
    return candidates[0]


def ffprobe_streams(video_path: Path) -> tuple[str | None, str | None]:
    probe = capture_json(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=index,codec_type,codec_name",
            "-of",
            "json",
            str(video_path),
        ],
        cwd=video_path.parent,
    )
    video_codec = None
    audio_codec = None
    for stream in probe.get("streams", []):
        if stream.get("codec_type") == "video" and video_codec is None:
            video_codec = stream.get("codec_name")
        if stream.get("codec_type") == "audio" and audio_codec is None:
            audio_codec = stream.get("codec_name")
    return video_codec, audio_codec


def normalize_to_mp4(source: Path, target: Path) -> None:
    if target.exists():
        target.unlink()

    video_codec, audio_codec = ffprobe_streams(source)
    audio_args = ["-c:a", "copy"] if audio_codec == "aac" else ["-c:a", "aac", "-b:a", "192k"]

    if source.suffix.lower() == ".mp4" and audio_codec == "aac":
        source.replace(target)
        return

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(source),
        "-map",
        "0:v:0",
        "-map",
        "0:a?",
        "-c:v",
        "copy",
        *audio_args,
        "-movflags",
        "+faststart",
        str(target),
    ]
    run(cmd, cwd=source.parent)

    if source.exists():
        source.unlink()

    if video_codec is None:
        raise RuntimeError(f"Could not detect a video stream in {source}")


def rename_sidecars(temp_base: str, final_base: str, workdir: Path) -> None:
    for path in workdir.iterdir():
        if not path.is_file():
            continue
        if not path.name.startswith(temp_base):
            continue
        new_name = final_base + path.name[len(temp_base) :]
        path.rename(workdir / new_name)


def cleanup_temp_videos(temp_base: str, final_video: Path, workdir: Path) -> None:
    if not final_video.exists():
        return
    for path in workdir.iterdir():
        if not path.is_file():
            continue
        if path == final_video:
            continue
        if not (path.name == temp_base or path.name.startswith(temp_base + ".")):
            continue
        if path.suffix.lower() not in VIDEO_EXTS:
            continue
        path.unlink()


def main() -> int:
    args = parse_args()
    workdir = args.workdir.resolve()
    workdir.mkdir(parents=True, exist_ok=True)

    if shutil.which("yt-dlp") is None:
        raise SystemExit("yt-dlp is required but was not found on PATH")
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is required but was not found on PATH")
    if shutil.which("ffprobe") is None:
        raise SystemExit("ffprobe is required but was not found on PATH")

    temp_base = f"{args.basename}.download"
    final_base = f"{args.basename}.video"

    ytdlp_cmd = [
        "yt-dlp",
        "--no-playlist",
        "--write-info-json",
        "--write-description",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs",
        args.sub_langs,
        "-f",
        "bv*+ba/b",
        "-o",
        f"{temp_base}.%(ext)s",
        args.url,
    ]
    run(ytdlp_cmd, cwd=workdir)

    downloaded_video = find_downloaded_video(temp_base, workdir)
    final_video = workdir / f"{final_base}.mp4"
    normalize_to_mp4(downloaded_video, final_video)
    rename_sidecars(temp_base, final_base, workdir)
    cleanup_temp_videos(temp_base, final_video, workdir)

    print(final_video)
    return 0


if __name__ == "__main__":
    sys.exit(main())
