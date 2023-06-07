import sys

# from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
# from PySide2.QtWebEngine import QtWebEngine
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WebEngineView Example")
        self.setGeometry(100, 100, 800, 600)

        self.webview = QWebEngineView(self)
        self.webview.load("https://www.youtube.com")
        self.setCentralWidget(self.webview)


# sys.exit(app.exec_())
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
