from PyQt5.QtWidgets import QApplication
from Misc.watchableVariable import WatchableVariable
from Misc.stringWatcherAndReader import StringWatcherAndReader

from ScreenCapture.screenRegionSelector import ScreenRegionSelector

import sys


if __name__ == '__main__':
    wv = WatchableVariable()
    watcher_thread = StringWatcherAndReader(wv)
    watcher_thread.start()

    app = QApplication(sys.argv)
    selector = ScreenRegionSelector(wv.set_value)
    selector.show()

    try:
        sys.exit(app.exec_())
    finally:
        watcher_thread.stop()
        watcher_thread.join()
