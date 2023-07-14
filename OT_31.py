from PyQt5.uic import loadUi
from PyQt5.QtSql import *
from PyQt5.QtWidgets import*
from PyQt5.QtCore import Qt, QModelIndex
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pyqtgraph.exporters # needed to save platted data
import sys  # We need sys so that we can pass argv to QApplication
import os
import nidaqmx
from nidaqmx.constants import LineGrouping
from nidaqmx.stream_writers import DigitalMultiChannelWriter
import numpy as np
from datetime import datetime
import csv
import time
import threading
import matplotlib.pyplot as plt
from nidaqmx.stream_writers import CounterWriter
from nidaqmx.constants import AcquisitionType
from nidaqmx.types import CtrTime
import ctypes
from nidaqmx._lib import lib_importer, ctypes_byte_str
from nidaqmx.errors import check_for_error
from nidaqmx._task_modules.channels.do_channel import DOChannel
from nidaqmx._task_modules.channel_collection import ChannelCollection
from nidaqmx.utils import unflatten_channel_string
from array import array
import pyflycap2 as pfc
import cv2

import Position
import AOD
import Funciones
import CCD
#Nidaqmx reference help
#https://nidaqmx-python.readthedocs.io/en/latest/

#PyQt reference help
#https://www.tutorialspoint.com/pyqt/pyqt_basic_widgets.htm

#Number of steps for entire range: 85300

#Adquisición de datos

#Interfaz con Qt Designer

class Control(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Control, self,).__init__(*args, **kwargs)
        loadUi("opticalTweezers.ui", self)

        self.initUI()

    def initUI(self):
        
        self.launch = False

    #Widgets
        self.centralwidget = QWidget(self)
        line = QLineEdit(self)

        self.Datos = QGroupBox()
        self.Canales = QFrame(self)
        self.Inputs = QFrame(self)
        self.graphDataFrame = QGraphicsView()
        
        #GraphicsView
        self.QPD

        #OpenWidget
        self.open = QOpenGLWidget
        self.CCD
               
        #tabla
        self.tabla = QTableWidget()

        #progress bar
        self.progressBar = QProgressBar()

        #label
        self.label.setText("Presiona Run Test para comenzar")

        #button
        self.buttonRunTest.clicked.connect(self.test)
        self.buttonStop.clicked.connect(self.Stop)
        self.buttonFin.clicked.connect(self.Finalizar)
        self.Default.clicked.connect(Position.defaultPosition)

        #lcd
        self.lcd = QLCDNumber()
        self.lcdX
        self.lcdAngX
        self.lcdY
        self.lcdAngY

        self.lcdFactor
        self.lcdFactor1

        #TextEdit
        self.txt = QTextEdit()
        self.textFreqX   #valor de la frecuencia
        self.textFreqY
        self.textAmpX
        self.textAmpY

##        self.textFreqX.textChanged.connect(self.onChangeText)
        

        self.Channel
        self.maxVoltageEntry
        self.minVoltageEntry
        self.numberOfSamples
        self.sampleRate

        #LineEdit
        self.lineFreqX = line
        
        #List
        self.list = QListWidget()
        self.listMove

        #ToolButton
        self.verMas = QToolButton()
        self.VerMasLuz
        self.VerMasDatos
        
        #checkBox
        self.checkBox = QCheckBox()
        self.State = self.checkBox.checkState()
        print(self.lineFreqX.text())

        #llamar AOD
        #self.aod = aod()

        
##    def Progeso(self):
##        self.contador = 0
##
##        while self.contador <= 100:
##            time.sleep(1)
##            self.progressBar.setValue(self.contador)
##            self.contador += 10

            #podrìa entegar diectamente el tiempo por punto y cuànto tardò en total
##    def onChangeText(self):
##        freqX = self.textFreqX.text()
##        print(freqX)


    def onClicked(self):
        #self.checkBox1_1.isChecked() == True
        #self.aod = aod()
        AOD.aod.initialize()
        
    #Mensaje cuando se selecciona botón. Se genera un cambio después de la acción  
    def Stop(self):
        
        continuar = True
        while continuar:
            
            if self.buttonStop.clicked():
                
                self.label.setText("Seleccionaste Stop")
                

                #nùmero impar de veces
                continuar = False

            else:
                #nùmero par
                self.buttonStop.clicked()
                pass
        
    def RunTest(self):
        self.label.setText("Seleccionaste Run Test")
        self.buttonRunTest.clicked.connect(self.test)      
        
    def Finalizar(self):
        self.label.setText("Seleccionaste Finalizar")
        if self.launch:
            print('en proceso')
            self.lauch = False
        self.clear()
        self.close()
        print('fin')

        #self.close()

    def Barra_numbers(self):
        print('running')
        'action #1 that takes a lot of time '
        'action #2 that also takes a lot of time'

        for n in range(101):
            if self.launch:
                self.pogressBar.setValue(n)
                time.sleep(0.01)
                QtCore.QCoreApplication.processEvents()
  
    def __getitem__(self,key):
        return getattr(self,key)

    def __setitem__(self, i, elem):
        setattr(self,i,elem)

    def initialize(self):
        AOD.aod.initialize()
        
        MA = AOD.aod.MA()
    
    def getPoints(self):
        #Obtener puntos desde Path
        Path = AOD.aod.Path(self)
        PathX = Path
        PathY = Path
        pointsAX = PathX[0]
        pointsFX = PathX[1]
        pointsAY = PathY[2]
        pointsFY = PathY[3]

        return pointsAX , pointsFX , pointsAY , pointsFY
   
    def PointsOfMas(self):
        #Obtener puntos desde MA
        MasX = AOD.aod.MA(self)
        MasY = AOD.aod.MA(self)
        pMasAX = MasX[0]
        pMasFX = MasX[1]
        pMasAY = MasY[2]
        pMasFY = MasY[3]

        return pMasAX, pMasFX, pMasAY, pMasFY


    def test(self):
        print('test')
        self.RunTest()
        #self.Barra_numbers()

        
        #parameters
        self.period = 1 #seg 
        line = Funciones.potencia(2,31)
        
        #get point array
        pointsAX , pointsFX , pointsAY , pointsFY = self.getPoints()
        pMasAX, pMasFX, pMasAY, pMasFY = self.PointsOfMas()
        AOD.aod.Path(self)
        
        FX = pointsFX
        AX = pointsAX 
        FXmas = pMasFX
        AXmas = pMasAX
        FY = pointsFY
        AY = pointsAY
        FYmas = pMasFY
        AYmas = pMasAY
        
        Position.Position(FX,AX,FXmas,AXmas,FY,AY,FYmas,AYmas,self.numberOfPoints)

    def clear(self):
        os.system('cls')


app = QApplication([])

window = Control()
window.show()
app.exec_()

