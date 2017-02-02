#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback
import os.path
import ui_maindlg
import geo_tools

USING_PYQT = 5
try:
    from PyQt5 import QtWidgets
    from PyQt5 import QtCore
except ImportError:
    from PyQt4 import QtGui as QtWidgets
    from PyQt5 import QtCore
    USING_PYQT = 4


class MainDlg(QtWidgets.QTabWidget, ui_maindlg.Ui_mainDlg):
    def __init__(self, parent=None):
        super(MainDlg, self).__init__(parent)
        self.setupUi(self)

    def pointFileChosen(self):
        answer = QtWidgets.QFileDialog.getOpenFileName(self,
                                                       "Please choose the POINT file",
                                                       "",
                                                       "Keyhole Markup Language (*.kml *.kmz)",
                                                       None,
                                                       QtWidgets.QFileDialog.Options())
        if USING_PYQT == 5:
            fileName, _ = answer
        else:
            fileName = answer

        if fileName:
            self.txtPointFilePath.setText(fileName)

    def polygonFileChosen(self):
        answer = QtWidgets.QFileDialog.getOpenFileName(self,
                                                       "Please choose the POLYGON file",
                                                       "",
                                                       "Keyhole Markup Language (*.kml *.kmz)",
                                                       None,
                                                       QtWidgets.QFileDialog.Options())
        if USING_PYQT == 5:
            fileName, _ = answer
        else:
            fileName = answer

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
        answer = QtWidgets.QFileDialog.getOpenFileName(self,
                                                       "Please choose the POLYGON file",
                                                       "",
                                                       "Keyhole Markup Language (*.kml *.kmz)",
                                                       None,
                                                       QtWidgets.QFileDialog.Options())
        if USING_PYQT == 5:
            fileName, _ = answer
        else:
            fileName = answer

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
        answer = QtWidgets.QFileDialog.getOpenFileName(self,
                                                       "Please choose the POLYGON file",
                                                       "",
                                                       "Keyhole Markup Language (*.kml *.kmz)",
                                                       None,
                                                       QtWidgets.QFileDialog.Options())
        if USING_PYQT == 5:
            fileName, _ = answer
        else:
            fileName = answer
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
