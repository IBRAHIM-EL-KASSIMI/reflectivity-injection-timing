"""Application entry point and input validation."""

import argparse
from pathlib import Path

from . import __version__
from .cycles_timeline import cycles_timeline


def validate_input_directory(input_directory: str | Path) -> str | None:
    """Return a user-facing validation error, or None when inputs are ready."""
    directory = Path(input_directory)
    if not directory.is_dir():
        return f"Input directory does not exist: {directory}"

    entries = list(directory.iterdir())
    files = [path for path in entries if path.is_file()]
    data_files = [
        path
        for path in files
        if "kinetics" in path.name.lower()
        and "data" in path.name.lower()
        and "comment" not in path.name.lower()
    ]
    comments_files = [path for path in files if "comment" in path.name.lower()]
    spot_files = [path for path in files if "spot" in path.name.lower()]

    if not data_files:
        return "No KineticsData file was found in the selected input directory."
    if not comments_files:
        return "No Kinetics_comments file was found in the selected input directory."
    if len(comments_files) > 1:
        return "Keep exactly one comments file in the input directory."
    if not spot_files:
        return "No Spot file was found in the selected input directory."
    output_folders = {"cycles_csv", "cycles_txt", "sep_cycles_csv", "sep_cycles_txt"}
    if any(path.suffix.lower() == ".xlsx" for path in files) or any(
        path.name.lower() in output_folders for path in entries
    ):
        return (
            "An Excel workbook or generated cycle folder already exists. "
            "Use a clean copy of the input files to avoid overwriting results."
        )

    try:
        timeline = cycles_timeline(directory)
    except ValueError as error:
        return str(error)
    if timeline == "ERROR":
        return "The comments file must contain the same number of START and END markers."
    return None


def main(argv: list[str] | None = None) -> int:
    """Validate the current working directory and start the desktop workflow."""
    parser = argparse.ArgumentParser(
        description="Analyze molecular reflectivity traces by injection cycle."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.parse_args(argv)

    error = validate_input_directory(Path.cwd())
    from .graphics import show_error, show_start_prompt

    if error is not None:
        show_error(error)
        return 1

    from .pipeline import start_analysis

    show_start_prompt(start_analysis)
    return 0
