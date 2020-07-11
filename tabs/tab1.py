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
    name = "点面计算"

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

        label2 = QLabel("面图层文件")
        editPolygonsPath = QLineEdit(self)
        editPolygonsPath.setDisabled(True)
        label2.setBuddy(editPolygonsPath)
        btnChoosePolygons = QPushButton("选择")
        hbox2 = QHBoxLayout()
        hbox2.addWidget(label2)
        hbox2.addWidget(editPolygonsPath)
        hbox2.addWidget(btnChoosePolygons)

        btnCalculate = QPushButton("计算")
        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(btnCalculate)

        txtResult = QPlainTextEdit(self)
        txtResult.setReadOnly(True)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addWidget(txtResult)
        self.setLayout(vbox)

        btnCalculate.clicked.connect(self.calculate)
        btnChoosePoints.clicked.connect(self.choosePointsFile)
        btnChoosePolygons.clicked.connect(self.choosePolygonsFile)

        self.editPointsPath = editPointsPath
        self.editPolygonsPath = editPolygonsPath
        self.txtResult = txtResult

    def calculate(self):
        pointFileName = self.editPointsPath.text()
        polygonFileName = self.editPolygonsPath.text()
        if not (os.path.exists(polygonFileName) and os.path.exists(pointFileName)):
            QMessageBox.critical(None, "找不到文件", "请重新选择文件", QMessageBox.Ok)
            return

        self.txtResult.setPlainText("")
        QApplication.processEvents()
        try:
            QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            points = loader.load_points(pointFileName)
            polygons = loader.load_polygons(polygonFileName)
            result = service.points_inside_info(points, polygons)
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

    def choosePolygonsFile(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "选择多边形图层文件", "", "KML文件 (*.kml *.kmz)",
        )
        if fileName:
            self.editPolygonsPath.setText(fileName)
