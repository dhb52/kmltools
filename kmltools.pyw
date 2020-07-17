import sys

# pylint: disable=no-name-in-module
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

import rc_resource
from tabs import tab1, tab2, tab3, tab4, tab5, tab6, tab7


class MyTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(MyTabWidget, self).__init__(parent)
        self.setupUi()

    def addTabModual(self, moduals):
        for m in moduals:
            self.addTab(m.Tab(), m.Tab.name)

    def setupUi(self):
        self.addTabModual([tab1, tab2, tab3, tab4, tab4, tab5, tab6, tab7])


class MainDlg(QWidget):
    def __init__(self, parent=None):
        super(MainDlg, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        tabWidget = MyTabWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(tabWidget)

        labelCopyright = QLabel("© dinghaibin@gd.cmcc")
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(labelCopyright)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setWindowTitle("KML规划支撑工具")
        self.resize(800, 600)
        self.setWindowIcon(QIcon(":/app.ico"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = MainDlg()
    dialog.show()
    sys.exit(app.exec_())
