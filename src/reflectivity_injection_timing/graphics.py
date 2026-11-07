"""Small Qt dialogs used by the desktop application."""

from collections.abc import Callable

from PyQt5.QtGui import QColor, QIcon, QPalette
from PyQt5.QtWidgets import QApplication, QMessageBox

_APP = QApplication.instance()


def _application() -> QApplication:
    global _APP
    application = QApplication.instance()
    if application is not None:
        _APP = application
    elif _APP is None:
        _APP = QApplication([])
    return _APP


def show_error(message: str) -> None:
    _application()
    dialog = QMessageBox()
    dialog.setWindowTitle("Input error")
    dialog.setText(message)
    dialog.setIcon(QMessageBox.Critical)
    dialog.setStandardButtons(QMessageBox.Ok)
    dialog.exec_()


def show_success(message: str = "The analysis completed successfully.") -> None:
    _application()
    dialog = QMessageBox()
    dialog.setWindowTitle("Analysis complete")
    dialog.setText(message)
    dialog.setIcon(QMessageBox.Information)
    dialog.setStandardButtons(QMessageBox.Ok)
    palette = dialog.palette()
    palette.setColor(QPalette.Window, QColor(220, 255, 220))
    dialog.setPalette(palette)
    dialog.exec_()


def show_start_prompt(
    function_to_execute: Callable[[], None] | None = None,
) -> None:
    _application()
    dialog = QMessageBox()
    dialog.setIcon(QMessageBox.Information)
    dialog.setWindowTitle("Ready to analyze")
    dialog.setText("Required files were found. Click OK to start the analysis.")
    dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    dialog.setWindowIcon(QIcon.fromTheme("dialog-information"))

    if function_to_execute is not None:
        def start_analysis() -> None:
            dialog.close()
            function_to_execute()

        dialog.button(QMessageBox.Ok).clicked.connect(start_analysis)

    dialog.exec_()
