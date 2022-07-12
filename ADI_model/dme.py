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
import matplotlib.pyplot as pyplot
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
    def __init__(self,ts=1/81.92e6,ns=8192,n_symbols=1253,amplitude=0.5,zin=None):
        self.ts = ts #1/81.92e6
        self.ns = ns #8192
        self.tstop=ts*ns 
        self.n_symbols=n_symbols

        pattern = np.random.randint(2,size=self.n_symbols)
        pattern[0]=1
        pattern[-1]=0
        tstart = 0
        self.amp=amplitude
        self.trise=10e-9
        self.per=80e-9
        self.pwl = ["0 %.3f" % self.amp]
        t0 = tstart
        tflat = (self.per-(4*self.trise))/2
        for i in pattern:
            x = i * self.amp * 2
            self.pwl.append("%.12f %.2f" % (t0 +  self.trise           , x-self.amp))
            self.pwl.append("%.12f %.2f" % (t0 + (self.trise+tflat)    , x-self.amp))
            self.pwl.append("%.12f %.2f" % (t0 + (3*self.trise+tflat)  ,
                -self.amp+(2*self.amp*(1-i))))
            self.pwl.append("%.12f %.2f" % (t0 + (3*self.trise+2*tflat),
                -self.amp+(2*self.amp*(1-i))))
            #print("%d %s %s %s %s" % (i, self.pwl[-4], self.pwl[-3], self.pwl[-2], self.pwl[-1]))
            t0 += self.per
        #self.pwl.append("%.12f %.2f" % (self.per*len(pattern), -self.amp+(2*self.amp*(1-i))))
        self.pwl_wave = pwlWave()
        self.pwl_wave.buildPwlFromText(self.pwl)

        #print(amplitude)


        self._sample_dme()
        self._fft_dme()
        cutoff = 20e6
        order = 1
        self._lpf_dme(cutoff, order)

        if(zin):
            for i,f in enumerate(self.fft_freq):
                self.fft_value[i] = zin[i] * self.fft_value[i]

        t_domain_sig = np.fft.irfft(self.fft_value)
        #print(t_domain_sig)
        #f, eye = pyplot.subplots(1,1, figsize=(10, 10))  # Create a figure and an axes.
        #eye.plot(range(len(t_domain_sig)), t_domain_sig)  # Plot more data on the axes...
        #eye.set_xlim([0,128])
        #pyplot.savefig("junk.png")
        #pyplot.close(f)

    def output_pwl_to_file(self, filename="pwl.txt"):
        with open(filename, 'w') as out:
            for p in self.pwl:
                out.write("%s\n" % p)

    def output_sampled_pwl_to_file(self, filename="sampled_pwl.txt"):
        with open(filename, 'w') as out:
            for i in range(0,len(self.sampled_times)):
                out.write("%.12f %.12f\n" % 
                        (self.sampled_times[i], self.sampled_values[i]))

    def _lpf_dme(self, cutoff, order):
        RC = cutoff / (2*math.pi)
        if(order < 1):
            return

        for i,f in enumerate(self.fft_freq):
            h = 1 / ((complex(0,(f/(2*math.pi)))/RC)**order + 1)
            self.fft_value[i] = h * self.fft_value[i]

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


