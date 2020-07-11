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

from helpers import loader, service


class Tab(QWidget):
    name = "图层点提取"

    def __init__(self, parent=None):
        super(Tab, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        label1 = QLabel("点图层文件")
        editPointsPath = QLineEdit(self)
        editPointsPath.setDisabled(True)
        label1.setBuddy(editPointsPath)
        btnChoosePoints = QPushButton("选择")
        hbox1 = QHBoxLayout()
        hbox1.addWidget(label1)
        hbox1.addWidget(editPointsPath)
        hbox1.addWidget(btnChoosePoints)

        btnCalculate = QPushButton("提取")
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

        btnCalculate.clicked.connect(self.extract)
        btnChoosePoints.clicked.connect(self.choosePointsFile)

        self.editPointsPath = editPointsPath
        self.txtResult = txtResult

    def extract(self):
        pointFileName = self.editPointsPath.text()
        if not os.path.exists(pointFileName):
            QMessageBox.critical(None, "找不到文件", "请重新选择文件", QMessageBox.Ok)
            return

        self.txtResult.setPlainText("")
        try:
            QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            points = loader.load_points(pointFileName)
            result = service.points_to_csv(points)
            self.txtResult.setPlainText(result)
        except:
            msg = traceback.format_exc()
            QMessageBox.critical(None, "错误", msg, QMessageBox.Ok)
        finally:
            QApplication.restoreOverrideCursor()

    def choosePointsFile(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "选择点图层文件", "", "KML文件 (*.kml *.kmz)",
        )
        if fileName:
            self.editPointsPath.setText(fileName)
