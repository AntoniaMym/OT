import numpy as np
import Funciones as fun
import nidaqmx

#-------------OUTPUT---------------#
class aod:
    FX0 = 75        #MHz
    factor = 0.3
    FY0 = 75  
    FXmax = 90  
    FXmin = 60  
    FYmax = 90  
    FYmin = 60  
    AX0 = 1
    AY0 = 1  #buscar unidades en matlab
    numberOfPoints = 100
    

    def Path(self):
        dxfreq = 60    #MHz
        dxamp = 1      #microm
        dyfreq = 60
        dyamp = 1

        xfreq = dxfreq
        xamp = dxamp
        yfreq = dyfreq
        yamp = dyamp

        freqBits = 23
        ampBits = 8
        freqMax = 500  #MHz
        ampMax = 1
        
        
        xfreqStep = 0.06 #MHz
        yfreqStep = 0.06 #MHz
        #xfreqStep = 0.5
        #yfreqStep = 0.5


        Buffer = 62                           #velocidad Sample cambia?
        TimeOut = 10 ** 6                     #microseg          

        deltaFreq = freqMax / (2**(freqBits)) #revisar fraqmax/mayorNumeroposible notar que freq està en MHz
        deltaAmp = ampMax / (2**(ampBits)-1)  #amp en microm
 

        #print(deltaFreq)                     #5.9 e-05.... 4.76 en MHz
        #print(deltaAmp)                      #0.0392

        Xfreq = np.arange(60,90,xfreqStep)  
        Yfreq = np.arange(60,90,yfreqStep)

        Xamp = np.arange(0,2,deltaAmp)
        Yamp = np.arange(0,2,deltaAmp)

        deltaT = 1/deltaFreq
        #print(deltaT)  #microSeg 16777.216

        TimeMin = 0

        dT = np.arange(TimeMin,TimeOut,deltaT)
        #oscLim = 250
           
        pX0 = 0
        pXmin = -50  #micrometros
        pXmax = 50
        self.numberOfPoints = 100
        pX = np.linspace(pXmin , pXmax, self.numberOfPoints)  #100 puntos, a elección
        
        pY0 = 0
        pYmin = -50  #micrometros
        pYmax = 50
        pY = np.linspace(pYmin , pYmax, self.numberOfPoints)

        #Posiciòn a Frecuencia    
        def ToFreq():
            FX0 = aod.FX0
            FY0 = aod.FY0
            FXmax = aod.FXmax
            FYmax = aod.FYmax
            FXmin = aod.FXmin
            FYmin = aod.FYmin
            factor = aod.factor

            '''posiciòn a frecuencia'''
            
            fX = FX0 + factor * pX
            fX[fX>FXmax] = FXmax
            fX[fX<FXmin] = FXmin
            
            fY = FY0 + factor * pY
            fY[fY>FYmax] = FYmax
            fY[fY<FYmin] = FYmin
            return 'X a Freq:', fX,'Y a Freq:', fY    
                
        aFreq = ToFreq()
        #print(aFreq)
        #PathFreqX = np.round(aFreq[1])
        PathFreqX = aFreq[1]
##        PathFreqY = np.round(aFreq[3])
        PathFreqY = aFreq[3]
        
        #pFreqBinX = list(map(fun.abinario,PathFreqX)) #info que se debe enviar
        #pFreqBinX = list(map(bin(),PathFreqX))
        #pFreqBinX = bin(PathFreqX)
        #print(pFreqBinX)
        #pFreqBinY = list(map(fun.abinario,PathFreqY)) #info a enviar

        #vecesX = len(pFreqBinX)                   #100
        #vecesY = len(pFreqBinY)


        pAmpX = [xamp]*self.numberOfPoints #fijo
        pAmpY = [yamp]*self.numberOfPoints#info a enviar
        #pAmpBinY = [1]*vecesY                     #info a enviar
        #pAmpX =1
        #pAmpY =1


        path = [pAmpX, PathFreqX, pAmpY, PathFreqY]

        return path

    #MA: Movimiento Armónico
    def MA(self):
        def MovArmonico(t0):
            MAx = 0
            MAy = 0
            #MAfreq = 5                         #rev
            MAfreq = 1                          #Hz
            MAphase = 90                        #para x empieza en AmpMax, para y empieza en 0
            MAxAmp = 2
            MAyAmp = 2
            MApuntos = 100
            periodo = 1 / MAfreq                #s, cada 1s da una vuelta completa

            t = t0 + np.linspace(0,1,MApuntos)  #intervalos de 0.02 s

            
            pX = MAxAmp * np.cos(2 * np.pi* MAfreq * t + MAphase)
            pY = MAyAmp * np.sin(2 * np.pi* MAfreq * t + MAphase)
            return 'posición X:', pX, 'posición Y:', pY
        

        MAS = MovArmonico(0) #esto va en orden 1freq, 1dT  2freq,2dT...
        Px = MAS[1]          # entrega la posiciòn en x dependiente de dt
        Py = MAS[3]          # '' en y ''
        #print(MAS)


