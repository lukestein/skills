#!/usr/bin/env python3
"""
Convert subtitle or ASR output into lightly cleaned Markdown.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TIMESTAMP_RE = re.compile(
    r"^\s*\d{2}:\d{2}:\d{2}(?:[.,]\d{3})?\s*-->\s*\d{2}:\d{2}:\d{2}(?:[.,]\d{3})?"
)
NUMERIC_INDEX_RE = re.compile(r"^\s*\d+\s*$")
DEFAULT_GLOSSARY = {
    "hetero skedastic": "heteroskedastic",
    "hetero skedasticity": "heteroskedasticity",
    "sharp ratio": "Sharpe ratio",
}
FILLER_PATTERNS = [
    re.compile(r"\b(?:um+|uh+|er+|ah+|mm+|hmm+)\b[\s,]*", re.IGNORECASE),
    re.compile(r"\byou know\b[\s,]*", re.IGNORECASE),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert subtitle or ASR output into lightly cleaned Markdown."
    )
    parser.add_argument("input", type=Path, help="Input transcript file")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output Markdown path. Defaults to <input-stem>.md",
    )
    parser.add_argument(
        "--title",
        help="H1 title for the Markdown file. Defaults to title-cased input stem.",
    )
    parser.add_argument(
        "--section-title",
        default="Transcript",
        help="Default H2 section heading.",
    )
    parser.add_argument(
        "--glossary",
        type=Path,
        help="Optional tab-separated glossary file with 'wrong<TAB>right' entries.",
    )
    return parser.parse_args()


def load_input(path: Path) -> str:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix == ".json":
        data = json.loads(text)
        if isinstance(data, dict) and isinstance(data.get("text"), str):
            return data["text"]
        if isinstance(data, dict) and isinstance(data.get("sentences"), list):
            return " ".join(
                sentence.get("text", "").strip()
                for sentence in data["sentences"]
                if isinstance(sentence, dict)
            )
        raise ValueError("Unsupported JSON transcript structure")
    return text


def strip_subtitle_markup(text: str) -> str:
    lines = []
    for raw_line in text.replace("\r\n", "\n").split("\n"):
        line = raw_line.strip()
        if not line:
            lines.append("")
            continue
        if line == "WEBVTT":
            continue
        if NUMERIC_INDEX_RE.match(line):
            continue
        if TIMESTAMP_RE.match(line):
            continue
        if line.startswith("NOTE ") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        line = re.sub(r"<[^>]+>", "", line)
        lines.append(line)
    return "\n".join(lines)


def load_glossary(path: Path | None) -> dict[str, str]:
    glossary = dict(DEFAULT_GLOSSARY)
    if not path:
        return glossary
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        wrong, right = line.split("\t", 1)
        glossary[wrong.strip()] = right.strip()
    return glossary


def apply_glossary(text: str, glossary: dict[str, str]) -> str:
    for wrong, right in sorted(glossary.items(), key=lambda item: len(item[0]), reverse=True):
        pattern = re.compile(rf"\b{re.escape(wrong)}\b", re.IGNORECASE)
        text = pattern.sub(right, text)
    return text


def clean_text(text: str) -> str:
    text = strip_subtitle_markup(text)
    text = text.replace("\n", " ")
    for pattern in FILLER_PATTERNS:
        text = pattern.sub("", text)
    text = re.sub(r"\b(\w+)(?:\s+\1\b)+", r"\1", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+([,.;:?!])", r"\1", text)
    text = re.sub(r"([,.;:?!])([^\s])", r"\1 \2", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"(?:\s*,){2,}", ",", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text)
    sentences = [normalize_sentence(part.strip()) for part in parts if part.strip()]
    return sentences or [text]


def normalize_sentence(sentence: str) -> str:
    return re.sub(
        r"^([\"']?)([a-z])",
        lambda match: f"{match.group(1)}{match.group(2).upper()}",
        sentence,
    )


def chunk_paragraphs(sentences: list[str], target_words: int = 120) -> list[str]:
    paragraphs: list[str] = []
    current: list[str] = []
    current_words = 0
    for sentence in sentences:
        words = len(sentence.split())
        current.append(sentence)
        current_words += words
        if current_words >= target_words:
            paragraphs.append(" ".join(current).strip())
            current = []
            current_words = 0
    if current:
        paragraphs.append(" ".join(current).strip())
    return paragraphs


def default_title(path: Path) -> str:
    stem = path.stem.replace("_", " ").replace("-", " ")
    return " ".join(part.capitalize() for part in stem.split())


def build_markdown(title: str, section_title: str, paragraphs: list[str]) -> str:
    body = "\n\n".join(paragraphs)
    return f"# {title}\n\n## {section_title}\n\n{body}\n"


def main() -> int:
    args = parse_args()
    raw_text = load_input(args.input)
    glossary = load_glossary(args.glossary)
    cleaned = clean_text(apply_glossary(raw_text, glossary))
    paragraphs = chunk_paragraphs(split_sentences(cleaned))
    title = args.title or default_title(args.input)
    output_path = args.output or args.input.with_suffix(".md")
    output_path.write_text(
        build_markdown(title, args.section_title, paragraphs),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
