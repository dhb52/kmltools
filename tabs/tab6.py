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

import geo_tools


class Tab(QWidget):
    name = "批量两点连线"

    def __init__(self, parent=None):
        super(Tab, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        label1 = QLabel("面图层文件")
        editExcelPath = QLineEdit(self)
        editExcelPath.setDisabled(True)
        label1.setBuddy(editExcelPath)
        btnChooseExcel = QPushButton("选择")
        hbox1 = QHBoxLayout()
        hbox1.addWidget(label1)
        hbox1.addWidget(editExcelPath)
        hbox1.addWidget(btnChooseExcel)

        btnGetTemplate = QPushButton("Excel模版")
        btnGenerate = QPushButton("生成")
        hbox2 = QHBoxLayout()
        hbox2.addWidget(btnGetTemplate)
        hbox2.addStretch(1)
        hbox2.addWidget(btnGenerate)

        txtResult = QPlainTextEdit(self)
        txtResult.setReadOnly(True)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(txtResult)
        self.setLayout(vbox)

        btnGetTemplate.clicked.connect(self.getTemplate)
        btnGenerate.clicked.connect(self.generate)
        btnChooseExcel.clicked.connect(self.chooseExcelFile)

        self.editExcelPath = editExcelPath
        self.txtResult = txtResult

    def generate(self):
        excelPath = self.editExcelPath.text()
        if not os.path.exists(excelPath):
            QMessageBox.critical(None, "找不到文件", "请重新选择文件", QMessageBox.Ok)
            return
        kmlPath, _ = QFileDialog.getSaveFileName(
            self, "保存为KML文件", "", "KML文件 (*.kml *.kmz)",
        )

        self.txtResult.setPlainText("")
        QApplication.processEvents()
        try:
            QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            geo_tools.link_points_kml(excelPath, kmlPath)
            self.txtResult.setPlainText("成功生成KML文件")
        except:
            msg = traceback.format_exc()
            QMessageBox.critical(None, "错误", msg, QMessageBox.Ok)
        finally:
            QApplication.restoreOverrideCursor()

    def chooseExcelFile(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "选择Excel文件", "", "Microsoft Excel File (*.xls *.xlsx)",
        )
        if fileName:
            self.editExcelPath.setText(fileName)

    def getTemplate(self):
        fileName, _ = QFileDialog.getSaveFileName(
            self, "选择Excel文件", "模版", "Microsoft Excel File (*.xlsx)",
        )
        if fileName:
            geo_tools.save_excel_template(fileName)