#De Posición a Frecuencia
        def PosToFreq(x,y):
            #factor = 0.3 #en inicio, comprobar
            FX0 = aod.FX0
            FY0 = aod.FY0
            FXmax = aod.FXmax
            FYmax = aod.FYmax
            FXmin = aod.FXmin
            FYmin = aod.FYmin
            factor = aod.factor
            
            FX = FX0 + factor * x
            FY = FY0 + factor * y
#encontrar el factor in '100 x 100 micro' depende experimental
#extremos accesibles por aod, dev 50 x = 50 feq = 90, x=-50 feq = 90
#90-60/100 = 0.3
            FX[FX>FXmax] = FXmax
            FX[FX<FXmin] = FXmin
            FY[FY>FYmax] = FYmax
            FY[FY<FYmin] = FYmin
            return FX, FY
        Freq = PosToFreq(Px,Py)
        masFreqX = np.round(Freq[0])
        masFreqY = np.round(Freq[1])
        
        masAmpX = [(2)] * len(masFreqX)
        masAmpY = [(2)] * len(masFreqX)

        masFreqBinX = list(map(fun.abinario,masFreqX))
        masFreqBinY = list(map(fun.abinario,masFreqY))

        masAmpBinX = [fun.abinario(2)] * len(masFreqX)
        masAmpBinY = [fun.abinario(2)] * len(masFreqX)
        

        mas = [masAmpX, masFreqX, masAmpY, masFreqY]
        
        #Revisar porque el rango de freq no oscila mucho: 2 números bin (muy poco?)

        t = np.linspace(0,1,50)
        
        MovArmonico(0)     
        PosToFreq(Px,Py)

        return mas


    def initialize(self):

        #construct digital words , ref : SendToArduino

        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line0:31')
            port0 = 0
            task.write(port0)
            task.start()

    
