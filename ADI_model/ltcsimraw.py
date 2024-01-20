#! /usr/bin/env python3

#Copyright  2021 <Michael Paul>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import sys
import string
import struct
import math
import re
import numpy as np
import argparse
from collections import OrderedDict

from os.path import dirname
import os.path 
sys.path.append(dirname(__file__)) #adds this file's director to the path
import mpUtil

class SignalIterator:
    def __init__(self, signal):
        self._signal = signal
        self._index = self._signal.start_index

    def __next__(self):
        if self._index < self._signal.stop_index:
            result = self._signal.getTimePointByIndex(self._index)
            self._index += 1
            return result
        raise StopIteration

#make groups by timepoint
class SimData(object):
    def __init__(self,trace_list):
        self.steps = []
        self.trace_list = trace_list
        self.last_x_data=-1e20 #rediculously negative number
        self.steps.append(self.newSimStep(trace_list))

    def newSimStep(self,trace_list):
        return SimStep(self.trace_list,len(self.steps))

    #add a time point curated from the raw file
    #the ltcsimraw object that calls this method
    #sould pass a list of data that matches the 
    #trace_list order and length
    def addTimePoint(self,time_point_data):
        if(self.last_x_data > time_point_data[0]):
            self.steps.append(self.newSimStep(self.trace_list))
        self.last_x_data = time_point_data[0]
        self.steps[-1].addTimePoint(time_point_data)

    def makeDifferentialSignal(self,labelp,labeln):
        name = ""
        for s in self.steps:
            name = s.differentialSignal(labelp,labeln)
            s.finalize_data()
        return(name)
        #TODO: add differential signal to trace list?

    def signal(self,name):
        signals = []
        for s in self.steps:
            signals.append(s.sigs[name])
        return signals

    #call this after all data has been added to the structure
    #this will set things up for easy access later
    def finalize_data(self):
        for s in self.steps:
            s.finalize_data()

    #when doing an fft you need even time steps from the simulator
    #even with commands to control the time setps the simulator will be
    #inconsistent at the beginning and end of the sim
    #restrict the data set to a subset of the data near the end of the trace
    #the first few time steps and the last time step are inconsitent
    def find_n_even_time_steps(self,n):
        for s in self.steps:
            s.find_n_even_time_steps(n)

    def fft(self,ns):
        self.find_n_even_time_steps(ns)
        for s in self.steps:
            s.fft()

    def last_time_point(self,signal_name):
        s = self.signal(signal_name)
        tp = []
        for x in s:
            tp.append(x.getTimePointByIndex(-1))
        return(tp)

    #fh is either gp.stdin (opened in another part of the program
    #or sys.stdout to send the data to the terminal
    def gnuplot_fft(self,fh,signal_name):
        output = self.signal(signal_name)
        plotstring = bytes("plot for [i=0:%d] '-' u 1:2:3:4 w vectors lt i+1 filled size screen 0.01,5 t sprintf(\"%s_%%d\", i)\n" % (len(self.steps)-1,signal_name),'utf8')

        fh.write(plotstring)
        for o in output:
            for x in o.iter_fft_plot_values():
                noise_floor = o.fft_median
                fh.write(b"%.12e %.12e 0 %.12e %.12e %.12e\n" %
                        (x[0],noise_floor,x[1]-noise_floor,x[2],x[1]))
            fh.write(b"e\n")
        fh.write(b"\n\n")

    #fh is either gp.stdin (opened in another part of the program
    #or sys.stdout to send the data to the terminal
    def gnuplot_signal(self,fh,signal_name):
        output = self.signal(signal_name)
        plotstring = bytes("plot for [i=0:%d] '-' u 1:2 w l lt i+1 t sprintf(\"%s_%%d\", i)\n" % (len(self.steps)-1, signal_name),'utf8')
        fh.write(plotstring)
        for o in output:
            for x in o:
                fh.write(b"%.12e %.12e\n" %
                        (x[0],x[1]))
            fh.write(b"e\n")
        fh.write(b"\n\n")


