from PyQt5.QtWidgets import QWidget, QApplication, QRubberBand
from PyQt5.QtGui import QMouseEvent, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect, QBuffer, QIODevice, QByteArray
from PIL import Image

import pytesseract
import io

pytesseract.pytesseract.tesseract_cmd = r'.//Tesseract//tesseract.exe'


class Capture(QWidget):
    CROSS_CURSOR = Qt.CrossCursor
    PNG_FORMAT = 'PNG'
    DEFAULT_LANGUAGE = 'eng'

    def __init__(self, main_window, queue):
        super().__init__()
        self.main = main_window
        # self.main.hide()

        self.setup_ui()

        self.queue = queue

    def setup_ui(self):
        self.setMouseTracking(True)
        desk_size = QApplication.desktop()
        self.setGeometry(0, 0, desk_size.width(), desk_size.height())
        self.setWindowFlags(
            self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
        self.setWindowOpacity(0.15)

        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()

        QApplication.setOverrideCursor(Capture.CROSS_CURSOR)
        self.imgmap = self.grab_screen()

    def grab_screen(self):
        screen = QApplication.primaryScreen()
        rect = QApplication.desktop().rect()
        return screen.grabWindow(
            QApplication.desktop().winId(),
            rect.x(),
            rect.y(),
            rect.width(),
            rect.height(),
        )

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
            self.rubber_band.show()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if not self.origin.isNull():
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            cropped_image = self.process_captured_image()

            self.pixmap_to_string(cropped_image)

            self.main.label.setPixmap(cropped_image)
            self.main.show()

            QApplication.restoreOverrideCursor()

            self.close()

    def process_captured_image(self):
        rect = self.rubber_band.geometry()

        cropped_image = self.imgmap.copy(rect)

        clipboard = QApplication.clipboard()
        clipboard.setPixmap(cropped_image)

        return cropped_image

    def pixmap_to_string(self, pixmap):
        png_data = self.pixmap_to_png(pixmap)

        et = self.extract_text(png_data)

        et_without_dashes = et.replace('-\n', '')
        et_without_linebreaks = et_without_dashes.replace('\n', ' ')

        self.queue.put(et_without_linebreaks)

    def pixmap_to_png(self, pixmap: QPixmap) -> QByteArray:
        buffer = QBuffer()
        buffer.open(QIODevice.WriteOnly)
        pixmap.save(buffer, Capture.PNG_FORMAT)
        png_data = buffer.data()
        buffer.close()
        return png_data

    def extract_text(self, png_data: QByteArray) -> str:
        try:
            image = Image.open(io.BytesIO(png_data))
            return pytesseract.image_to_string(image, lang=Capture.DEFAULT_LANGUAGE)
        except Exception as e:
            print(f'Error extracting text: {e}')
            return ''
