import sys
import os
import requests
import io
import cadquery as cq
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QFileDialog,
                             QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QMessageBox, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt
from PIL import Image
import utils

def get_next_filename(directory, prefix='model', extension='stl'):
    """Generate a unique filename with an incrementing number."""
    i = 1
    while True:
        filename = f"{prefix}_{i}.{extension}"
        if not os.path.exists(os.path.join(directory, filename)):
            return filename
        i += 1

class ImageProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Spotify Code to STL Converter')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #121212; color: #ffffff;")
        self.urlLabel = QLabel('Enter Spotify link:')
        self.urlLabel.setFont(QFont("Arial", 12, QFont.Bold))
        self.urlLabel.setAlignment(Qt.AlignCenter)
        self.urlLabel.setStyleSheet("QLabel {color: #ffffff;}")
        
        self.urlInput = QLineEdit(self)
        self.urlInput.setPlaceholderText('Insert link here...')
        self.urlInput.setStyleSheet("QLineEdit {background-color: #1f1f1f; color: #ffffff; padding: 5px; border-radius: 5px;}")

        self.messageLabel = QLabel('')
        self.messageLabel.setFont(QFont("Arial", 12))
        self.messageLabel.setStyleSheet("QLabel {color: #ffcc00;}")
        
        self.loadButton = self.createButton('Generate STL', self.generateSTL)
        self.openFolderButton = self.createButton('Open Folder', self.openFolder)
        self.openFolderButton.setEnabled(False)
        
        layout = QVBoxLayout()
        layout.addWidget(self.urlLabel)
        layout.addWidget(self.urlInput)
        layout.addWidget(self.messageLabel)
        layout.addWidget(self.loadButton)
        layout.addWidget(self.openFolderButton)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def createButton(self, text, func):
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #1f1f1f;
                color: #ffffff;
                border: 1px solid #ffffff;
                padding: 10px;
                margin: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2e2e2e;
            }
            QPushButton:pressed {
                background-color: #0d0d0d;
            }
        """)
        button.clicked.connect(func)
        return button

    def generateSTL(self):
        share_link = self.urlInput.text()
        
        if not share_link:
            self.showMessage("Please enter a valid Spotify link.")
            return
        
        data = utils.get_link_data(share_link)

        if len(data) != 2:
            self.showMessage("Something went wrong while parsing the URL.")
            return

        code_URL = f"https://www.spotifycodes.com/downloadCode.php?uri=jpeg%2F000000%2Fwhite%2F640%2Fspotify%3A{data[0]}%3A{data[1]}"
        r = requests.get(code_URL)

        if not r.ok or not r.content:
            self.showMessage("Something went wrong while fetching the Spotify code.")
            return

        try:
            img = Image.open(io.BytesIO(r.content)).crop((160, 0, 640-31, 160))
        except Exception as e:
            self.showMessage(f"Error loading image: {e}")
            return

        width, height = img.size
        pix = img.load()

        bar_heights = []
        max_height_of_single_bar = 0

        for x in range(width):
            at_bar = False
            curr_height = 0

            for y in range(height):
                if pix[x, y][0] > 20 or pix[x, y][1] > 20 or pix[x, y][2] > 20:
                    at_bar = True
                    curr_height += 1

            if at_bar and curr_height > max_height_of_single_bar:
                max_height_of_single_bar = curr_height / 20
            elif not at_bar and max_height_of_single_bar > 0:
                bar_heights.append(max_height_of_single_bar)
                max_height_of_single_bar = 0

        if not bar_heights:
            self.showMessage("No bars detected in the Spotify code image.")
            return

        models_dir = 'models'
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)

        try:
            model = cq.importers.importStep('base_model.step')
        except Exception as e:
            self.showMessage(f"Error importing base model: {e}")
            return

        curr_bar = 0

        for bar in bar_heights:
            model = (
                model.pushPoints([(15.5 + curr_bar * 1.88, 7.5)])
                .sketch()
                .slot(9 / 5 * bar, 1, 90)
                .finalize()
                .extrude(4)
            )
            curr_bar += 1

        filename = get_next_filename(models_dir, 'model', 'stl')

        try:
            cq.exporters.export(model, os.path.join(models_dir, filename))
        except Exception as e:
            self.showMessage(f"Error exporting model: {e}")
            return

        self.showMessage(f"File {filename} created successfully! The file is located in the models folder", success=True)
        self.openFolderButton.setEnabled(True)
        self.generatedFilePath = os.path.join(models_dir, filename)

    def openFolder(self):
        if hasattr(self, 'generatedFilePath'):
            os.startfile(os.path.dirname(self.generatedFilePath))

    def showMessage(self, message, success=False):
        if success:
            self.messageLabel.setStyleSheet("QLabel {color: #00ff00;}")
        else:
            self.messageLabel.setStyleSheet("QLabel {color: #ffcc00;}")
        self.messageLabel.setText(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageProcessor()
    ex.show()
    sys.exit(app.exec_())
