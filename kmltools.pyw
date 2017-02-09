#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback
import os.path
import ui_maindlg
import geo_tools

from PyQt5 import QtWidgets
from PyQt5 import QtCore

class MainDlg(QtWidgets.QTabWidget, ui_maindlg.Ui_mainDlg):
    def __init__(self, parent=None):
        super(MainDlg, self).__init__(parent)
        self.setupUi(self)

    def pointFileChosen(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                       "Please choose the POINT file",
                                                       "",
                                                       "Keyhole Markup Language (*.kml *.kmz)",
                                                       None,
                                                       QtWidgets.QFileDialog.Options())

        if fileName:
            self.txtPointFilePath.setText(fileName)

    def polygonFileChosen(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                       "Please choose the POLYGON file",
                                                       "",
                                                       "Keyhole Markup Language (*.kml *.kmz)",
                                                       None,
                                                       QtWidgets.QFileDialog.Options())

        if fileName:
            self.txtPolygonFilePath.setText(fileName)

    def doCalculate(self):
        polygonFileName = self.txtPolygonFilePath.text()
        pointFileName = self.txtPointFilePath.text()
        if not (os.path.exists(polygonFileName) and os.path.exists(pointFileName)):
            QtWidgets.QMessageBox.critical(
                None,
                'File not found',
                'Please choose your input file',
                QtWidgets.QMessageBox.Ok)
            return

        self.txtResult.setPlainText("")
        QtWidgets.QApplication.processEvents()

        try:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            points, polygons = geo_tools.load_data(
                pointFileName, polygonFileName)
            result = geo_tools.points_inside_info(points, polygons)
            self.txtResult.setPlainText(result)
        except:
            msg = traceback.format_exc()
            QtWidgets.QMessageBox.critical(
                None,
                "Error",
                msg,
                QtWidgets.QMessageBox.Ok)
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    def areaFileChosen(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                       "Please choose the POLYGON file",
                                                       "",
                                                       "Keyhole Markup Language (*.kml *.kmz)",
                                                       None,
                                                       QtWidgets.QFileDialog.Options())

        if fileName:
            self.txtAreaFilePath.setText(fileName)

    def doCalculateArea(self):
        areaFileName = self.txtAreaFilePath.text()
        if not os.path.exists(areaFileName):
            QtWidgets.QMessageBox.critical(
                None,
                'File not found',
                'Please choose your input file',
                QtWidgets.QMessageBox.Ok)
            return

        self.txtAreaResult.setPlainText("")
        QtWidgets.QApplication.processEvents()

        try:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            polygons = geo_tools.load_polygons(areaFileName)
            result = geo_tools.calc_poly_areas(polygons)
            self.txtAreaResult.setPlainText(result)
        except:
            msg = traceback.format_exc()
            QtWidgets.QMessageBox.critical(
                None,
                "Error",
                msg,
                QtWidgets.QMessageBox.Ok)
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    def lineFileChosen(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                       "Please choose the POLYGON file",
                                                       "",
                                                       "Keyhole Markup Language (*.kml *.kmz)",
                                                       None,
                                                       QtWidgets.QFileDialog.Options())

        if fileName:
            self.txtLineFilePath.setText(fileName)

    def doCalculateLength(self):
        lineFileName = self.txtLineFilePath.text()
        if not os.path.exists(lineFileName):
            QtWidgets.QMessageBox.critical(
                None,
                'File not found',
                'Please choose your input file',
                QtWidgets.QMessageBox.Ok)
            return

        self.txtLengthResult.setPlainText("")
        QtWidgets.QApplication.processEvents()

        try:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            lines = geo_tools.load_lines(lineFileName)
            result = geo_tools.calc_line_length(lines)
            self.txtLengthResult.setPlainText(result)
        except:
            msg = traceback.format_exc()
            QtWidgets.QMessageBox.critical(
                None,
                "Error",
                msg,
                QtWidgets.QMessageBox.Ok)
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()


app = QtWidgets.QApplication(sys.argv)
dialog = MainDlg()
dialog.show()
app.exec_()
