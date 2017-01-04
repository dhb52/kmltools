# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'maindlg.ui'
#
# Created: Sat Sep 17 15:55:50 2016
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtGui
from PyQt4 import QtCore
import sys  
import traceback
import os.path
import ui_maindlg  
import geo_tools
  
class MainDlg(QtGui.QTabWidget, ui_maindlg.Ui_mainDlg):  
    def __init__(self, parent=None):  
        super(MainDlg, self).__init__(parent)  
        self.setupUi(self)  

    def pointFileChosen(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
            "Please choose the POINT file",
            "",
            "Keyhole Markup Language (*.kml *.kmz)",
            None,
            QtGui.QFileDialog.Options())

        if fileName:
            self.txtPointFilePath.setText(fileName)

    def polygonFileChosen(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
            "Please choose the POLYGON file",
            "",
            "Keyhole Markup Language (*.kml *.kmz)",
            None,
            QtGui.QFileDialog.Options())
        if fileName:
            self.txtPolygonFilePath.setText(fileName)


    def doCalculate(self):
        polygonFileName = unicode(self.txtPolygonFilePath.text())
        pointFileName = unicode(self.txtPointFilePath.text())
        if not (os.path.exists(polygonFileName) and os.path.exists(pointFileName)):
            QtGui.QMessageBox.critical(
                None,
                'File not found', 
                'Please choose your input file',
                QtGui.QMessageBox.Ok)
            return            

        self.txtResult.setPlainText("")
        QtGui.QApplication.processEvents()

        try:
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            points, polygons  = geo_tools.load_data(pointFileName, polygonFileName)
            result = geo_tools.points_inside_info(points, polygons)
            self.txtResult.setPlainText(result)
        except:
            msg = traceback.format_exc()
            QtGui.QMessageBox.critical(
                None,
                "Error",
                msg,
                QtGui.QMessageBox.Ok)
        finally:
            QtGui.QApplication.restoreOverrideCursor()

    def areaFileChosen(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
            "Please choose the POLYGON file",
            "",
            "Keyhole Markup Language (*.kml *.kmz)",
            None,
            QtGui.QFileDialog.Options())
        if fileName:
            self.txtAreaFilePath.setText(fileName)        


    def doCalculateArea(self):
        areaFileName = unicode(self.txtAreaFilePath.text())
        if not os.path.exists(areaFileName):
            QtGui.QMessageBox.critical(
                None,
                'File not found', 
                'Please choose your input file',
                QtGui.QMessageBox.Ok)
            return

        self.txtAreaResult.setPlainText("")
        QtGui.QApplication.processEvents()
        
        try:
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            polygons = geo_tools.load_polygons(areaFileName)
            result = geo_tools.calc_poly_areas(polygons)
            self.txtAreaResult.setPlainText(result)        
        except:
            msg = traceback.format_exc()
            QtGui.QMessageBox.critical(
                None,
                "Error",
                msg,
                QtGui.QMessageBox.Ok)
        finally:
            QtGui.QApplication.restoreOverrideCursor()

    def lineFileChosen(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
            "Please choose the POLYGON file",
            "",
            "Keyhole Markup Language (*.kml *.kmz)",
            None,
            QtGui.QFileDialog.Options())
        if fileName:
            self.txtLineFilePath.setText(fileName)    


    def doCalculateLength(self):
        lineFileName = unicode(self.txtLineFilePath.text())
        if not os.path.exists(lineFileName):
            QtGui.QMessageBox.critical(
                None,
                'File not found', 
                'Please choose your input file',
                QtGui.QMessageBox.Ok)
            return

        self.txtLengthResult.setPlainText("")
        QtGui.QApplication.processEvents()

        try:
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            lines = geo_tools.load_lines(lineFileName)
            result = geo_tools.calc_line_length(lines)
            self.txtLengthResult.setPlainText(result)        
        except:
            msg = traceback.format_exc()
            QtGui.QMessageBox.critical(
                None,
                "Error",
                msg,
                QtGui.QMessageBox.Ok)
        finally:
            QtGui.QApplication.restoreOverrideCursor()
        

app = QtGui.QApplication(sys.argv)  
dialog = MainDlg()  
dialog.show()  
app.exec_()  
