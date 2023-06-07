#!/usr/bin/env python3
import os
import re
import sys
from collections import defaultdict
from enum import Enum
from pathlib import Path

# from PySide2.QtCore import QLoggingCategory
# from PySide2.QtGui import QGuiApplication, QIcon
from PySide2.QtGui import QIcon
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWebEngineWidgets import QWebEngineView
# from PySide2.QtWebEngine import QtWebEngine
# from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtWidgets import QApplication

import ress


class WSite(Enum):
    none = 0
    jupiter = 1
    hugo = 2
    python = 3
    youtube = 4


def windows_to_browser_path(path):
    path = path.replace("\\", "/")
    if len(path) > 1 and path[1] == ":":
        path = "file://" + path
    else:
        path = "file:///" + os.path.abspath(path)
    return path


def linux_to_browser_path(path):
    path = path.replace("\\", "/")
    path = "file://" + os.path.abspath(path)
    return path


def ifWebAddr(input_str: str) -> tuple:
    if input_str == "-tray":
        return False, WSite.none
    regex = r"^https?://(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}(?:/?|[/?]\S+)$|^(?:\d{1,3}\.){3}\d{1,3}$"
    print("parameter: " + input_str)
    if "localhost" in input_str or ":1313" in input_str or "127.0.0.1" in input_str:
        return True, WSite.hugo
    elif "youtube" in input_str:
        return True, WSite.youtube
    elif "8888" in input_str:
        return True, WSite.python
    elif "religionen.html" in input_str:
        return True, WSite.jupiter
    if re.match(regex, input_str):
        return True, WSite.jupiter
    else:
        return False, WSite.none


class MyAppEng(QQmlApplicationEngine):
    def __init__(self):
        super().__init__()
        self.rootContext().setContextProperty("MyAppEng", self)


def start():
    global wsite
    # QLoggingCategory.setFilterRules("*.error=true\n*.info=false\n*.warning=false")
    app = QApplication(sys.argv)
    # QtWebEngine.initialize()
    engine = MyAppEng()
    engine.rootContext().setContextProperty("MyAppEng", engine)
    engine.load(os.fspath(Path(__file__).resolve().parent / "main.qml"))
    w = engine.rootObjects()[0].children()[1]
    path_regex = re.compile(
        r'^[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$|^/([^/\0]+(/[^/\0]+)*)?$'
    )
    pfad = ""
    browser_path = "file:///home/alex/religionen.html?preselect=no_universal"
    tueb = 0
    wsite = WSite.none
    for path in sys.argv[1:]:
        ifRemote, which = ifWebAddr(path)
        if path_regex.match(path):
            pfad = path
        elif ifRemote:
            tueb = 1
            browser_path = path
        if which != WSite.none:
            wsite = which
    if pfad != "":
        windows_path_regex = re.compile(
            r'^[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$'
        )
        linux_path_regex = re.compile(r"^/.*$")
        if windows_path_regex.match(pfad):
            browser_path = windows_to_browser_path(pfad)
            tueb = 2
        elif linux_path_regex.match(pfad):
            browser_path = linux_to_browser_path(pfad)
            tueb = 3
        print("Browser-PATH: {}".format(browser_path))
    w.setProperty("url", browser_path)
    if not engine.rootObjects():
        sys.exit(-1)
    if "-tray" in sys.argv:
        engine.rootObjects()[0].setVisible(False)
    elif tueb == 0:
        print(
            "possible parameters: -tray\nAnd web addresses or filesystem adresses for windows or unix"
        )
    wsites = defaultdict(lambda: "Jupiter.png")
    wsites |= {
        WSite.hugo: "hugo.png",
        WSite.python: "python.png",
        WSite.jupiter: "Jupiter.png",
        WSite.none: "Jupiter.png",
        WSite.youtube: "youtube.png",
    }
    print(wsites[wsite] + " ist das Icon, durch: " + str(wsite))
    app.setWindowIcon(QIcon(":/" + wsites[wsite]))

    onexi = app.exec_()
    sys.exit(onexi)


# QT_LOGGING_RULES = "*.info=False;driver.usb.debug=True"
if __name__ == "__main__":
    # web_view = QWebEngineView()
    start()
