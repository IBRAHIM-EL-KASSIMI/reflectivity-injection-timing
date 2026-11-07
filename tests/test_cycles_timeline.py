import tempfile
import unittest
from pathlib import Path

from reflectivity_injection_timing.cycles_timeline import (
    cycles_timeline,
    parse_cycle_timeline,
)


class ParseCycleTimelineTests(unittest.TestCase):
    def test_parses_times_and_normalizes_cycle_title(self) -> None:
        timeline = parse_cycle_timeline(
            [
                "00:00:10 Valve START molecule A / 3.5 min",
                "00:00:50 Valve END wash",
            ]
        )

        self.assertEqual(timeline, {1: (10, 50, "molecule_A___3.5_min")})

    def test_returns_error_when_marker_counts_differ(self) -> None:
        timeline = parse_cycle_timeline(["00:00:10 START molecule A"])

        self.assertEqual(timeline, "ERROR")

    def test_rejects_malformed_timestamps(self) -> None:
        with self.assertRaisesRegex(ValueError, "HH:MM:SS"):
            parse_cycle_timeline(["not-a-time START molecule A"])

    def test_reads_comments_file_from_given_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            comments_file = Path(temporary_directory) / "Kinetics_comments.txt"
            comments_file.write_text(
                "00:00:10 START molecule A\n00:00:50 END wash\n",
                encoding="utf-8",
            )

            self.assertEqual(
                cycles_timeline(temporary_directory),
                {1: (10, 50, "molecule_A")},
            )


if __name__ == "__main__":
    unittest.main()
