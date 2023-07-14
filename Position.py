import numpy as np
import nidaqmx
import time
import AOD

def Position(a,b,c,d,e,f,g,h,numberOfPoints):
    #FX,AX,FXmas,AXmas,FY,AY,FYmas,AYmas,numberOfPoints
    aod = AOD.aod()

    
    period = 1 #s
    samp_rate = numberOfPoints/period
    n = 0      #inicial
    time0 = time.time() #inicio toma de tiempo

    
    #ciclo para obtener puntos y asignar tareas    
    for n in range(numberOfPoints):
        #------------Path X------------
        FreqX = a[n] 
        AmpX = b[n]
        #------------MAS X-------------
        FreqXmas = c[n] #MHz
        AmpXmas = d[n]
        #------------task X------------
        FreqX_task = np.uint32(FreqX + FreqXmas)
        AmpX_task = AmpX 

        #------------Path Y------------
        FreqY = e[n]
        AmpY = f[n]
        #------------MAS Y-------------
        FreqYmas = g[n]  
        AmpYmas = h[n]
        #------------task Y------------
        FreqY_task = np.uint32(FreqY + FreqYmas)
        AmpY_task = AmpY

##        setXAmp = aod.setXAmp(AmpX_task)
##        setYAmp = aod.setYAmp(AmpY_task)
##        setXFreq = aod.setXFreq(FreqX_task)
##        setYFreq = aod.setYFreq(FreqY_task)
        setXAmp = aod.setXAmp(AmpX_task)
        setYAmp = aod.setYAmp(AmpY_task)
        setXFreq = aod.setXFreq(FreqX_task)
        setYFreq = aod.setYFreq(FreqY_task)


        #El NI lee toda las líneas, cuando le entrego un valor de la frecuencia
        #por lo que va a prender desde x2**8 hasta x2**31, si le entrego 60000
        #va a cortar los primeros 8 dígitos binarios.
        #finalmente la frecuencia efectiva será FreqY_task - (2**0+...+2**8)

        #print(FreqX_task)
        

##        with nidaqmx.Task() as task:
##            #Amp
##            #---X---
##            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line0:7')
##            #---Y---
##            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line0:7')
##            
##            #Freq
##            #---X---
##            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line8:31')
##            #---Y---
##            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line8:31')
##            
##            #Write Task
##            values = [AmpX_task, AmpY_task, FreqX_task, FreqY_task]
##            task.write(values)

        time.sleep(1/samp_rate)
        n = n + 1

    time1 = time.time()
    elapsedTime = time1 - time0
    effTimePerPoint = elapsedTime / n
    expTimePerPoint = 1/samp_rate
    print('elapsed time : %f, Time per Point : %f, exp Time PerPoint %f' %(elapsedTime, effTimePerPoint, expTimePerPoint))
    print('done')


def defaultPosition():
    FX0 = [AOD.aod.FX0]
    AX0 = [AOD.aod.AX0]
    FXmas0 = [0]
    AXmas0 = [0]
    
    FY0 = [AOD.aod.FY0]
    AY0 = [AOD.aod.AY0]
    FYmas0 = [0]
    AYmas0 = [0]

    numberOfPoints = 1
    
    Position(FX0,AX0,FXmas0,AXmas0,FY0,AY0,FYmas0,AYmas0,numberOfPoints)

    print('ready')
