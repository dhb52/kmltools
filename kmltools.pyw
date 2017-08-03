#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import os.path
import geo_tools

try:
    from PyQt5.QtWidgets import (
        QTabWidget, QFileDialog, QApplication, QMessageBox)
    from PyQt5 import QtCore
    PYQT_VER = 5

    def unicode(s):
        return s
    from ui_maindlg5 import Ui_mainDlg
except ImportError:
    from PyQt4.QtGui import (
        QTabWidget, QFileDialog, QApplication, QMessageBox)
    from PyQt4 import QtCore
    PYQT_VER = 4
    from ui_maindlg4 import Ui_mainDlg


def getOpenFileName(*args):
    if PYQT_VER == 5:
        fileName, _ = QFileDialog.getOpenFileName(*args)
        return fileName
    else:
        fileName = QFileDialog.getOpenFileName(*args)
        return fileName


class MainDlg(QTabWidget, Ui_mainDlg):

    def __init__(self, parent=None):
        super(MainDlg, self).__init__(parent)
        self.setupUi(self)

    def pointFileChosen(self):
        fileName = getOpenFileName(self,
                                   "Please choose the POINT file",
                                   "",
                                   "Keyhole Markup Language (*.kml *.kmz)")

        if fileName:
            self.txtPointFilePath.setText(fileName)

    def polygonFileChosen(self):
        fileName = getOpenFileName(self,
                                   "Please choose the POLYGON file",
                                   "",
                                   "Keyhole Markup Language (*.kml *.kmz)")

        if fileName:
            self.txtPolygonFilePath.setText(fileName)

    def doCalculate(self):
        polygonFileName = unicode(self.txtPolygonFilePath.text())
        pointFileName = unicode(self.txtPointFilePath.text())
        if not (os.path.exists(polygonFileName) and os.path.exists(pointFileName)):
            QMessageBox.critical(
                None,
                'File not found',
                'Please choose your input file',
                QMessageBox.Ok)
            return

        self.txtResult.setPlainText("")
        QApplication.processEvents()

        try:
            QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            points, polygons = geo_tools.load_data(
                pointFileName, polygonFileName)
            result = geo_tools.points_inside_info(points, polygons)
            self.txtResult.setPlainText(result)
        except:
            msg = traceback.format_exc()
            QMessageBox.critical(
                None,
                "Error",
                msg,
                QMessageBox.Ok)
        finally:
            QApplication.restoreOverrideCursor()

    def areaFileChosen(self):
        fileName = getOpenFileName(self,
                                   "Please choose the POLYGON file",
                                   "",
                                   "Keyhole Markup Language (*.kml *.kmz)")

        if fileName:
            self.txtAreaFilePath.setText(fileName)

    def doCalculateArea(self):
        areaFileName = unicode(self.txtAreaFilePath.text())
        if not os.path.exists(areaFileName):
            QMessageBox.critical(
                None,
                'File not found',
                'Please choose your input file',
                QMessageBox.Ok)
            return

        self.txtAreaResult.setPlainText("")
        QApplication.processEvents()

        try:
            QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            polygons = geo_tools.load_polygons(areaFileName)
            result = geo_tools.calc_poly_areas(polygons)
            self.txtAreaResult.setPlainText(result)
        except:
            msg = traceback.format_exc()
            QMessageBox.critical(
                None,
                "Error",
                msg,
                QMessageBox.Ok)
        finally:
            QApplication.restoreOverrideCursor()

    def lineFileChosen(self):
        fileName = getOpenFileName(self,
                                   "Please choose the POLYGON file",
                                   "",
                                   "Keyhole Markup Language (*.kml *.kmz)")

        if fileName:
            self.txtLineFilePath.setText(fileName)

    def doCalculateLength(self):
        lineFileName = unicode(self.txtLineFilePath.text())
        if not os.path.exists(lineFileName):
            QMessageBox.critical(
                None,
                'File not found',
                'Please choose your input file',
                QMessageBox.Ok)
            return

        self.txtLengthResult.setPlainText("")
        QApplication.processEvents()

        try:
            QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            lines = geo_tools.load_lines(lineFileName)
            result = geo_tools.calc_line_length(lines)
            self.txtLengthResult.setPlainText(result)
        except:
            msg = traceback.format_exc()
            QMessageBox.critical(
                None,
                "Error",
                msg,
                QMessageBox.Ok)
        finally:
            QApplication.restoreOverrideCursor()

    def areaIntersectionFileChosen(self):
        fileName = getOpenFileName(self,
                                   "Please choose the POLYGON file",
                                   "",
                                   "Keyhole Markup Language (*.kml *.kmz)")

        if fileName:
            self.txtAreaIntersectionFilePath.setText(fileName)

    def doCalculateAreaIntersection(self):
        areaFileName = unicode(self.txtAreaIntersectionFilePath.text())
        if not os.path.exists(areaFileName):
            QMessageBox.critical(
                None,
                'File not found',
                'Please choose your input file',
                QMessageBox.Ok)
            return

        self.txtAreaResult.setPlainText("")
        QApplication.processEvents()

        try:
            QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            polygons = geo_tools.load_polygons(areaFileName)
            result = geo_tools.calc_area_intersection_area(polygons)
            self.txtAreaIntersectionResult.setPlainText(result)
        except:
            msg = traceback.format_exc()
            QMessageBox.critical(
                None,
                "Error",
                msg,
                QMessageBox.Ok)
        finally:
            QApplication.restoreOverrideCursor()


def main():
    import sys

    app = QApplication(sys.argv)
    dialog = MainDlg()
    dialog.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
