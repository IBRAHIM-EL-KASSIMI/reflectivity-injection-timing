# Reflectivity-Based Injection Timing Analyzer (RITA)

RITA processes molecular reflectivity time-series from injection experiments. It
segments traces using the instrument's annotated injection-cycle boundaries,
detects and aligns response rises, applies background correction, and exports
the results to a multi-sheet Excel workbook.

> **Scope:** The current workflow uses `START` and `END` timestamps from the
> experiment comments file as cycle boundaries. It does not independently
> predict injection times from raw reflectivity measurements.

## Requirements

- Python 3.10 or later
- A desktop environment supported by Qt (PyQt5)
- Instrument-exported kinetics data, a comments file, and a spot file

## Install

Clone the repository and create an environment:

```bash
git clone https://github.com/ELKA-IBRAHIM/DATA_ANALYSIS_PROJECT.git
cd DATA_ANALYSIS_PROJECT
python -m venv .venv
```

Activate it and install the application:

```bash
# Linux or macOS
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install -e .
```

## Prepare and run an analysis

Use a **separate, empty folder** for each run. Put these files in that folder:

1. One or more kinetics data files. Their names must contain both `Kinetics`
   and `Data` (for example, `KineticsData1.txt`).
2. Exactly one comments file. Its name must contain `comment`.
3. One spot file. Its name must contain `spot`.

The comments file must start each relevant line with an `HH:MM:SS` timestamp.
Mark every injection-cycle boundary with `START` and `END`; include a cycle
title after `START`. Kinetics files must be tab-delimited, with elapsed time in
minutes in the first column and signal values in the remaining columns. The
spot file must follow the instrument's tab-delimited format; each signal name
must have a numeric order prefix followed by a dash (for example,
`1-moleculeA`).

Change to the folder containing the input files, then launch RITA:

```bash
cd /path/to/your/private-run-folder
rita
```

You can also run `python -m reflectivity_injection_timing`. The app checks the
required inputs and opens a confirmation dialog before processing. It will
decline to run if Excel workbooks or generated cycle folders are already in the
input folder; move the original inputs to a clean folder for a new run.

The analysis produces intermediate cycle files and a date-stamped
`Analysed_Data_YYYY-MM-DD.xlsx` workbook in the input folder. Keep the original
inputs backed up and review the generated workbook before using it downstream.

## Development

Install the optional development tools and run the test suite:

```bash
python -m pip install -e ".[dev]"
python -m pytest
ruff check src tests
```

Application source is in `src/reflectivity_injection_timing/`; tests use
synthetic inputs and do not require experiment data. The default launcher uses
the primary pipeline in `pipeline.py`. `pipeline_v2.py` retains an alternate
historical workflow for comparison and is not the default application path.

## Data privacy

Experiment files and generated results are private by default and should not be
added to the public repository. `.gitignore` excludes common local data and
output paths, but ignore rules are not a privacy guarantee. Review
`git status --short` and the complete commit history before publishing or
sharing a repository.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE).
