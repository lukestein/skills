#!/usr/bin/env python3
"""
Run slide-extractor without its blocking OpenCV preview window.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

SPEAKER_STRIP_FRACTION = 225 / 1280


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run slide-extractor headlessly by bypassing its preview-window pause."
    )
    parser.add_argument(
        "video",
        type=Path,
        help="Path to the local video file",
    )
    parser.add_argument(
        "--skip",
        type=float,
        default=3,
        help="Seconds to skip between frame comparisons",
    )
    parser.add_argument(
        "--diff",
        type=float,
        default=0.008,
        help="Difference threshold for slide capture",
    )
    parser.add_argument(
        "--coords",
        help="Explicit JSON coordinates like '[[0,0],[720,1055]]'",
    )
    parser.add_argument(
        "--layout",
        choices=[
            "full-frame",
            "speaker-right",
            "speaker-left",
        ],
        default="speaker-right",
        help="Convenience crop preset when --coords is not provided",
    )
    parser.add_argument(
        "--exclude-width-fraction",
        type=float,
        default=SPEAKER_STRIP_FRACTION,
        help=(
            "Fraction of the frame width to exclude from the left or right side "
            "when using speaker-left or speaker-right"
        ),
    )
    return parser.parse_args()


def resolve_coords(
    args: argparse.Namespace,
    frame_height: int,
    frame_width: int,
) -> list[list[int]]:
    if args.coords:
        return json.loads(args.coords)

    exclude_fraction = min(max(args.exclude_width_fraction, 0.0), 0.95)
    excluded_width = round(frame_width * exclude_fraction)
    keep_right_edge = max(frame_width - excluded_width, 1)
    keep_left_edge = min(excluded_width, frame_width - 1)

    presets = {
        "full-frame": [[0, 0], [frame_height, frame_width]],
        "speaker-right": [[0, 0], [frame_height, keep_right_edge]],
        "speaker-left": [[0, keep_left_edge], [frame_height, frame_width]],
    }
    return presets[args.layout]


def main() -> int:
    args = parse_args()
    video_path = args.video.resolve()
    if not video_path.exists():
        raise SystemExit(f"Video not found: {video_path}")

    import slide_extractor.main as sem

    # Bypass the package's OpenCV preview-window pause for headless runs.
    sem.cv2.imshow = lambda *a, **k: None
    sem.cv2.waitKey = lambda *a, **k: 32
    sem.cv2.destroyAllWindows = lambda *a, **k: None

    original_fromarray = sem.Image.fromarray

    def corrected_fromarray(obj, *args, **kwargs):
        # OpenCV frames are BGR; PIL expects RGB channel order for correct colors.
        if isinstance(obj, np.ndarray) and obj.ndim == 3 and obj.shape[2] == 3:
            obj = sem.cv2.cvtColor(np.uint8(obj), sem.cv2.COLOR_BGR2RGB)
        return original_fromarray(obj, *args, **kwargs)

    sem.Image.fromarray = corrected_fromarray

    video = sem.cv2.VideoCapture(str(video_path))
    ok, frame = video.read()
    video.release()
    if not ok or frame is None:
        raise SystemExit(f"Could not read a frame from {video_path}")

    frame_height, frame_width = frame.shape[:2]
    coords = sem.np.array(resolve_coords(args, frame_height, frame_width))
    sem.extract_slides(
        path=str(video_path),
        confidence=args.diff,
        skip=args.skip,
        coor=coords,
        url="",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
