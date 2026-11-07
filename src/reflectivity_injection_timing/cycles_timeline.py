"""Read injection cycle boundaries from an instrument comments file."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

import chardet

CycleTimeline = dict[int, tuple[int, int, str]]
TimelineResult = CycleTimeline | Literal["ERROR"]

_TIME_PATTERN = re.compile(r"^\s*(\d{2}):(\d{2}):(\d{2})")


def _seconds_from_line(line: str, line_number: int) -> int:
    match = _TIME_PATTERN.match(line)
    if match is None:
        raise ValueError(f"Expected an HH:MM:SS timestamp on line {line_number}.")

    hours, minutes, seconds = (int(value) for value in match.groups())
    return hours * 3600 + minutes * 60 + seconds


def parse_cycle_timeline(lines: list[str]) -> TimelineResult:
    """Parse START/END markers into numbered (start, end, title) tuples."""
    starts: list[tuple[int, str]] = []
    ends: list[int] = []

    for line_number, line in enumerate(lines, start=1):
        if "START" in line:
            title_match = re.search(r"\bSTART\s*(.*)", line)
            if title_match is None or not title_match.group(1).strip():
                raise ValueError(f"Missing cycle title on line {line_number}.")
            title = title_match.group(1).strip().replace(" ", "_").replace("/", "_")
            starts.append((_seconds_from_line(line, line_number), title))
        if "END" in line:
            ends.append(_seconds_from_line(line, line_number))

    if len(starts) != len(ends):
        return "ERROR"

    return {
        index: (start, ends[index - 1], title)
        for index, (start, title) in enumerate(starts, start=1)
    }


def cycles_timeline(directory: str | Path = ".") -> TimelineResult:
    """Read the comments file in *directory* and return its cycle boundaries."""
    input_directory = Path(directory)
    comments_files = sorted(
        path
        for path in input_directory.iterdir()
        if path.is_file() and "comment" in path.name.lower()
    )
    if not comments_files:
        raise FileNotFoundError(
            f"No comments file was found in {input_directory.resolve()}."
        )
    if len(comments_files) > 1:
        raise ValueError(
            f"Expected one comments file in {input_directory.resolve()}, "
            f"found {len(comments_files)}."
        )

    comments_file = comments_files[0]
    contents = comments_file.read_bytes()
    detected_encoding = chardet.detect(contents).get("encoding")
    encoding = detected_encoding or "utf-8"
    text = contents.decode(encoding, errors="replace")
    return parse_cycle_timeline(text.splitlines())
