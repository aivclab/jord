#!/usr/bin/env python3

__author__ = "Christian Heider Lindbjerg"
__doc__ = r"""

           Created on 02-12-2020
           """

from typing import Tuple

# noinspection PyUnresolvedReferences
from qgis.PyQt import QtWidgets

__all__ = ["make_dialog_progress_bar", "DialogProgressBar"]

from warg import AlsoDecorator, passes_kws_to


class DialogProgressBar(AlsoDecorator):
    @passes_kws_to()
    def __init__(self, progress: int = 0, **kwargs):
        self._progress_dialog, self._progress_bar = make_dialog_progress_bar(
            progress, **kwargs
        )

    def __enter__(self):
        if self._progress_dialog:
            self._progress_dialog.show()
        return self._progress_bar

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._progress_dialog:
            self._progress_dialog.close()


def make_dialog_progress_bar(
    progress: int = 0,
    *,
    minimum_width: int = 300,
    min_value: int = 0,
    max_value: int = 100,
    title: str = "Progress",
    label: str = ""
) -> Tuple[QtWidgets.QDialog, QtWidgets.QProgressBar]:
    """
    Create a progress bar dialog.

    :param title:
    :param label:
    :param min_value:
    :param max_value:
    :param progress: The progress to display.
    :type progress: int
    :param minimum_width: The minimum width of the dialog.
    :type minimum_width: int
    :return: The dialog.
    :rtype: Tuple[QtWidgets.QDialog, QtWidgets.QProgressBar]
    """
    dialog = QtWidgets.QProgressDialog()
    dialog.setWindowTitle(title)
    dialog.setLabelText(label)

    bar = QtWidgets.QProgressBar(dialog)
    bar.setTextVisible(True)
    bar.setValue(min_value)
    bar.setValue(progress)
    bar.setMaximum(max_value)

    dialog.setBar(bar)
    dialog.setMinimumWidth(minimum_width)

    return dialog, bar


if __name__ == "__main__":

    def calc(x, y):
        from time import sleep

        dialog, bar = make_dialog_progress_bar(0)
        bar.setValue(0)
        bar.setMaximum(100)
        sum_ = 0
        for i in range(x):
            for j in range(y):
                k = i + j
                sum_ += k
            i += 1
            bar.setValue((float(i) / float(x)) * 100)
            sleep(0.1)
        print(sum_)

    # calc(10000, 2000)