##    def setXAmp(self,a):
##        #a: decimal value varying between 0 and 1
##        #Vpp, Vmax = 5 volts
##        #Power = Vpp^2/8R = Vpp^2/400 (R= 50 Ohms) , Pmax = 25/400 = 100/1600 = 1/16 Watts
##        #Pmax = 62.5 mW
##        #Maximum Power for ADO 2W, tested with 1,7 Watts
##        with nidaqmx.Task() as task:
##            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line0:7')
##            task.write(np.uint32(a*255))
##
##    def setYAmp(self,a):
##        with nidaqmx.Task() as task:
##            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line0:7')
##            task.write(np.uint32(a*255))
##        
##    def setXFreq(self,f):
##        #f: decimal value varying between 60 and 90 MHz
##        # tested between 59.5 and 89.5 MHz
##        # 23 bits
##        # F(MHz) = N x 500 / 2**23
##        #Vpp, Vmax = 5 volts
##        #Power = Vpp^2/8R = Vpp^2/400 (R= 50 Ohms) , Pmax = 25/400 = 100/1600 = 1/16 Watts
##        #Pmax = 62.5 mW
##        #Maximum Power for ADO 2W, tested with 1,7 Watts
##        N = np.uint32(2**8 * f*(2**(23))/(500))
##        #N = np.uint32(f*(2**(23))/(500))  #revisar
##        print(bin(N))
##        with nidaqmx.Task() as task:
##            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line8:31')
##            task.write(N)
##
##    def setYFreq(self,f):
##        N = np.uint32(2**8 * f*(2**(23))/(500))
##        print(bin(N))
##        with nidaqmx.Task() as task:
##            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line8:31')
##            task.write(N)

    def setXAmp(self,a):
        #a: decimal value varying between 0 and 1
        #Vpp, Vmax = 5 volts
        #Power = Vpp^2/8R = Vpp^2/400 (R= 50 Ohms) , Pmax = 25/400 = 100/1600 = 1/16 Watts
        #Pmax = 62.5 mW
        #Maximum Power for ADO 2W, tested with 1,7 Watts
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line0:7')
            task.write(np.uint32(a*255))

    def setYAmp(self,a):
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line0:7')
            task.write(np.uint32(a*255))

    def NtoTask(self,N):
        
        binN1 = bin(N)
        binN2 = binN1.replace("b","0")
        zeros = "0"*23
        binN = zeros + binN2
        fin = len(binN)
        
        n0 = np.uint32(binN[fin-1:fin])
        n1 = np.uint32(binN[fin-2:fin-1])
        n2 = np.uint32(binN[fin-3:fin-2])
        n3 = np.uint32(binN[fin-4:fin-3])
        n4 = np.uint32(binN[fin-5:fin-4])
        n5 = np.uint32(binN[fin-6:fin-5])
        n6 = np.uint32(binN[fin-7:fin-6])
        n7 = np.uint32(binN[fin-8:fin-7])
        n8 = np.uint32(binN[fin-9:fin-8])

        n9 = np.uint32(binN[fin-10:fin-9])
        n10 = np.uint32(binN[fin-11:fin-10])
        n11 = np.uint32(binN[fin-12:fin-11])
        n12 = np.uint32(binN[fin-13:fin-12])
        n13 = np.uint32(binN[fin-14:fin-13])
        n14 = np.uint32(binN[fin-15:fin-14])
        n15 = np.uint32(binN[fin-16:fin-15])
        n16 = np.uint32(binN[fin-17:fin-16])
        
        n17 = np.uint32(binN[fin-18:fin-17])
        n18 = np.uint32(binN[fin-19:fin-18])
        n19 = np.uint32(binN[fin-20:fin-19])
        n20 = np.uint32(binN[fin-21:fin-20])
        n21 = np.uint32(binN[fin-22:fin-21])
        n22 = np.uint32(binN[fin-23:fin-22])
        n23 = np.uint32(binN[fin-24:fin-23])
##        n21= np.uint32(0)
##        n22= np.uint32(0)
##        n23= np.uint32(0)

        self.value = [bool(n0), bool(n1),bool(n2),bool(n3),bool(n4),bool(n5),bool(n6),bool(n7),bool(n8),bool(n9),bool(n10),bool(n11),bool(n12),bool(n13),bool(n14),bool(n15),bool(n16),bool(n17),bool(n18),bool(n19),bool(n20),bool(n21),bool(n22),bool(n23)]
        #print(value)

        
    def setXFreq(self,f):
        #f: decimal value varying between 60 and 90 MHz
        # tested between 59.5 and 89.5 MHz
        # 23 bits
        # F(MHz) = N x 500 / 2**23
        #Vpp, Vmax = 5 volts
        #Power = Vpp^2/8R = Vpp^2/400 (R= 50 Ohms) , Pmax = 25/400 = 100/1600 = 1/16 Watts
        #Pmax = 62.5 mW
        #Maximum Power for ADO 2W, tested with 1,7 Watts
                #N = np.uint32(f*(2**(23))/(500))  #revisar
        #print(binN)
        N = np.uint32(f * (2**23)/500)
        self.NtoTask(N)
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line8')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line9')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line10')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line11')

            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line12')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line13')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line14')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line15')

            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line16')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line17')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line18')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line19')

            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line20')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line21')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line22')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line23')

            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line24')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line25')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line26')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line27')

            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line28')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line29')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line30')
            task.do_channels.add_do_chan('cDAQ1Mod1/port0/line31')
            
            task.write(self.value)

    def setYFreq(self,f):
        N = np.uint32(f * (2**23)/500)
        self.NtoTask(N)
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line8')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line9')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line10')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line11')

            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line12')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line13')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line14')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line15')

            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line16')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line17')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line18')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line19')

            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line20')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line21')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line22')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line23')

            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line24')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line25')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line26')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line27')

            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line28')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line29')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line30')
            task.do_channels.add_do_chan('cDAQ1Mod2/port0/line31')
            
            task.write(self.value)
        
        
