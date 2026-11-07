"""Alternative legacy pipeline retained for comparison with the primary workflow."""

from . import separate_cycles_v2
from .background_signals_v2 import add_background
from .change_column_order_v2 import reorder_columns
from .combine_workbook_v2 import combine_workbook
from .cycles_timeline import cycles_timeline
from .difference_signals_v2 import difference_signals
from .graphics import show_success
from .y_transform_v2 import y_transform


def start_analysis() -> None:
    """Run the alternate pipeline in the current input-data directory."""
    timeline = cycles_timeline()
    if timeline == "ERROR":
        raise ValueError("The comments file must contain the same number of START and END markers.")

    rows_before_cycle = 100
    print("Separating cycles...")
    separate_cycles_v2.separate_cycles(timeline, rows_before_cycle)
    print("Applying Y transform...")
    y_transform()
    print("Ordering columns...")
    reorder_columns()
    print("Adding background signal...")
    add_background()
    print("Calculating signal minus background...")
    difference_signals()
    print("Creating the multi-sheet workbook...")
    combine_workbook()
    show_success(
        "Alternative analysis completed:\n\n"
        "Cycle separation, Y transform, column ordering, background correction, "
        "and workbook export."
    )
