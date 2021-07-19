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
    name = "面积计算"

    def __init__(self, parent=None):
        super(Tab, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        label1 = QLabel("面图层文件")
        editPolygonsPath = QLineEdit(self)
        editPolygonsPath.setDisabled(True)
        label1.setBuddy(editPolygonsPath)
        btnChoosePolygons = QPushButton("选择")
        hbox1 = QHBoxLayout()
        hbox1.addWidget(label1)
        hbox1.addWidget(editPolygonsPath)
        hbox1.addWidget(btnChoosePolygons)

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
        btnChoosePolygons.clicked.connect(self.choosePolygonsFile)

        self.editPolygonsPath = editPolygonsPath
        self.txtResult = txtResult

    def calculate(self):
        polygonFileName = self.editPolygonsPath.text()
        if not os.path.exists(polygonFileName):
            QMessageBox.critical(self, "找不到文件", "请重新选择文件", QMessageBox.Ok)
            return

        self.txtResult.setPlainText("")
        QApplication.processEvents()
        try:
            QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            polygons = loader.load_polygons(polygonFileName)
            multi_polygons = loader.load_multi_polygons(polygonFileName)
            result = service.calc_polygons_area(polygons + multi_polygons)
            self.txtResult.setPlainText(result)
        except:
            msg = traceback.format_exc()
            QMessageBox.critical(self, "错误", msg, QMessageBox.Ok)
        finally:
            QApplication.restoreOverrideCursor()

    def choosePolygonsFile(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "选择多边形图层文件", "", "KML文件 (*.kml *.kmz)",
        )
        if fileName:
            self.editPolygonsPath.setText(fileName)