#grouped x-axis and several y-axis traces
class SimStep(object):
    def __init__(self,trace_list,step_number):
        #make signal groups here
        self.trace_list = trace_list
        self.step_number=step_number
        self.sigs = OrderedDict()
        self.sigs[trace_list[0]] = TimeSignal(trace_list[0])
        self.x_axis_signal = self.sigs[trace_list[0]]
        self.start_index = 0
        self.end_index = 0
        for i in range(1,len(trace_list)):
            #create signal objects
            self.sigs[trace_list[i]] = Signal(trace_list[i])

    #add a time point curated from the raw file
    #the ltcsimraw object that calls this method
    #sould pass a list of data that matches the 
    #trace_list order and length
    def addTimePoint(self,time_point_data):
        for i,x in enumerate(self.trace_list):
            self.sigs[x].addData(time_point_data[i])

    def differentialSignal(self,labelp,labeln):
        d = DifferentialSignal(self.sigs[labelp],self.sigs[labeln])
        d.x_axis_signal = self.sigs[self.trace_list[0]]
        self.sigs[d.name] = d
        self.trace_list.append(d.name)
        return(d)

    def finalize_data(self):
        for s in self.sigs:
            self.sigs[s].stop_index  = len(self.sigs[s].values)-1
            self.sigs[s].start_index = 0
            self.sigs[s].x_axis_signal = self.sigs[self.trace_list[0]]

    def find_n_even_time_steps(self,n):
        self.sigs[self.trace_list[0]].find_n_even_time_steps(n)
        #spread the word to the rest of the signals
        for i in range(1,len(self.trace_list)):
            self.sigs[self.trace_list[i]].stop_index = \
            self.sigs[self.trace_list[0]].stop_index

            self.sigs[self.trace_list[i]].start_index = \
            self.sigs[self.trace_list[0]].start_index

    def fft(self):
        for s in self.sigs:
            self.sigs[s].fft()

class Signal(object):
    #start and end index as class variables keep all of the data synchronized
    #on the x-axis when a subset of the data traces is being used.
    #frequency values

    def __init__(self,name):
        self.name = name
        self.values=[]
        self.fft_phasors=[]
        self.iter=0
        self.is_x_axis=False
        self.x_axis_signal=None
        self.stop_index=0
        self.start_index=0

    def __str__(self):
        s = "name  : %s\nlen   : %d\nstart : %d\nstop  : %d" % (self.name,
                len(self.values), self.start_index, self.stop_index)
        return s

    def __repr__(self):
        s = "name : %s, len : %d, start : %d, stop  : %d" % (self.name,
                len(self.values), self.start_index, self.stop_index)
        return s

    def __iter__(self):
        return SignalIterator(self)

    def iter_fft_plot_values(self):
        for i,x in enumerate(self.fft_phasors):
            #print(i)
            yield (self.x_axis_signal.fft_phasors[i],20*np.ma.log10(np.abs(x)),
                    np.angle(x))

    #return the name of the signal with v() or ix(), etc stripped off
    #example return is ('v','a') as a tuple for v(a)
    #or ('ix','m1:s') for ix(m1:s)
    def _simple_name(self):
        if(self.is_x_axis):
            return self.name
        else:
            m1 = re.search('(v|ix|i)\((\S*)\)',self.name,flags=re.IGNORECASE);
            try:
                return(m1.group(1),m1.group(2))
            except Exception as e:
                print(e)
                print("Can't understand this signal '%s'" % self.name)
                exit(1)

    def addData(self,value):
        self.values.append(value)

    def getLength(self):
        return len(self.values[self.start_index:self.stop_index])

    def getValueByIndex(self,index):
        try:
            return self.values[index]
        except Exception as e:
            print(e)
            print("index outside of array: %d / %d" % (index, len(self.values)))
        return None

    #used for iteration throught the data.  Index refers to a cell in the values
    #array
    def getTimePointByIndex(self, index):
        return (self.x_axis_signal.getValueByIndex(index),
                self.getValueByIndex(index))

    def getT0(self):
        return (self.x_axis_signal.getValueByIndex(self.start_index),
                self.getValueByIndex(self.start_index))

    def fft(self):
        self.values = np.array(self.values, dtype=float)
        self.fft_phasors = np.fft.rfft(self.values[self.start_index:self.stop_index])

        #use masked arrays to stop -inf from messing up median statistics
        a = np.abs(self.fft_phasors)
        l = 20*np.ma.log10(a)
        self.fft_median = np.ma.median(l)
        print("%s: median %.1fdB" % (self.name, self.fft_median))

class DifferentialSignal(Signal):
    #sigp and sign are Signal objects
    def __init__(self,sigp,sign):
        self.sigp = sigp
        self.sign = sign
        self.start_index=0
        self.stop_index=0

        np = sigp._simple_name()
        nn = sign._simple_name()
        self.name = "%s(%s,%s)" % (np[0],np[1],nn[1])
        self.is_x_axis=False
        self.values=[]

        for i in range(len(self.sigp.values)):
            self.values.append(self.sigp.values[i]-self.sign.values[i])

