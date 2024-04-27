from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QPushButton,
    QCheckBox,
)
from PyQt5.QtCore import Qt

from ScreenCapture.capture import Capture
from ScreenCapture.communicate import Communicate


class ScreenRegionSelector(QMainWindow):
    BACKGROUND_COLOR = 'rgb(63, 63, 63)'
    BUTTON_NORMAL_COLOR = 'rgb(60, 90, 255)'
    BUTTON_HOVER_COLOR = 'rgb(60, 20, 255)'
    BUTTON_DISABLED_COLOR = 'rgb(83, 83, 83)'

    def __init__(self, queue):
        super().__init__(None)
        self.setWindowTitle('Screenshot Reader')
        self.setup_ui()

        self.queue = queue

        self.et = None
        self.summarize = False

    def setup_ui(self):
        frame = QFrame()
        frame.setStyleSheet(f'background-color: {self.BACKGROUND_COLOR};')
        frame.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(5, 5, 5, 5)

        btn_stylesheet = f'''
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
                                        
                        

                        QLabel {{
                            border: 2px solid white;
                        }}
                    '''

        toggle_stylesheet = f'''
                            QPushButton::hover {{background-color: {self.BUTTON_HOVER_COLOR}}}
                                QPushButton::disabled {{background-color: {self.BUTTON_DISABLED_COLOR}}}
                                QCheckBox {{
                                    border: 2px solid white;
                                    border-radius: 5px;
                                    padding: 10px;
                                    color: white;
                                    font-weight: bold;
                                    font-family: Arial;
                                    font-size: 12px;
                                }}
                                QCheckBox::indicator:checked {{color: white;}}
                            '''

        self.label = QLabel()
        self.btn_read = QPushButton('Read')
        self.btn_repeat = QPushButton('Repeat')
        self.summarize_toggle = QCheckBox('Summarize')
        self.summarize_toggle.setCheckable(True)

        self.btn_read.setStyleSheet((btn_stylesheet))
        self.btn_repeat.setStyleSheet((btn_stylesheet))
        self.summarize_toggle.setStyleSheet(toggle_stylesheet)

        self.btn_read.clicked.connect(self.capture)
        self.btn_repeat.clicked.connect(self.repeat)
        self.summarize_toggle.clicked.connect(self.set_summarize)

        self.btn_read.setFixedSize(80, 40)
        self.btn_repeat.setFixedSize(80, 40)

        layout.addWidget(self.label)

        inner_layout = QHBoxLayout()
        inner_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(inner_layout)

        inner_layout.addWidget(self.btn_read)
        inner_layout.addWidget(self.btn_repeat)
        inner_layout.addWidget(self.summarize_toggle)

        self.btn_repeat.setEnabled(False)

        self.communicate = Communicate()
        self.communicate.changed.connect(self.enable_button_btn_repeat)

        self.setCentralWidget(frame)

    def capture(self):
        self.hide()  # Still shows up if the area captured overlaps with where the main window is located for some reason.
        self.capturer = Capture(self, self.queue)
        self.capturer.show()

    def repeat(self):
        if self.et is not None:
            self.queue.put(self.et)

    def enable_button_btn_repeat(self):
        if self.et is not None:
            self.btn_repeat.setEnabled(True)

    def set_summarize(self):
        self.summarize = not self.summarize
