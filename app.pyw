# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'maindlg.ui'
#
# Created: Sat Sep 17 15:55:50 2016
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtGui
from PyQt4 import QtCore
import sys  
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
            "Keyhole Markup Language (KML) (*.KML)",
            None,
            QtGui.QFileDialog.Options())

        if fileName:
            self.txtPointFilePath.setText(fileName)

    def polygonFileChosen(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
            "Please choose the POLYGON file",
            "",
            "Keyhole Markup Language (KML) (*.KML)",
            None,
            QtGui.QFileDialog.Options())
        if fileName:
            self.txtPolygonFilePath.setText(fileName)


    def doCalculate(self):
        self.txtResult.setPlainText("")
        QtGui.QApplication.processEvents()
        polygonFileName = self.txtPolygonFilePath.text()
        pointFileName = self.txtPointFilePath.text()
        geo_tools.load_data(pointFileName, polygonFileName)
        result = geo_tools.points_inside_info()
        self.txtResult.setPlainText(result)


    def areaFileChosen(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
            "Please choose the POLYGON file",
            "",
            "Keyhole Markup Language (KML) (*.KML)",
            None,
            QtGui.QFileDialog.Options())
        if fileName:
            self.txtAreaFilePath.setText(fileName)        


    def doCalculateArea(self):
        self.txtAreaResult.setPlainText("")
        QtGui.QApplication.processEvents()
        areaFileName = self.txtAreaFilePath.text()
        geo_tools.load_polygons(areaFileName)
        result = geo_tools.calc_poly_areas()
        self.txtAreaResult.setPlainText(result)        
        

app = QtGui.QApplication(sys.argv)  
dialog = MainDlg()  
dialog.show()  
app.exec_()  
