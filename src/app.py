import youtube_dl
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

ydl_opts = {}
WIDTH = 500
HEIGHT = 100


class ProcessRunnable(QRunnable):
    def __init__(self, target, args):
        QRunnable.__init__(self)
        self.t = target
        self.args = args

    def run(self):
        self.t(*self.args)

    def start(self):
        QThreadPool.globalInstance().start(self)


class GUI(QWidget):
    def __init__(self):
        global WIDTH, HEIGHT
        super().__init__()
        self.setWindowTitle('Youtube Downloader')
        self.setGeometry(0, 0, WIDTH, HEIGHT)
        self.setFixedSize(WIDTH, HEIGHT)

        self.create_grid()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        self.center()
        self.show()

    def create_grid(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QGridLayout()
        self.link = QTextEdit('', self)
        self.btn = QPushButton('Download', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.clicked.connect(self.download)
        self.extract = QCheckBox('Extract Audio')
        self.extract.setChecked(True)
        self.dir = QTextEdit('E:/Musik', self)
        layout.addWidget(self.link, 0, 0)
        layout.addWidget(self.btn, 0, 1)
        layout.addWidget(self.extract, 0, 2)
        layout.addWidget(self.dir, 0, 3)
        self.horizontalGroupBox.setLayout(layout)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def download(self):
        if self.extract.isChecked():
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        ProcessRunnable(target=self._download, args=()).start()

    def _download(self):
        with youtube_dl.YoutubeDL(ydl_opts) as dl:
            os.chdir(self.dir.toPlainText)
            try:
                dl.download(self.link.toPlainText().splitlines())
            except Exception as e:
                print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())
