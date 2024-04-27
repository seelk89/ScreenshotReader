from PyQt5.QtWidgets import QApplication
from Misc.stringWatcherAndReader import StringWatcherAndReader

from ScreenCapture.screenRegionSelector import ScreenRegionSelector

import sys
import queue


if __name__ == '__main__':
    q = queue.Queue()
    swr = StringWatcherAndReader(q)
    swr.start()

    app = QApplication(sys.argv)
    selector = ScreenRegionSelector(q)
    selector.show()

    try:
        sys.exit(app.exec_())
    finally:
        while not q.empty():
            try:
                q.get_nowait()
            except queue.Empty:
                break

        swr.stop()
        swr.join()
