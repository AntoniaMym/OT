
##    def voltage(self):
##        numberOfPoints = 100
##        self.samp_rate = numberOfPoints/self.period
##        
##        with nidaqmx.Task() as task:
##            task.ai_channels.add_ai_voltage_chan('Dev1/ai0') #primero lo lee el USB6008
##            task.timing.cfg_samp_clk_timing(self.samp_rate, samps_per_chan = numberOfPoints*2, sample_mode = AcquisitionType.CONTINUOUS)
##            task.start()
##            
##            n = 1
##            while True:
##                data = task.read(number_of_samples_per_channel = numberOfPoints)  #guarda los datos
##                n = n+1
##
##            task.stop()


        #CanalFisico = self.Canales.Channel.get()
##        self.Channel.insert("Dev1/ai0")
##
##        
##        maxVoltaje = int(self.Canales.maxVoltageEntry.get())
##        self.maxVoltageEntry.insert(0, "10")
##        
##        minVoltaje = int(self.Canales.minVoltageEntry.get())
##        self.minVoltageEntry.insert(0, "-10")
##        
##        sampleRate = int(self.Inputs.sampleEntry.get())
##        self.numberOfSamples = int(self.Inputs.numberOfSamplesEntry.get())
##
##
##        self.task = nidaqmx.Task()
##        self.task.ai_channels.add_ai_voltage_chan(physicalChannel, min_val=minVoltage, max_val=maxVoltage)
##        self.task.timing.cfg_samp_clk_timing(sampleRate,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,samps_per_chan=self.numberOfSamples*3)
##        self.task.start()
import pyflycap2 as pfc
import cv2
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

#ejemplo de video, nueva ventana

class ccd():

    def Image():
        path = "/ProgramData/Microsoft/Windows/Start Menu/Programs/Thorlabs/DCx Cameras"
        im_path= os.path.join(path)
        img = cv2.imread(img_path)
        #plt.imshow(img)
        recolor = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(recolor)
        plt.show()

    def Video():
        cap = cv2.VideoCapture(os.path.join())
        ret, frame = cap.read()
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.show()
        cap.release()
        cap.read()

        cap = cv2.VideoCapture(os.path.join('data','videos','coders.mp4'))
        # Loop through each frame
        for frame_idx in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
    
            # Read frame 
            ret, frame = cap.read()
    
            # Gray transform
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
            # Show image
            cv2.imshow('Video Player', gray)
    
            # Breaking out of the loop
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
##
##    # Close down everything
        cap.release()
        cv2.destroyAllWindows()
