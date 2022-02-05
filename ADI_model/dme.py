#! /usr/bin/env python

#Copyright  2021 <Michael Paul>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re
import sys
import math
import numpy as np
import argparse

from os.path import dirname
import os.path 
sys.path.append(dirname(__file__)) #adds this file's director to the path
import mpUtil

#expects to be initialized with two (x,y) tuples
#it then figures out y=mx+b from the points and returns
# y when x is given
class Line2D(object):
    def __init__(self,p1,p2):
        self.x1 = p1[0]
        self.y1 = p1[1]
        self.x2 = p2[0]
        self.y2 = p2[1]
            
        try:
            self.m = (self.y2-self.y1)/(self.x2-self.x1)
        except:
            print("x1 and x2 are the same: %g %g" % (self.x1,self.x2))
            return None
        self.b = self.y2-(self.m*self.x2)

    def getY(self,x):
        return self.m*x+self.b

    #returns true if x is between x1 and x2
    def x_in_range(self,x):
        if x < self.x1:
            return -1
        if x > self.x2:
            return 1
        return 0


#pass a group of points that describe a pwl shape
#then call this object with a time and it returns the y value for that time
#pass a pwlFile that is space delimited, 2 columns of x y points
class pwlWave(object):
    def __init__(self,pwlFile=None):
        self.line_pointer = None
        if(self.readPWLFile(pwlFile)):
            self.buildPwlFromText()
            pass
        pass

    def readPWLFile(self,pwlFile):
        self.pwlFile = pwlFile
        self.pwl = []

        try :
            file = open(self.pwlFile)
        except:
            log = []
            return False

        with file as inf:
            self.log = []
            self.text = []
            for line in inf:
                self.text.append(line)
                
        return True

    def buildPwlFromText(self,text=None):
        if(text is not None):
            self.text = text

        self.lines = []
        for line in self.text:
            line = line.rstrip()
            ln = line.split()
            ln[0] = float(ln[0])
            ln[1] = float(ln[1])
            self.pwl.append(ln)

        for i in range(len(self.pwl)-1):
            self.lines.append(Line2D(self.pwl[i],self.pwl[i+1]))

        self.line_index = 0

        return True
            
    def pwlTimes(self,time):
        #pwl = ((0,0.6),(0.5,0.8),(0.501,0.9), (0.560,0.9), (0.561,0.6))
        #pwl = ((0,0.6),(0.5,0.6),(0.501,0.8), (0.560,0.8), (0.561,0.6))

        #this section makes the pattern repeat forever
        while time < self.pwl[0][0]:
            time += self.pwl[-1][0]

        while time > self.pwl[-1][0]:
            time -= self.pwl[-1][0]

        #this section makes 1st and last points persist
        if False:
            if time < self.pwl[0][0]:
                return self.pwl[0][1]
            if time > self.pwl[-1][0]:
                return self.pwl[-1][1]

        while(self.line_index >= 0 and self.line_index < len(self.lines)):
            i = self.lines[self.line_index].x_in_range(time)
            if i == 0:
                return self.lines[self.line_index].getY(time)
            self.line_index += i

        print("Should not have gotten here!!!!")
        return p[-1][1]

