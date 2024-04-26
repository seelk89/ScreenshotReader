from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QFrame,
    QPushButton,
)
from PyQt5.QtCore import Qt

from ScreenCapture.capture import Capture


class ScreenRegionSelector(QMainWindow):
    BACKGROUND_COLOR = '#3f3f3f'
    BUTTON_NORMAL_COLOR = 'rgb(60, 90, 255)'
    BUTTON_HOVER_COLOR = 'rgb(60, 20, 255)'

    def __init__(self, queue):
        super().__init__(None)
        self.setWindowTitle('Screenshot Reader')
        self.setup_ui()

        self.queue = queue

    def setup_ui(self):
        frame = QFrame()
        frame.setStyleSheet(f'background-color: {self.BACKGROUND_COLOR};')
        frame.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(5, 5, 5, 5)

        self.label = QLabel()
        self.btn_capture = QPushButton('Capture')
        self.btn_capture.setStyleSheet(
            (
                f'''
                    QFrame {{background-color: {self.BACKGROUND_COLOR};}}
                                    
                    QPushButton {{
                        border-radius: 5px;
                        background-color: {self.BUTTON_NORMAL_COLOR};
                        padding: 10px;
                        color: white;
                        font-weight: bold;
                        font-family: Arial;
                        font-size: 12px;
                    }}
                                    
                    QPushButton::hover {{background-color: {self.BUTTON_HOVER_COLOR}}}
                '''
            )
        )
        self.btn_capture.clicked.connect(self.capture)

        layout.addWidget(self.label)
        layout.addWidget(self.btn_capture)

        self.setCentralWidget(frame)

    def capture(self):
        self.capturer = Capture(self, self.queue)

        self.capturer.show()