class TimeSignal(Signal):
    #limit the precision of the number to stop floating point error from 
    #creating jitter

    def get_time_step(self,index,time_precision=15):
        return round(self.values[index]-self.values[index-1],time_precision)

    def verify_time_steps(self,time_precision=15):
        #check that all time steps are equal to dt
        #and extract differentail signals
        dt = self.get_time_step(self.start_index+1,time_precision)
        ok=True
        for i in range(self.start_index+1,self.stop_index):
            d = self.get_time_step(i,time_precision)
            if(d != dt):
                #print("%d %e != %e" % (i, d, dt))
                ok=False
        return ok

    def find_n_even_time_steps2(self,n):
        d = np.diff(self.values)
        for i,x in enumerate(d):
            print(i,x)

    #look for a run of even time steps so a time domain signal can
    #be converted to a frequency domain signal
    def find_n_even_time_steps(self,n):
        time_precision=15
        stop_index=len(self.values)-1
        start_index=stop_index-n
        found=False
        while(len(self.values[start_index:stop_index]) >= n and not found):
            found=True
            dt = self.get_time_step(stop_index,time_precision)
            #print(stop_index)
            for i in range(stop_index,start_index,-1):
                t = self.get_time_step(i,time_precision)
                #print("%5d %.15e %.15e" % (i,t,dt))
                if(dt != t):
                    stop_index=i-1
                    start_index=stop_index-n
                    found=False
                    break
        if(found):
            self.start_index=start_index
            self.stop_index=stop_index
            #print("%d %d %d" % (len(self.values[self.start_index:self.stop_index]),self.start_index, self.stop_index))
        else:
            self.find_n_even_time_steps2(n)
            print("Couldn't find enough even timesteps for fft")
            print(stop_index)
            print(start_index)
            print(stop_index-start_index)
            exit(1)

    def fft(self):
        dt = self.get_time_step(self.start_index+1)
        self.fft_phasors  = np.fft.rfftfreq(n=int(self.getLength()), d=dt)


