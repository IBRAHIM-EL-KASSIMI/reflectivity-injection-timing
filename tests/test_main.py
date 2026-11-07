import tempfile
import unittest
from pathlib import Path

from reflectivity_injection_timing.main import validate_input_directory


class ValidateInputDirectoryTests(unittest.TestCase):
    def create_valid_inputs(self, directory: Path) -> None:
        (directory / "KineticsData1.txt").write_text("", encoding="utf-8")
        (directory / "Kinetics_comments.txt").write_text(
            "00:00:10 START molecule A\n00:00:50 END wash\n",
            encoding="utf-8",
        )
        (directory / "Spot file.txt").write_text(
            "synthetic spot metadata\n",
            encoding="utf-8",
        )

    def test_accepts_valid_synthetic_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            self.create_valid_inputs(directory)

            self.assertIsNone(validate_input_directory(directory))

    def test_reports_missing_data_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            (directory / "Kinetics_comments.txt").write_text(
                "00:00:10 START molecule A\n00:00:50 END wash\n",
                encoding="utf-8",
            )
            (directory / "Spot file.txt").write_text("synthetic\n", encoding="utf-8")

            self.assertIn("KineticsData", validate_input_directory(directory))

    def test_refuses_to_run_when_workbook_already_exists(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            self.create_valid_inputs(directory)
            (directory / "Analysed_Data_2026-01-01.xlsx").touch()

            self.assertIn("already exists", validate_input_directory(directory))

    def test_refuses_to_run_when_generated_cycle_folder_exists(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            self.create_valid_inputs(directory)
            (directory / "Cycles_csv").mkdir()

            self.assertIn("already exists", validate_input_directory(directory))


if __name__ == "__main__":
    unittest.main()