#set up a pulse train that can be used to measure pulse response
#need a repeating (prime number) set of pulses that are coherantly sampled
#across the sample period
#ts * ns / Prime = Tpulse
#Tpulse should be long so that reflections die out before the next transition
#Tpulse should also be short so that the coherant sample gets as many amplitudes 
#and phases as possible
class pulse_wave(object):
    def __init__(self,ts=1/81.92e6,ns=8192, prime=13, duty_cycle=0.5, trise=10e-9):
        self.ts = ts #1/81.92e6
        self.ns = ns #8192
        self.tstop=ts*ns 
        self.tper = ts * ns / prime
        self.trise=10e-9
        self.thigh = duty_cycle * (self.tper - 2 * self.trise)
        self.tlow  = (1-duty_cycle) * (self.tper - 2 * self.trise)

        self.pwl_wave = pwlWave()
        tstart = 0
        t0 = tstart
        self.amp=1

        if(False): #short pulse
            self.pwl =     ["%.12f %.2f" % (t0,               0)]
            self.pwl.append("%.12f %.2f" % (t0+1e-12,  self.amp))
            self.pwl.append("%.12f %.2f" % (t0+self.ts,  self.amp))
            self.pwl.append("%.12f %.2f" % (t0+self.ts+1e-12,  0))
            self.pwl.append("%.12f %.2f" % (self.tper, 0))

        if(True):
            self.pwl =     ["%.12f %.2f" % (t0,               1*self.amp)]
            self.pwl.append("%.12f %.2f" % (self.thigh,       1*self.amp))
            self.pwl.append("%.12f %.2f" % (self.thigh+trise, 0))
            self.pwl.append("%.12f %.2f" % (self.tper-trise , 0))
            self.pwl.append("%.12f %.2f" % (self.tper,        1*self.amp))
            self.pwl_wave.buildPwlFromText(self.pwl)

        self._sample_()
        self._fft_()

    def _sample_(self):
        self.sampled_times  = []
        self.sampled_values = []
        for i in range(0,self.ns):
            tx = i * self.ts
            self.sampled_times.append(tx)
            self.sampled_values.append(self.pwl_wave.pwlTimes(tx))
            #dme.write("%.12f %.12f\n" % (tx, values[-1]))
            ##use this to make an eye diagram
            #t0=self.per/2
            #loop=per
            #if(False):
            #    if(tx - t0 > loop):
            #        t0+=loop
            #        print("")
            #    print("%.12f %.12f" % (tx-t0, wave.pwlTimes(tx)))
        #print("#last timepoint = %.12f, %.2f" % (tx, values[-1]))

    def _fft_(self):
        values = np.array(self.sampled_values, dtype=float)
        self.fft_value = np.fft.rfft(values)
        self.fft_freq  = np.fft.rfftfreq(n=values.size, d=self.ts)
        #mag = np.abs(fft_value)**2
        #reconstruct = np.fft.irfft(fft_value)

        #for i in range(0,len(reconstruct)):
            #print("%.12f %.12f" % (ts*i, reconstruct[i]))

        #with open("dme_wave.fft", 'w') as fft:
        #    for i in range(0,len(fft_freq)):
        #        fft.write("{:.12f} {:.12g}\n".format(fft_freq[i], fft_value[i]))