class ltcsimraw():

    def __init__(self,rawfile):
        self.rawfile = rawfile
        self.preamble = {}

        #hash of variable names to number in the rawfile
        self.variableNumber = {}
        self.variables = []
        self.binary_start = 0
        self.nvars = 0
        self.points = 0
        #differently

        self.filehandle = None
        self.timePoint = 0
        #self.mcalc = Mcalc()
        

        ntrys=0
        file=None
        if not os.path.isfile(self.rawfile):
            print("Raw File does not exist!\n-> ",self.rawfile)
            exit(1)

        while file==None and os.path.isfile(self.rawfile):
            try:
                file=open(self.rawfile, "rb")
                break
            except:
                print( "rawfile: cannot open: %s" % rawfile)
                ntrys += 1
                if(ntrys > 100):
                    exit(1)

        with file as inf:
            self.x64 = self.detectX64File(inf)
            self.readPreamble(inf)
            self.readVariables(inf)
            
            self.binary_start = inf.tell()

        file.close()
        self.complex_data = False
        if "complex" in self.preamble['Flags']:
            self.complex_data = True

    
    #If the First 2
    def detectX64File(self,file):
        fpointer = file.tell()
        file.seek(0,0)
        r = file.read(2)
        file.seek(fpointer,0)
        if r[0]== ord('T') and  r[1]==0:
                return True
        return False

    def lt_readline(self,file):
        line = ""
        keep_reading=True
        nread=1

        #In ltcsim x64 the ascii characters are being written as 16bit
        #chars, for example 'T' is written to the file as 'T\0'
        #If x64 is detected read the chars as 16 bits and throw away the 
        #trailing '\0'
        if self.x64==True:
            #print("Reading x64 file")
            nread=2
        else:
            pass
            #print("Reading x32 file")
        while(keep_reading):
            r = file.read(nread)
            #print("r len: ", len(r))
            r = r[0]
            if(r==ord('\n')):
                keep_reading=False
            elif(r==ord('\0')):
                print( "Should never get here!!!")
                pass
            else:
                line += chr(r)
        #print(line)
        return line

    def readPreamble(self,file):
        self.preamble = {}
        #for line in iter(file.readline, ''):
        while(True):
            line = self.lt_readline(file)
            #print( line)
            if line.startswith("Variables:"):
                break
            line = line.rstrip()
            #print( "#" + line)
            ln = line.split(": ") 
            print( line)
            #print( ln)
            self.preamble.update({ln[0]:ln[1]})

        self.nvars =  int(self.preamble['No. Variables'])
        self.points = int(self.preamble['No. Points'])
        #self.x64 = int(


    def readVariables(self,file):
        self.variables = [] 
        #for line in iter(file.readline, ''):
        while(True):
            line = self.lt_readline(file)
            if line.startswith("Binary:"):
                break
            line = line.rstrip()
            #print( line)
            ln = line.split()
            #variableNumber[ln[1].lower()] = ln[0]
            self.variables.append(ln[1].lower())

        for i,v in enumerate(self.variables):
            self.variableNumber[v] = i


    
    #pass a variable number to be extracted from the file
    def getSignal(self,varnums):
        with open(self.rawfile, "rb") as f:
            #print( self.binary_start)
            f.seek(self.binary_start)
            size = self.getChunkSize(f)
            ans = []
            tp = []

            #chose the data reading method
            readfunc = self.readReal
            if self.complex_data:
                readfunc = self.readComplex
            
            for n in range(self.points):
                chunk = f.read(size)
                if chunk:
                    p = readfunc(chunk,varnums)
                    ans.append(p)
            f.close()
        return ans

    #parses complex number from a chunk of the file.
    def readComplex(self, chunk, signals):
        x = struct.unpack('d',chunk[0:8])[0]
        ret = [abs(x)]
        for y in signals:
            start = y * 16 
            end = start + 16
            p = struct.unpack('dd',chunk[start:end])
            ret.append(complex(p[0],p[1]))
        return ret

    def readReal(self,chunk,signals):
        x = struct.unpack('d',chunk[0:8])[0]
        ret = [abs(x)]
        #print( x)
        for y in signals:
            start = (y * 4) + 4
            end = start + 4
            p = struct.unpack('f',chunk[start:end])[0]
            #print( p)
            ret.append(p)
        return ret

    #returns the size of 1 data point in the file
    #this is the x-axis info plus all of the variables for one point on the
    #x-axis
    def getChunkSize(self,handle):
        x = handle.tell()
        handle.seek(0,2) #seeks to the end of the file
        end = handle.tell()
        nbytes = end-self.binary_start
        handle.seek(x)
        return nbytes//self.points

    def readLastTimePoint(self):
        if self.filehandle == None:
            self.filehandle = open(self.rawfile, "rb")
            self.filehandle.seek(self.binary_start,0)
            self.chunkSize = self.getChunkSize(self.filehandle)
            self.filehandle.seek(-1 * self.chunkSize,2)

            #tstop = float(mpUtil.decodeEngineeringNotation(args.tstop))
            #istop = rf.searchTime(tstop)

        chunk = self.filehandle.read(self.chunkSize)
        readFunc = self.readReal
        if self.complex_data:
            readFunc = self.readComplex

        if chunk:
            v = range(1,self.nvars)
            self.tp = readFunc(chunk,v)
            return True
        return False

    def readTimePoint(self):
        if self.filehandle == None:
            self.filehandle = open(self.rawfile, "rb")
            self.filehandle.seek(self.binary_start,0)
            self.chunkSize = self.getChunkSize(self.filehandle)

        chunk = self.filehandle.read(self.chunkSize)
        readFunc = self.readReal
        if self.complex_data:
            readFunc = self.readComplex

        if chunk:
            v = range(1,self.nvars)
            self.tp = readFunc(chunk,v)
            return True
        return False

    def copyRawFile(self):
        if self.filehandle == None:
            self.filehandle = open(self.rawfile, "rb")
            self.filehandle.seek(self.binary_start,0)
            self.chunkSize = self.getChunkSize(self.filehandle)

        self.filehandle.seek(0)
        header = self.filehandle.read(self.binary_start)
        of = open("concat.raw", "wb")
        of.write(header)
        data = self.filehandle.read(4096)
        of.write(data)
        of.write(struct.pack('d',0.0))
        of.write(data)
        of.close()
        exit(0)

    #works with readTimePoint....
    def getVal(self,var):
        i = self.variableNumber[var]
        return self.tp[i]

    #decodes signals names into variable numbers 
    def getSignalLabels(self, vlist, ilist, others=[]):
        y = []
        labels = ["time"]
        if(self.complex_data):
            labels = ["frequency"]

        for v in vlist:
            s = "v(%s)" % v.lower()
            for i in self.variables:
                if s in i:
                    #print( i)
                    y.append(self.variableNumber[i])
                    labels.append(s)
                    continue

        for i in ilist:
            s = "(%s)" % i.lower()
            for i in self.variables:
                if i.startswith("i") and s in i:
                    y.append(self.variableNumber[i])
                    labels.append(i)
                    continue

        for x in others:
            s = x.lower()
            for i in self.variables:
                if s in i:
                    #print( self.variableNumber[i])
                    y.append(self.variableNumber[i])
                    labels.append(i)
                    continue
        return (y, labels)

    #returns data in an aoa
    def getSignals(self, vlist, ilist, others=[]):
        (y,labels)=self.getSignalLabels(vlist,ilist,others)
        sig = self.getSignal(y)
        return (sig, labels)

    #returns data as a hash of signal objects
    def getSignalObjects(self, vlist, ilist, others=[]):
        (y,labels)=self.getSignalLabels(vlist,ilist,others)

        #print(labels)
        #setup a dict with signal names as the keys 
        #and signal objects as the value
        simdata = SimData(labels)
        return self.readSignals(simdata,y)

    #read data into signal objects
    def readSignals(self,sigs,varnums):
        with open(self.rawfile, "rb") as f:
            f.seek(self.binary_start)
            size = self.getChunkSize(f)

            #choose the read function
            readfunc = self.readReal
            if self.complex_data:
                readfunc = self.readComplex
            
            for n in range(self.points):
                chunk = f.read(size)
                if chunk:
                    p = readfunc(chunk,varnums)
                    sigs.addTimePoint(p)
        sigs.finalize_data()
        return sigs

    def ac_gain(self, vport1, vport2):
        (data,labels) = self.getSignals([],[],[vport1,vport2])
        index = dict(zip(labels, range(0,len(labels))))
        av = []
        frequency=[]
        for x in data:
            vend = x[index[vport2]]
            vin  = x[index[vport1]]
            av.append(vend/vin)
            frequency.append(x[0])
        return({"frequency" : frequency , "av" : av})

    def scattering_parameters(self, vport1, iport1, vport2, iport2, rin=50, rout=50):
        (data,labels) = self.getSignals([],[],[vport1[0],vport1[1],vport2[0],vport2[1],iport1,iport2])
        index = dict(zip(labels, range(0,len(labels))))
        #print(labels)
        frequency=[]
        s11=[]
        s11_phase=[]
        s22=[]
        s22_phase=[]
        dm_cm=[]
        s21=[]
        gain=[]
        phase=[]
        zin=[rin]
        zin_mag=[]
        zin_phase=[]
        zout=[rout]
        zout_mag=[]
        zout_phase=[]

        for x in data:
            vend_cm = (x[index[vport2[0]]]+x[index[vport2[1]]])/2
            vend    = x[index[vport2[0]]]-x[index[vport2[1]]]
            iend    = x[index[iport2]]
            vin     = x[index[vport1[0]]]-x[index[vport1[1]]]
            iin     = x[index[iport1]]
            a1 = (vin + (iin*rin))
            b1 = (vin - (iin*rin))
            a2 = (vend + (iend*rout))
            b2 = (vend - (iend*rout))
            s11_mp  = self.decodeComplex((a1 / b1))
            s22_mp  = self.decodeComplex((a2 / b2))
            s21_mp  = self.decodeComplex(b2 / a1)
            gain_mp = self.decodeComplex(vend/vin)
            dm_cm_mp = self.decodeComplex(vend_cm/vin)
            frequency.append(x[0])
            s11.append(s11_mp[0])
            s11_phase.append(s11_mp[1])
            s22.append(s22_mp[0])
            s22_phase.append(s22_mp[1])
            s21.append(s21_mp[0])
            gain.append(gain_mp[0])
            phase.append(gain_mp[1])
            dm_cm.append(dm_cm_mp[0])
            zin.append(vin / iin)
            zin_mag.append(pow(10,self.decodeComplex(vin/iin)[0]/20))
            zin_phase.append(self.decodeComplex(vin/iin)[1])
            zout.append(vend / iend)
            zout_mag.append(pow(10,self.decodeComplex(vend/iend)[0]/20))
            zout_phase.append(self.decodeComplex(vend/iend)[1])

        return {
            "frequency" : frequency,
            "s11" : s11,
            "s11_phase" : s11_phase,
            "s22" : s22,
            "s22_phase" : s22_phase,
            "s21" : s21,
            "gain" : gain,
            "phase" : phase,
            "zin" : zin,
            "zin_mag" : zin_mag,
            "zin_phase" : zin_phase,
            "zout" : zout,
            "zout_mag" : zout_mag,
            "zout_phase" : zout_phase,
            "dm_cm" : dm_cm,
            }

    def fft_transfer(self, fft, vport1, vport2):
        (data,labels) = self.getSignals([],[],[vport1[0],vport1[1],vport2[0],vport2[1]])
        index = dict(zip(labels, range(0,len(labels))))
        #print(labels)
        #frequency=[]
        #fft_out = [0]
        fft_out =  [complex(1e-30,0)]
        for i in range(0,len(data)):
            vend   = data[i][index[vport2[0]]]-data[i][index[vport2[1]]]
            vin    = data[i][index[vport1[0]]]-data[i][index[vport1[1]]]
            #gain_mp = self.decodeComplex(vend/vin)
            phasor_out = fft[i+1] * (vend/vin)
            fft_out.append(phasor_out)
            #frequency.append(data[i][0])

        return fft_out

    def fft_zin(self, fft, vport1, iport):
        (data,labels) = self.getSignals([],[],[vport1[0],vport1[1],iport])
        index = dict(zip(labels, range(0,len(labels))))
        #print(labels)
        #frequency=[]
        #fft_out = [0]
        fft_out =  [complex(1e-30,0)]
        for i in range(0,len(data)):
            zin    = data[i][index[vport1[0]]]-data[i][index[vport1[1]]] / data[i][index[iport]]
            #gain_mp = self.decodeComplex(vend/vin)
            phasor_out = fft[i+1] * zin
            fft_out.append(phasor_out)
            #frequency.append(data[i][0])

        return fft_out

    #changes the data from an aoa to an array of strings suitable for feeding to
    #gnuplot
    def setGnuplotFormat(self,sig,labels):
        out = []
        out.append( "#" + " ".join(labels))
        timelast = -1000000;
        nsteps = 1
        for i in sig:
            if timelast > i[0]:
                out.append("e\n\n")
                nsteps += 1
            out.append(" ".join(format("%.6e" % x) for x in i))
            timelast = i[0];
        out.append("e\n\n")
        out.append("#" + " ".join(labels))
        return (out, nsteps)

    #changes real/imag into db/degrees
    def decodeComplex(self,cmplx):
        a=np.array([cmplx.real,cmplx.imag])
        a.dtype = complex
        ans = [1e-308,0]
        try:
            ans = (20*math.log10(np.absolute(a)), \
                np.angle(a,deg=True)[0])
        except:
            pass
        return ans

    def plotComplex(self,sigs,nsteps,names,corners):
        import subprocess
    
        for c in corners:
            print( c)
        gnuplot_bin = ['/usr/bin/env', 'gnuplot','-persist', '-']
        gp = subprocess.Popen(gnuplot_bin,stdin = subprocess.PIPE,
        stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        title = "set title '%s'\n" % names[0]
        #gp.stdin.write(title)
        gp.stdin.write("set multiplot layout 2,1 title 'AC Response'\n")
        #gp.stdin.write("unset key\n")
        gp.stdin.write("set key outside right\n")
        #gp.stdin.write("set xlabel 'time'\n")
        gp.stdin.write("set format x \"%.0s%c\" \n")
        gp.stdin.write("set logscale x\n")
        #gp.stdin.write("labels = \"%s\"" % corners)
    
        #gp.stdin.write("plot for [corner in labels] '-' u 1:2 w l" % nsteps)
        gp.stdin.write("plot for [corner=1:%d] '-' u 1:2 w l t sprintf(\"%%d\",corner)" % nsteps)
        #gp.stdin.write("plot for [corner=1:%d] '-' u 1:2 w l" % nsteps)
    
        for i in sigs:
            line = i + "\n"
            #line = i 
            gp.stdin.write(line)
            gp.stdin.flush()
    
        gp.stdin.write("set yrange [-180:180] \n")
        gp.stdin.write("set ytics -180,60,180\n")
        gp.stdin.write("set xlabel 'frequency'\n")
        #gp.stdin.write("plot for [corner=1:%d] '-' u 1:3 w l" % nsteps)
        gp.stdin.write("plot for [corner=1:%d] '-' u 1:3 w l t sprintf(\"%%d\",corner)" % nsteps)
        for i in sigs:
            line = i + "\n"
            #line = i 
            gp.stdin.write(line)
            gp.stdin.flush()
    
        gp.stdin.write("unset multiplot")
        #for line in iter(gp.stderr.readline,''):
               #print( line.rstrip())
        gp.communicate('e\nquit\n')

    #pass the rawfile object
    def searchTime(self,time):
        s = self.getSignal([0])
        index=0
        return _binarySearch(s,time,0,len(s))

def _binarySearch(timeSeries,time,start,end):
    mid = (end + start) / 2 
    #print( "%d\t%e\t%e" % (mid, timeSeries[mid][0],time))
    if(mid == start or mid == end):
        return mid
    if(time < timeSeries[mid][0]):
        return _binarySearch(timeSeries,time,start,mid)
    elif(time > timeSeries[mid][0]):
        return _binarySearch(timeSeries,time,mid,end)
    else:
        return mid

if __name__ == '__main__':

    #if(len(sys.argv) > 1):#ys.argv[1]):
    #    rawfile = sys.argv[1]
    #    if(not os.path.isfile(rawfile)):
    #        rawfile = None

        
    ## example:
    #for b in bytes_from_file('filename'):
    #    do_stuff_with(b)

    dot_ide = os.path.join(os.environ['PROJECTS'],".ide") #adds this file's director to the path
    parser = argparse.ArgumentParser(
        description='extract data from an ltspice .raw file'
        )

    parser.add_argument('--xfer', type=str, \
            help='open loop gain analysis using impedance sensitive probe\n \
            pass the subcircuit name of the probe (xp for example)')

    parser.add_argument('-b', '--bias', action='store_true', help='print out\
            bias voltages suitable for a .loadbias call')

    parser.add_argument('-c', '--copy', action='store_true', help='\
            copies a rawfile. not really useful')

    parser.add_argument('-s', '--sub', action='store_true', help='print\
            substrate currents')

    parser.add_argument('--preamble', action='store_true', help='print\
    the preamble')

    parser.add_argument('--plot', action='store_true', help='send the output to\
    gnuplot.  only works with the -i or -v options')

    parser.add_argument('--multiplot', action='store_true', help='send the output to\
    gnuplot.  Each distict waveform is in its own window. Only works with the -i or -v options')

    parser.add_argument('-l', '--list', action='store_true', help='print\
    the signal names')

    parser.add_argument('-m', '--match', metavar='match', type=str, 
        help='node name to match.  Match starts with I and ends with "match")')

    parser.add_argument('-t', '--stats', metavar='signal', dest='signal', type=str,
        help='USE ISLEUTH.py instead full signal names to match.  Prints out stats on the names. \
    Example: Use spifile.py to get a list of nodes that sink current. \
    Then feed the list to this to find the ones that are talking too much current' \
            )

    parser.add_argument('--tstart', metavar='time', help=' \
    time to start extraction')

    parser.add_argument('--tstop', metavar='time', help=' \
    time to end extraction')

    parser.add_argument('-v', '--volt', metavar='volt', type=str, nargs='+',
        default=[],
        help='list of voltages to extract (whitespace delimited)\
    separate two names with a comma (,) to have the nodes plotted differentially')

    parser.add_argument('-i', '--current', metavar='current', type=str, nargs='+',
        default=[],
        help='list of currents to extract')

    if(len(sys.argv) > 1 and sys.argv[-1] != None):
        rawfile = sys.argv.pop()
        #print( rawfile)
    else:
        parser.print_help()
        exit(1)

    args = parser.parse_args()
    #print( "*" + args)

    rf = ltcsimraw(rawfile)

    if args.signal:
        print( "Stats:")
        sigs = args.signal.split()
        ans = []
        for i in sigs:
            i = i.lower()
            if i in rf.variables:
                y = rf.variableNumber[i]
                s = rf.getSignal([y])
                sig = np.transpose(np.array(s,np.float))

                #argmin gives the index at min
                median = np.median(sig[1])
                min = np.amin(sig[1])
                max = np.amax(sig[1])
                std = np.std(sig[1])
                charge = np.trapz(sig[1],sig[0])
                ans.append([y,std,min,max,charge,median])
                #print( "%s %e %e %e %e" % (y ,std, min, max, charge))
        print( len(ans))
        a = np.array(ans)
        index = np.argsort(a[:,1])
        index = index[::-1]
        print( "%13s %13s %13s %13s %13s %13s" % ("RMS","Min","Max","Charge","Median","Name"))
        for n,i in enumerate(index):
            print( "% e % e % e % e % e %s" % (a[i][1], a[i][2], a[i][3],
                    a[i][4], a[i][5], rf.variables[int(a[i][0])]))
            if n > 10:
                break
        exit(0)

    if args.sub:
        print( "Substrate Currents")
        ans = []
        for i in rf.variables:
            i = i.lower()
            if i.startswith("i") and i.endswith("sub)"):
                y = rf.variableNumber[i]
                s = rf.getSignal([y])
                sig = np.transpose(np.array(s,np.float))

                #argmin gives the index at min
                min = np.amin(sig[1])
                max = np.amax(sig[1])
                std = np.std(sig[1])
                charge = np.trapz(sig[1],sig[0])
                ans.append([y,std,min,max,charge])
                #print( "%s %e %e %e %e" % (y ,std, min, max, charge))
        a = np.array(ans)
        index = np.argsort(a[:,1])
        index = index[::-1]
        print( "%13s %13s %13s %13s %13s" % ("RMS","Min","Max","Charge","Name"))
        for n,i in enumerate(index):
            print( "% e % e % e % e %s" % (a[i][1], a[i][2], a[i][3], a[i][4], rf.variables[int(a[i][0])]))
            if n > 10:
                break
        exit(0)

    if args.match:
        print( "Node(s) Matching: " + args.match)
        ans = []
        for i in rf.variables:
            if i.startswith("i") and i.endswith(args.match.lower() + ")"):
                y = rf.variableNumber[i]
                s = rf.getSignal([y])
                sig = np.transpose(np.array(s,np.float))

                #argmin gives the index at min
                min = np.amin(sig[1])
                max = np.amax(sig[1])
                std = np.std(sig[1])
                charge = np.trapz(sig[1],sig[0])
                ans.append([y,std,min,max,charge])
                #print( "%s %e %e %e %e" % (y ,std, min, max, charge))
        if(len(ans)):
            a = np.array(ans)
            index = np.argsort(a[:,1])
            index = index[::-1]
            print( "%13s %13s %13s %13s %13s" % ("RMS","Min","Max","Charge","Name"))
            for n,i in enumerate(index):
                print( "% e % e % e % e %s" % (a[i][1], a[i][2], a[i][3], a[i][4], rf.variables[int(a[i][0])]))
                if n > 10:
                    break
        else:
            print( "No Match")
        exit(0)

    elif args.xfer:
        print( "Use the script \"acAnalysis.py\" instesd")
        exit (0)

    elif args.volt or args.current:
        differential = []
        diffExtract = []
        #scan for arguements that have commas
        #if a comma is found the string needs to broken up so that the signals
        #can be plotted differentailly
        removeSigs = []
        for s in args.volt:
            if ',' in s:
                ln = s.split(',')
                #make a list of diff signals to remove from the single ended list
                removeSigs.append(s)
                
                #list of single ended signals to extract
                diffExtract.extend(ln)

                #2D list. Rows are diff signals
                #column 0 is the + signal
                #column 1 is the - signal
                differential.append(ln)

        #remove the diff signals from the single ended list
        for s in removeSigs:
            args.volt.remove(s)

        #extract the single ended and differental data
        (data,labels) = rf.getSignals(args.volt,args.current)
        (diff_data,diff_labels) = rf.getSignals(diffExtract,[])

        #convert extracted single ended signals into diff signals
        #append the diff signals to the single ended data
        for d in differential:
            try:
                indexp = diff_labels.index("v(%s)" % d[0])
                indexn = diff_labels.index("v(%s)" % d[1])
                for i,a in enumerate(diff_data):
                    x = a[indexp]-a[indexn]
                    data[i].append(x)
                labels.append("v(%s,%s)" % (d[0],d[1]))
            except:
                print( "problem extracting signal: v(%s,%s)" % (d[0],d[1]))


        istart = 0
        istop = rf.points-1
        if args.tstart:
            tstart = float(mpUtil.decodeEngineeringNotation(args.tstart))
            #istart = rf.searchTime(tstart)
            #tstart = data[istart][0]
        else:
            tstart = data[0][0]

        if args.tstop:
            tstop = float(mpUtil.decodeEngineeringNotation(args.tstop))
            #istop = rf.searchTime(tstop)
            #tstop = data[istop][0]
        else:
            tstop = data[-1][0]

        (sigs,nsteps) = rf.setGnuplotFormat(data[istart:istop],labels)
        names = labels
        names.pop(0)

        if(args.plot and rf.complex_data):
            ln = rawfile.split(".")
            extension = ln.pop()
            basename = ".".join(ln)
            logfile = basename + '.log'
            from steptable import StepTable 
            table = StepTable()
            table.readLogfile(logfile)
            print( table.steps)

            rf.plotComplex(sigs,nsteps,names,table.steps)
        elif(args.plot):
            from os import linesep as nl

            import subprocess
            gnuplot_bin = ['/usr/bin/env', 'gnuplot','-persist', '-']
            gp = subprocess.Popen(gnuplot_bin,stdin = subprocess.PIPE, \
                stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            
            gp.stdin.write( \
"set terminal qt size 640,480 enhanced font 'Linear Helv Cond Bold,9'\n")

            pstrings = []
            for i,n in enumerate(names):
                #gp.stdin.write("unset key\n")
                #gp.stdin.write("set xlabel 'time'\n")
                #title = "set title '%s'\n" % n
                #gp.stdin.write(title)
                gp.stdin.write("set xrange [%e:%e]\n" % (tstart, tstop))
                pstrings.append("for [corner=1:%d] '-' u 1:%d w l t '%s'" % \
                        (nsteps, 2+i ,n ))

            plotstring = ",".join(pstrings)
            plotstring = "plot %s\n" % (plotstring)
            print( plotstring)
            gp.stdin.write(plotstring)

            for i,n in enumerate(names):
                for l in sigs:
                    line = l + "\n"
                    #line = i 
                    gp.stdin.write(line)
                    gp.stdin.flush()

            print( len(names))
            gp.communicate('e\nquit\n')
            
        elif(args.multiplot):
            from os import linesep as nl

            import subprocess
            gnuplot_bin = ['/usr/bin/env', 'gnuplot','-persist', '-']
            gp = subprocess.Popen(gnuplot_bin,stdin = subprocess.PIPE, \
                stdout = subprocess.PIPE, stderr = subprocess.PIPE)

            height = 480 + 120*(len(names)-1)
            if height > 900:
                height = 900
            print( height)
            gp.stdin.write( \
"set terminal qt size 640,%d enhanced font 'Linear Helv Cond Bold,9'\n" % \
            height)

            gp.stdin.write("set multiplot layout %d,1 \n" % \
                (len(names)))

            for i,n in enumerate(names):
                #gp.stdin.write("set size 1.0,0.5\n")
                gp.stdin.write("unset key\n")
                #gp.stdin.write("set xlabel 'time'\n")
                title = "set title '%s'\n" % n
                gp.stdin.write(title)
                gp.stdin.write("set xrange [%e:%e]\n" % (tstart, tstop))
                gp.stdin.write("plot for [corner=1:%d] '-' u 1:%d w l t '%s\'n" % \
                        (nsteps, 2+i ,n ))

                for l in sigs:
                    line = l + "\n"
                    #line = i 
                    gp.stdin.write(line)
                    gp.stdin.flush()

            print( len(names))
            gp.stdin.write("unset multiplot\n")
            gp.communicate('e\nquit\n')

        elif rf.complex_data == False:
            pass
            #mpUtil.aoaPrint((sigs))
            for i in sigs:
                print( i)

    elif args.copy:
        rf.copyRawFile()

    elif args.preamble:
        print( rf.preamble )
        exit(0)

    elif args.list:
        for v in rf.variables:
            print( v)
        exit(0)

    elif args.bias:
        rf.readLastTimePoint()
        for i,v in enumerate(rf.tp):
            if i == 0:
                print( "*%s=%s" % (rf.variables[i],rf.tp[i]))
                print( ".ic")
                continue
            if(rf.variables[i].startswith("v")):
                print( "+%s=%s" % (rf.variables[i],rf.tp[i]))

    else:
        rf.readTimePoint()
        rf.readLastTimePoint()
        for i,v in enumerate(rf.tp):
            #print( rf.getVal("time"))
            print( "%d %s %s" % (i,rf.variables[i],rf.tp[i]))
