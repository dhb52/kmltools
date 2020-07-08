#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback
import os.path
import geo_tools

# pylint: disable
from PyQt5.QtWidgets import QTabWidget, QFileDialog, QApplication, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon

from ui_maindlg5 import Ui_MainDlg

import rc_resource


class MainDlg(QTabWidget, Ui_MainDlg):
    def __init__(self, parent=None):
        super(MainDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/app.ico"))

    def pointFileChosen(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "选择点图层文件", "", "KML文件 (*.kml *.kmz)",
        )
        if fileName:
            self.txtPointFilePath.setText(fileName)

    def polygonFileChosen(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "选择多边形图层文件", "", "KML文件 (*.kml *.kmz)",
        )
        if fileName:
            self.txtPolygonFilePath.setText(fileName)

    def pointsOutFileChosen(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "选择多边形图层文件", "", "KML文件 (*.kml *.kmz)",
        )
        if fileName:
            self.txtPointsOutFilePath.setText(fileName)

    def doCalculate(self):
        polygonFileName = self.txtPolygonFilePath.text()
        pointFileName = self.txtPointFilePath.text()
        if not (os.path.exists(polygonFileName) and os.path.exists(pointFileName)):
            QMessageBox.critical(None, "找不到文件", "请重新选择文件", QMessageBox.Ok)
            return

        self.txtResult.setPlainText("")
        QApplication.processEvents()

        try:
            QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            points, polygons = geo_tools.load_data(pointFileName, polygonFileName)
            result = geo_tools.points_inside_info(points, polygons)
            self.txtResult.setPlainText(result)
        except:
            msg = traceback.format_exc()
            QMessageBox.critical(None, "错误", msg, QMessageBox.Ok)
        finally:
            QApplication.restoreOverrideCursor()

    def areaFileChosen(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "选择多边形图层文件", "", "KML文件 (*.kml *.kmz)",
        )
        if fileName:
            self.txtAreaFilePath.setText(fileName)

    def doCalculateArea(self):
        areaFileName = self.txtAreaFilePath.text()
        if not os.path.exists(areaFileName):
            QMessageBox.critical(None, "找不到文件", "请重新选择文件", QMessageBox.Ok)
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
            QMessageBox.critical(None, "错误", msg, QMessageBox.Ok)
        finally:
            QApplication.restoreOverrideCursor()

    def lineFileChosen(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "选择连线的图层文件", "", "KML文件 (*.kml *.kmz)",
        )
        if fileName:
            self.txtLineFilePath.setText(fileName)

    def doCalculateLength(self):
        lineFileName = self.txtLineFilePath.text()
        if not os.path.exists(lineFileName):
            QMessageBox.critical(None, "找不到文件", "请重新选择文件", QMessageBox.Ok)
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
            QMessageBox.critical(None, "错误", msg, QMessageBox.Ok)
        finally:
            QApplication.restoreOverrideCursor()

    def areaIntersectionFileChosen(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "选择多边形图层文件", "", "KML文件 (*.kml *.kmz)",
        )
        if fileName:
            self.txtAreaIntersectionFilePath.setText(fileName)

    def doCalculateAreaIntersection(self):
        areaFileName = self.txtAreaIntersectionFilePath.text()
        if not os.path.exists(areaFileName):
            QMessageBox.critical(None, "找不到文件", "请重新选择文件", QMessageBox.Ok)
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
            QMessageBox.critical(None, "错误", msg, QMessageBox.Ok)
        finally:
            QApplication.restoreOverrideCursor()

    def doOutputPoints(self):
        pointsFileName = self.txtPointsOutFilePath.text()
        if not os.path.exists(pointsFileName):
            QMessageBox.critical(None, "找不到文件", "请重新选择文件", QMessageBox.Ok)
            return

        self.txPointOutResult.setPlainText("")
        try:
            QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            points = geo_tools.load_points(pointsFileName)
            result = geo_tools.points_to_csv(points)
            self.txPointOutResult.setPlainText(result)
        except:
            msg = traceback.format_exc()
            QMessageBox.critical(None, "错误", msg, QMessageBox.Ok)
        finally:
            QApplication.restoreOverrideCursor()


def main():
    app = QApplication(sys.argv)
    dialog = MainDlg()
    dialog.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
