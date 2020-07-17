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
    name = "网格站点机房连线"

    def __init__(self, parent=None):
        super(Tab, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        label1 = QLabel("基站图层文件")
        editRadioPath = QLineEdit(self)
        editRadioPath.setDisabled(True)
        label1.setBuddy(editRadioPath)
        btnChooseRadio = QPushButton("选择")
        hbox1 = QHBoxLayout()
        hbox1.addWidget(label1)
        hbox1.addWidget(editRadioPath)
        hbox1.addWidget(btnChooseRadio)

        label2 = QLabel("机房图层文件")
        editCranPath = QLineEdit(self)
        editCranPath.setDisabled(True)
        label2.setBuddy(editCranPath)
        btnChooseCran = QPushButton("选择")
        hbox2 = QHBoxLayout()
        hbox2.addWidget(label2)
        hbox2.addWidget(editCranPath)
        hbox2.addWidget(btnChooseCran)

        label3 = QLabel("网格图层文件")
        editGridPath = QLineEdit(self)
        editGridPath.setDisabled(True)
        label3.setBuddy(editGridPath)
        btnChooseGrid = QPushButton("选择")
        hbox3 = QHBoxLayout()
        hbox3.addWidget(label3)
        hbox3.addWidget(editGridPath)
        hbox3.addWidget(btnChooseGrid)

        btnCalculate = QPushButton("连线")
        hbox4 = QHBoxLayout()
        hbox4.addStretch(1)
        hbox4.addWidget(btnCalculate)

        txtResult = QPlainTextEdit(self)
        txtResult.setReadOnly(True)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addWidget(txtResult)
        self.setLayout(vbox)

        btnCalculate.clicked.connect(self.calculate)
        btnChooseRadio.clicked.connect(self.chooseRadioFile)
        btnChooseCran.clicked.connect(self.chooseCranFile)
        btnChooseGrid.clicked.connect(self.chooseGridFile)

        self.editRadioPath = editRadioPath
        self.editCranPath = editCranPath
        self.editGridPath = editGridPath
        self.txtResult = txtResult

    def calculate(self):
        radioFileName = self.editRadioPath.text()
        cranFileName = self.editCranPath.text()
        gridFileName = self.editGridPath.text()
        if not (
            os.path.exists(radioFileName)
            and os.path.exists(cranFileName)
            and os.path.exists(gridFileName)
        ):
            QMessageBox.critical(None, "找不到文件", "请重新选择文件", QMessageBox.Ok)
            return

        out_kml = self.chooseOutKml()
        if not out_kml:
            QMessageBox.critical(None, "找不到文件", "请设置选择输出文件", QMessageBox.Ok)
            return

        self.txtResult.setPlainText("")
        QApplication.processEvents()
        try:
            QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            radio_points = loader.load_points(radioFileName)
            cran_points = loader.load_points(cranFileName)
            grids = loader.load_polygons(gridFileName)
            result = service.link_radio_cran(radio_points, cran_points, grids, out_kml)
            self.txtResult.setPlainText(result)
        except:
            msg = traceback.format_exc()
            QMessageBox.critical(None, "错误", msg, QMessageBox.Ok)
        finally:
            QApplication.restoreOverrideCursor()

    def chooseRadioFile(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "选择基站图层文件", "", "KML文件 (*.kml *.kmz)",
        )
        if fileName:
            self.editRadioPath.setText(fileName)

    def chooseCranFile(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "选择CRAN机房图层文件", "", "KML文件 (*.kml *.kmz)",
        )
        if fileName:
            self.editCranPath.setText(fileName)

    def chooseGridFile(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "选择多边形图层文件", "", "KML文件 (*.kml *.kmz)",
        )
        if fileName:
            self.editGridPath.setText(fileName)

    def chooseOutKml(self):
        fileName, _ = QFileDialog.getSaveFileName(
            self, "选择输出KML文件", "基站CRAN机房连线", "KML文件 (*.kml)",
        )
        return fileName
