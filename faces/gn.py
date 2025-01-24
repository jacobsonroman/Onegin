# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, QPointF, QEvent

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_images()
        self.display_current_image()

    def initUI(self):
        self.setWindowTitle("Onegin.ai")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.title_label = QLabel("Onegin.ai", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 40px; font-weight: bold;")

        self.view = QGraphicsView(self)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.viewport().installEventFilter(self)

        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.view)

        self.folder_path = r"C:\Users\JR\hair"
        self.images = []
        self.current_image_index = 0
        self.image_positions = []
        self.image_items = {}

        self.is_dragging = False
        self.last_mouse_pos = None

    def load_images(self):
        for filename in os.listdir(self.folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                img_path = os.path.join(self.folder_path, filename)
                img = QImage(img_path)
                pixmap = QPixmap.fromImage(img)
                self.images.append((filename, pixmap))
                self.image_positions.append(QPointF(self.view.width() // 2, self.view.height() // 2))

    def display_current_image(self):
        self.scene.clear()
        filename, pixmap = self.images[self.current_image_index]
        item = QGraphicsPixmapItem(pixmap)

        previous_position = self.image_positions[self.current_image_index]
        item.setPos(previous_position)
        
        self.scene.addItem(item)
        self.image_items[self.current_image_index] = item

    def wheelEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.zoom(event.angleDelta().y())
        else:
            if event.angleDelta().y() > 0:
                self.prev_image()
            else:
                self.next_image()

    def next_image(self):
        self.save_current_image_position()
        self.current_image_index += 1
        if self.current_image_index >= len(self.images):
            self.current_image_index = 0
        self.display_current_image()

    def prev_image(self):
        self.save_current_image_position()
        self.current_image_index -= 1
        if self.current_image_index < 0:
            self.current_image_index = len(self.images) - 1
        self.display_current_image()

    def save_current_image_position(self):
        item = self.image_items.get(self.current_image_index)
        if item:
            self.image_positions[self.current_image_index] = item.pos()

    def resizeEvent(self, event):
        self.center_images()

    def center_images(self):
        for i, pos in enumerate(self.image_positions):
            offset_x = self.view.width() // 2 - pos.x()
            offset_y = self.view.height() // 2 - pos.y()
            self.image_positions[i] = QPointF(self.view.width() // 2, self.view.height() // 2)
            if i in self.image_items:
                self.image_items[i].setPos(self.image_positions[i])

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.is_dragging = True
                self.last_mouse_pos = event.pos()
            return True
        elif event.type() == QEvent.MouseMove:
            if self.is_dragging and self.last_mouse_pos:
                delta = event.pos() - self.last_mouse_pos
                item = self.image_items.get(self.current_image_index)
                if item:
                    item.moveBy(delta.x(), delta.y())
                self.last_mouse_pos = event.pos()
            return True
        elif event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.LeftButton:
                self.is_dragging = False
                self.last_mouse_pos = None
                # Update the position of the image
                item = self.image_items.get(self.current_image_index)
                if item:
                    self.image_positions[self.current_image_index] = item.pos()
            return True
        return super().eventFilter(source, event)

    def zoom(self, delta):
        factor = 1.15 if delta > 0 else 0.85
        current_pos = self.view.mapToScene(self.view.viewport().rect().center())
        self.view.scale(factor, factor)
        new_pos = self.view.mapToScene(self.view.viewport().rect().center())
        delta_pos = new_pos - current_pos
        self.view.translate(delta_pos.x(), delta_pos.y())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())