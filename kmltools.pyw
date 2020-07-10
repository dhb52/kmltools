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
from tabs import tab1, tab2, tab3, tab4, tab5, tab6


class MyTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(MyTabWidget, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.addTab(tab1.Tab(), tab1.Tab.name)
        self.addTab(tab2.Tab(), tab2.Tab.name)
        self.addTab(tab3.Tab(), tab3.Tab.name)
        self.addTab(tab4.Tab(), tab4.Tab.name)
        self.addTab(tab5.Tab(), tab5.Tab.name)
        self.addTab(tab6.Tab(), tab6.Tab.name)


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
