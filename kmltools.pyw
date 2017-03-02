#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import os.path
import ui_maindlg
import geo_tools

from PyQt5.QtWidgets import (
    QTabWidget, QFileDialog, QApplication, QMessageBox)
from PyQt5 import QtCore


class MainDlg(QTabWidget, ui_maindlg.Ui_mainDlg):

    def __init__(self, parent=None):
        super(MainDlg, self).__init__(parent)
        self.setupUi(self)

    def pointFileChosen(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Please choose the POINT file",
                                                  "",
                                                  "Keyhole Markup Language (*.kml *.kmz)",
                                                  None,
                                                  QFileDialog.Options())

        if fileName:
            self.txtPointFilePath.setText(fileName)

    def polygonFileChosen(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Please choose the POLYGON file",
                                                  "",
                                                  "Keyhole Markup Language (*.kml *.kmz)",
                                                  None,
                                                  QFileDialog.Options())

        if fileName:
            self.txtPolygonFilePath.setText(fileName)

    def doCalculate(self):
        polygonFileName = self.txtPolygonFilePath.text()
        pointFileName = self.txtPointFilePath.text()
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
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Please choose the POLYGON file",
                                                  "",
                                                  "Keyhole Markup Language (*.kml *.kmz)",
                                                  None,
                                                  QFileDialog.Options())

        if fileName:
            self.txtAreaFilePath.setText(fileName)

    def doCalculateArea(self):
        areaFileName = self.txtAreaFilePath.text()
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
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Please choose the POLYGON file",
                                                  "",
                                                  "Keyhole Markup Language (*.kml *.kmz)",
                                                  None,
                                                  QFileDialog.Options())

        if fileName:
            self.txtLineFilePath.setText(fileName)

    def doCalculateLength(self):
        lineFileName = self.txtLineFilePath.text()
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


def main():
    import sys

    app = QApplication(sys.argv)
    dialog = MainDlg()
    dialog.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