#generate eye diagrams from a 1d (y points only) array where data was sampled with
#the specified sample rate and the data bit(s) have the specified sample period
#t_domain_sigs is a list of time domain signals.  Each one will be added to the eye diagram
class eye_diagram(object):
    def __init__(self,
            t_domain_sigs,
            symbol_period=80e-9,
            sample_rate=1/81.92e6,
            node_number=0,
            imgDir="."):
        self.symbol_period=symbol_period
        self.sample_rate=sample_rate
        self.t_domain_sigs = t_domain_sigs
        self.number = node_number
        self.imgDir = imgDir
        self.imgfile =  os.path.join(imgDir, "eye%d.png" % self.number)
        self.slicefile =  os.path.join(imgDir, "slice%d.png" % self.number)
        self.nbins=320
        self.nbits=256
        self.bin_width=symbol_period/self.nbins
        self.bins   = [[] for x in range(self.nbins)]
        self.t_offset = 0
        self.xt = []
        self.yt = []
        self.amp_y = []
        self.amp_x = []
        self.heatmap = np.zeros(shape=(self.nbits, self.nbins))
        #self.average_yp = []
        #self.average_yn = []
        #self.average_x = []

        self.eye_area_0 = 0
        self.eye_area_1 = 1 
        self._make_eye()

    #wrap the signal around an 80ns period (time % 80ns)
    #chop period into 0.5ns bins
    #place samples in the bins
    #loop through the bins, find bin with lowest pk-pk value
    #look for the bin with the smallest peak to peak value, this is probably the 0 crossing area
    def _make_histogram_2d(self) -> None:
        self.bins   = [[] for x in range(self.nbins)]
        for sig in self.t_domain_sigs:
            t=0
            #make histogram of time domain signal wrapped around (modulo) symbol_period
            for i in range(0,len(sig)):
                tn = i * self.sample_rate
                if (tn - t) > self.symbol_period:
                   t+=self.symbol_period
                b = int((tn-t)/self.bin_width) 
                self.bins[b].append((tn-t,sig[i]))

        #look for the bin with the smallest peak to peak value, this is probably the 0 crossing area
        min_ptp=1e6 #an unreasonably big number...
        self.min_bin=0
        for b in range(len(self.bins)):
            (x,y) = np.ptp(self.bins[b],axis=0)
            if(y < min_ptp):
                min_ptp = y
                self.min_bin = b

        #move data from the bins into the eye-diagram output
        #the eye diagram output is a scatter plot so causality of each point is not very important
        #subtract min_bin*bin_width from the timepoint values to center the transition on 0ns
        #adding half of a bin to the offset keeps the bin centered and it looks nicer in the plot
        self.t_offset = self.bin_width*(self.min_bin+0.5)
        for i in range(0,len(self.bins)):
            index = (i+self.min_bin) % len(self.bins)
            for s in self.bins[index]:
                self.yt.append(s[1])
                time = s[0]-self.t_offset
                if(time < 0):
                    time+=self.symbol_period
                self.xt.append(time)

    def _digitize(self, vmax=1, vmin=-1, nbits=256, v=0) -> int:
        #move voltages to a 0 based system
        if(v >= vmax):
            return nbits-1
        if(v <= vmin):
            return 0
        vx = v - vmin
        vm = vmax - vmin
        vn = 0
        return int(nbits * vx / vm)

    def _measure_opening_area(self,start_index,end_index):
        opening = 0

        #for i in range(start_index,end_index):
        a2 = np.transpose(self.heatmap)
        asum = 0
        for i in range(start_index,end_index+1):
            #assumes that nonzero returns nonzero indicies in ascending order
            p = np.nonzero(a2[i][128:])
            n = np.nonzero(a2[i][:128])
            #print(i)
            #print(p)
            #print(p[0][0]+128)
            #print(n[0][-1])
            #exit(1)
            asum += (p[0][0]+128-n[0][-1])

        return(asum)

    def plot_eye(self, filename=None, saturation_level=12):
        #print(self.imgfile)
        if filename==None:
            filename=self.imgfile
        else:
            self.imgfile = filename
        f, eye = pyplot.subplots(1,1, figsize=(10, 10))  # Create a figure and an axes.
        s = "Node %d - toffset %.2fns" % (self.number, self.t_offset*1e9)
        eye.set_title(s)
        eye.imshow(self.heatmap, cmap='hot', origin='lower', vmin=0, vmax=saturation_level, aspect='auto')  # Plot more data on the axes...
        pyplot.savefig(filename)
        pyplot.close(f)

    def plot_slice(self, filename=None):
        print(self.slicefile)
        if filename==None:
            filename=self.slicefile
        f, eye = pyplot.subplots(1,1, figsize=(10, 10))  # Create a figure and an axes.
        s = "Node %d - Zero Crossing Slice - %.3fns/%.3fns" % (self.number,
                self.crossing1_width*1e9, self.crossing2_width*1e9)
        eye.set_title(s)
        eye.plot(range(self.nbins), self.zero_crossing_array)  # Plot more data on the axes...
        pyplot.savefig(filename)
        pyplot.close(f)

    def _measure_zero_crossing(self):
        #measure zero crossing widths

        #find the slice that should go the middle of the eye in the y direction
        zero_crossing_index = int(self.nbits/2)

        #add in the slices above and below to add some noise rejection
        self.zero_crossing_array = \
                  self.heatmap[zero_crossing_index + 0 ]\
                + self.heatmap[zero_crossing_index + 1 ]\
                + self.heatmap[zero_crossing_index - 1 ]

        #get the indicies of the non-zero elements
        a = np.nonzero(self.zero_crossing_array)

        #look for large gaps in the indicies
        #the two largest gaps should represent the eye openings
        b = np.diff(a[0])
        i1 = np.argmax(b)

        #invert the first gap measurement so the second can be easily found
        b[i1] *= -1
        i2 = np.argmax(b)
        b[i1] *= -1 #uninvert now that i2 has been found

        #make sure the vairable i1 represents the first eye opening
        if(i1 > i2):
            t = i1
            i1 = i2
            i2 = t

        #print(a[0])
        #print(b)
        #print("i1    %d" % i1)
        #print("b[i1] %d" % b[i1])
        #print("i2    %d" % i2)
        #print("b[i2] %d" % b[i2])

        self.index0 = a[0][i1]+1
        self.index1 = a[0][i1]+b[i1]-1
        self.index2 = a[0][i2]+1
        self.index3 = a[0][i2]+b[i2]-1

        #print("self.index0 : %d" % (self.index0) )
        #print("self.index1 : %d" % (self.index1) )
        #print("self.index2 : %d" % (self.index2) )
        #print("self.index3 : %d" % (self.index3) )

        self.crossing_time     = self.bin_width * (self.index2 + self.index1) / 2
        self.crossing_time_min = self.bin_width * self.index1
        self.crossing_time_max = self.bin_width * self.index2
        self.crossing1_width = self.bin_width * ((self.nbins - self.index3) + self.index0)
        self.crossing2_width = self.bin_width * (self.index2 - self.index1)
        #exit(1)


    def _make_eye(self):
        #generate a centered 2d histogram
        self._make_histogram_2d()
    
        vmax=0.75
        vmin=-0.75
        for i in range(0,len(self.bins)):
            index = (i+self.min_bin) % len(self.bins)
            for s in self.bins[index]:
                bin_y = self._digitize(vmax, vmin, self.nbits, s[1])
                self.heatmap[bin_y][i] += 1

        #determines 4 indicies indicating where the eyes open and close
        self._measure_zero_crossing()
        dig_area = self._measure_opening_area(self.index0, self.index1)
        self.eye_area_1 = dig_area * self.bin_width * ((vmax - vmin) / self.nbits)
        dig_area = self._measure_opening_area(self.index2, self.index3)
        self.eye_area_2 = dig_area * self.bin_width * ((vmax - vmin) / self.nbits)
        print("%.6e %.6e %6.3fnV*s : %6.3fnV*s" % (self.crossing1_width, self.crossing2_width,self.eye_area_1*1e9, self.eye_area_2*1e9))

    def getHtmlOutput(self):
        html = ""
        html += "<DIV class=content>\n"
        html += "<DIV class=main>\n"
        html += "<DIV class=simtitle>\n"
        html += \
            "<DIV class=simname><p class=label>%s %s</p></DIV>" \
            % ("Node", self.number)
        
        graphId = "node%d" % (self.number)
        html += "<p class=text><a onclick=\"toggleItem('%s')\" > show\
        images</a></p>" % graphId
        eye_plot = "eye%d.png" % self.number
        html += "<DIV id='%s' style='display:none'>" % graphId
        html += "<HR>"
        html += "<img src=\"img/%s\" alt=\"img/%s\" height=\"500\" width=\"500\"></img>" % (eye_plot, eye_plot)
        html += "<HR>"
        html += "</DIV></DIV></DIV></DIV>"
        return html


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
