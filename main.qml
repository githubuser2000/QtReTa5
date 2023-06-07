import QtQuick 2.13
import QtQuick.Controls 2.13
import Qt.labs.platform 1.1
import Qt.labs.platform 1.1 as LabsPlatform
import QtQuick.Window 2.13
import QtWebEngine 1.1
//import QtWebEngine 1.1
/*import QtQuick
import QtQuick.Controls
import QtWebEngine
import Qt.labs.platform*/

Window {
    width: 640
    height: 480
    visible: true
    title: "ReTa Icon"
    id : win
    visibility: "Maximized"
    flags: Qt.FramelessWindowHint
    WebEngineView {
        id : web
        visible: true
        anchors.fill: parent
        url: "https://www.bing.com/"
        anchors.centerIn: parent
        //onLoadingChanged : if (loadProgress === 100 )  MyAppEng.entf()
        onLoadingChanged : if (loadProgress === 100 )  tray.updateSystemTrayIcon()

    }
    LabsPlatform.SystemTrayIcon {
        visible: true
        icon.source: updateSystemTrayIcon();
        //icon.name: "QtReTa"
        //icon.mask: true
        //tooltip : qsTr("ReTa Icon")
        id : tray
        menu: Menu {
            MenuItem {
                text: qsTr("visible")
                onTriggered: {
                    win.visible = ! win.visible
                }
            }
            MenuItem {
                text: qsTr("Quit")
                onTriggered: Qt.quit()
            }
        }
        onActivated: {
            win.visible = ! win.visible
            updateSystemTrayIcon();
        }
        function updateSystemTrayIcon() {
            let addy = web.url.toString().substring(0, "http://127.0.0.1:1313/".length);
            let addy2 = web.url.toString().substring(0, "http://127.0.0.1/".length);
            let addy3 = web.url.toString().substring(0, "http://127.0.0.1:8888/".length);
            //console.log("Host-Adresse:", "http://127.0.0.1:1313/" == addy);
            //console.log("addy3 anfang:", addy3);
            //console.log("addy3 anfang:",  "http://127.0.0.1:8888/");
            if (addy2 == "http://127.0.0.1/" || addy == "http://127.0.0.1:1313/" || web.url.toString().includes(":1313")) {

                icon.source = "qrc:/hugo.png";
            } else
                if (addy3 == "http://127.0.0.1:8888/" || addy3 == "http://localhost:8888/") {
                    //console.log("addy3 ja:", addy3);
                    icon.source = "qrc:/python.png";
                } else
                    if (web.url.toString().includes("youtube")) {
                        //console.log("addy3 ja:", addy3);
                        icon.source = "qrc:/youtube.png";
                    } else {
                        //console.log("Icon ist Jupiter");
                        icon.source = "qrc:/Jupiter.png";
                    }
            return icon.source
        }
    }

}
