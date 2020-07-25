import os
import traceback

# pylint: disable=no-name-in-module
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core import loader, service


class Tab(QWidget):
    name = "长度计算"

    def __init__(self, parent=None):
        super(Tab, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        label1 = QLabel("线图层文件")
        editLinesPath = QLineEdit(self)
        editLinesPath.setDisabled(True)
        label1.setBuddy(editLinesPath)
        btnChooseLines = QPushButton("选择")
        hbox1 = QHBoxLayout()
        hbox1.addWidget(label1)
        hbox1.addWidget(editLinesPath)
        hbox1.addWidget(btnChooseLines)

        btnCalculate = QPushButton("计算")
        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(btnCalculate)

        txtResult = QPlainTextEdit(self)
        txtResult.setReadOnly(True)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(txtResult)
        self.setLayout(vbox)

        btnCalculate.clicked.connect(self.calculate)
        btnChooseLines.clicked.connect(self.chooseLinesFile)

        self.editLinesPath = editLinesPath
        self.txtResult = txtResult

    def calculate(self):
        lineFileName = self.editLinesPath.text()
        if not os.path.exists(lineFileName):
            QMessageBox.critical(self, "找不到文件", "请重新选择文件", QMessageBox.Ok)
            return

        self.txtResult.setPlainText("")
        QApplication.processEvents()

        try:
            QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            lines = loader.load_lines(lineFileName)
            result = service.calc_lines_length(lines)
            self.txtResult.setPlainText(result)
        except:
            msg = traceback.format_exc()
            QMessageBox.critical(self, "错误", msg, QMessageBox.Ok)
        finally:
            QApplication.restoreOverrideCursor()

    def chooseLinesFile(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "选择线图层文件", "", "KML文件 (*.kml *.kmz)",
        )
        if fileName:
            self.editLinesPath.setText(fileName)
