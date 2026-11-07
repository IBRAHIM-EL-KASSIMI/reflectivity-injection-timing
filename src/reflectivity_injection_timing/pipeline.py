"""The primary data-processing pipeline."""

from . import separate_cycles
from .align_cycle_starts import align_cycle_starts
from .background_signals import add_background
from .change_column_order import reorder_columns
from .combine_workbook import combine_workbook
from .cycles_timeline import cycles_timeline
from .detect_response_rise import detect_response_rise
from .difference_signals import difference_signals
from .graphics import show_success
from .rows_to_remove import rows_to_remove
from .x_transform import x_transform
from .y_transform import y_transform


def start_analysis() -> None:
    """Run the established analysis steps in the current input-data directory."""
    timeline = cycles_timeline()
    if timeline == "ERROR":
        raise ValueError("The comments file must contain the same number of START and END markers.")

    rows_before_cycle = 100
    print("Separating cycles...")
    separate_cycles.separate_cycles(timeline, rows_before_cycle)
    print("Applying Y transform...")
    y_transform()
    print("Detecting response rises and applying X transform...")
    rises = detect_response_rise()
    x_transform(rows_to_remove(rises))
    print("Ordering columns...")
    reorder_columns()
    print("Adding background signal...")
    add_background()
    print("Calculating signal minus background...")
    difference_signals()
    print("Aligning cycle starts...")
    align_cycle_starts()
    print("Creating the multi-sheet workbook...")
    combine_workbook()
    show_success(
        "Analysis completed:\n\n"
        "Cycle separation, Y transform, response-rise alignment, column ordering, "
        "background correction, and workbook export."
    )
