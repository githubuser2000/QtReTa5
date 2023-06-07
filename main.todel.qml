import QtQuick 2.13
import QtQuick.Controls 2.13
import QtWebEngine 1.1

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "WebEngine Example"

    WebEngineView {
        visible: true
        id: webView
        anchors.fill: parent
        url: "https://www.web.de"
    }
}
