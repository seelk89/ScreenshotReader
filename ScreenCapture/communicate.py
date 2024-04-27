from PyQt5.QtCore import pyqtSignal, QObject


class Communicate(QObject):
    changed = pyqtSignal()