class dme_wave(object):
    def __init__(self,ts=1/81.92e6,ns=8192,n_symbols=1250):
        self.ts = ts #1/81.92e6
        self.ns = ns #8192
        self.tstop=ts*ns 
        self.n_symbols=n_symbols

        pattern = np.random.randint(2,size=self.n_symbols)
        pattern[0]=1
        pattern[-1]=0
        tstart = 0
        self.amp=0.5
        self.trise=10e-9
        self.per=80e-9
        self.pwl = ["0 %.2f" % self.amp]
        t0 = tstart
        tflat = (self.per-(4*self.trise))/2
        for i in pattern:
            self.pwl.append("%.12f %.2f" % (t0+self.trise, i-self.amp))
            self.pwl.append("%.12f %.2f" % (t0+(self.trise+tflat),  i-self.amp))
            self.pwl.append("%.12f %.2f" % (t0+(3*self.trise+tflat),   -self.amp+(1-i)))
            self.pwl.append("%.12f %.2f" % (t0+(3*self.trise+2*tflat), -self.amp+(1-i)))
            t0 += self.per
        self.pwl.append("%.12f %.2f" % (self.per*len(pattern), -self.amp+(1-i)))
        self.pwl_wave = pwlWave()
        self.pwl_wave.buildPwlFromText(self.pwl)

        self._sample_dme()
        self._fft_dme()

    def _sample_dme(self):
        self.sampled_times  = []
        self.sampled_values = []
        for i in range(0,self.ns):
            tx = i * self.ts
            self.sampled_times.append(tx)
            self.sampled_values.append(self.pwl_wave.pwlTimes(tx))
            #dme.write("%.12f %.12f\n" % (tx, values[-1]))
            ##use this to make an eye diagram
            #t0=self.per/2
            #loop=per
            #if(False):
            #    if(tx - t0 > loop):
            #        t0+=loop
            #        print("")
            #    print("%.12f %.12f" % (tx-t0, wave.pwlTimes(tx)))
        #print("#last timepoint = %.12f, %.2f" % (tx, values[-1]))

    def _fft_dme(self):
        values = np.array(self.sampled_values, dtype=float)
        self.fft_value = np.fft.rfft(values)
        self.fft_freq  = np.fft.rfftfreq(n=values.size, d=self.ts)
        #mag = np.abs(fft_value)**2
        #reconstruct = np.fft.irfft(fft_value)

        #for i in range(0,len(reconstruct)):
            #print("%.12f %.12f" % (ts*i, reconstruct[i]))

        #with open("dme_wave.fft", 'w') as fft:
        #    for i in range(0,len(fft_freq)):
        #        fft.write("{:.12f} {:.12g}\n".format(fft_freq[i], fft_value[i]))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='performs a convolution over a pwl as if the pwl was being\
        read by an adc'\
        )

    parser.add_argument('--wave', type=str, default="pwl.txt", \
            help='simulate the class template in the time domain')

    parser.add_argument('--plot', action='store_true',\
            help='plot the --wave output.  Only works when --wave is also used')

    args = parser.parse_args()

    ts = 1/81.92e6
    ns = 8192
    tstop=ts*ns 

    #pattern = [1,0,1,1,0,1,0,0,0,0,1,1,1,1]
    pattern = np.random.randint(2,size=1250)
    pattern[0]=1
    pattern[-1]=0
    tstart = 0
    amp=0.5
    trise=10e-9
    per=80e-9
    op = ["0 0.5"]
    t0 = tstart
    tflat = (per-(4*trise))/2
    for i in pattern:
        op.append("%.12f %.2f" % (t0+trise, i-amp))
        op.append("%.12f %.2f" % (t0+(trise+tflat), i-amp))
        op.append("%.12f %.2f" % (t0+(3*trise+tflat), -amp+(1-i)))
        op.append("%.12f %.2f" % (t0+(3*trise+2*tflat), -amp+(1-i)))
        t0 +=per
    op.append("%.12f %.2f" % (per*len(pattern), -amp+(1-i)))

    with open("dme_pattern.txt", 'w') as dme:
        dme.write("\n".join(op))

    if(args.wave):
        #wave = pwlWave(args.wave)
        wave = pwlWave("dme_pattern.txt")
        i=0
        times = []
        values = []
        t0=40e-9
        loop=per

        with open("dme_wave.txt", 'w') as dme:
            for i in range(0,ns):
                tx = i * ts
                times.append(tx)
                values.append(wave.pwlTimes(tx))
                dme.write("%.12f %.12f\n" % (tx, values[-1]))
                if(False):
                    if(tx - t0 > loop):
                        t0+=loop
                        print("")
                    print("%.12f %.12f" % (tx-t0, wave.pwlTimes(tx)))
            print("#last timepoint = %.12f, %.2f" % (tx, values[-1]))

    values = np.array(values, dtype=float)
    fft_value = np.fft.rfft(values)
    fft_freq  = np.fft.rfftfreq(n=values.size, d=ts)
    mag = np.abs(fft_value)**2
    reconstruct = np.fft.irfft(fft_value)

    #for i in range(0,len(reconstruct)):
        #print("%.12f %.12f" % (ts*i, reconstruct[i]))

    with open("dme_wave.fft", 'w') as fft:
        for i in range(0,len(fft_freq)):
            fft.write("{:.12f} {:.12g}\n".format(fft_freq[i], fft_value[i]))

    if(args.wave and args.plot):
        import subprocess
        gnuplot_bin = ['/usr/bin/env', 'gnuplot', '-']
        gp = subprocess.Popen(gnuplot_bin,stdin = subprocess.PIPE,
        stdout = subprocess.PIPE, stderr = subprocess.PIPE)

        gp.stdin.write("set term qt enhanced font \"Linear Helv Cond Bold,9\"\n")
        gp.stdin.write("unset key\n")
        #gp.stdin.write("set multiplot layout 5,1\n")
        #gp.stdin.write("set xrange [-0.001:0.01]\n")
        #gp.stdin.write("set yrange [0:*]\n")
        gp.stdin.write("set title 'Class %d Template: Current Waveform'\n")

        gp.stdin.write("plot for [i=0:%d] '-' u 2:4 w lp\n" % nmax)
        for a in aoa:
            for line in a:
                gp.stdin.write("%s\n" % line)
            gp.stdin.write("e\n\n")

        print(">"),
        user_input = raw_input()

        gp.stdin.write("unset multiplot\n")
        gp.communicate('e\nquit\n')

    exit (0)
