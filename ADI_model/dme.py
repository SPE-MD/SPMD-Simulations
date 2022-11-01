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
from matplotlib.ticker import EngFormatter
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

class analog_filter_s_domain(object):
    #filter_type is 'hpf' or 'lpf', add butterworth, chebychev, etc later...
    def __init__(self, filter_type, cutoff=1e6, order=1):
        self.cutoff=cutoff
        self.order=order
        self.filter_type = filter_type
        self.poles = self._butterworth_poles(self.cutoff,self.order)

    def _butterworth_poles(self, cutoff, order):
        Wcutoff = (2*math.pi*cutoff)
        poles = []
        for k in range(1,order+1):
            poles.append(Wcutoff * np.exp(complex(0,((2*k)+order-1)*np.pi)/(2*order)))
        return poles

    def filter_fft(self, fft_freq, fft):
        if(self.filter_type.lower() == "hpf"):
            return self._hpf(fft_freq,fft)
        elif(self.filter_type.lower() == "lpf"):
            return self._lpf(fft_freq,fft)
        else:
            print("unknown filter type: %s" % self.filter_type)
            return self.fft

    def _hpf(self, fft_freq, fft):
        #print("HPF Filter Order %d, Cutoff %.3e" % (self.order, self.cutoff)) 
        if(self.order < 1):
            print("HPF order < 1 : %d " % self.order)
            return fft

        Wcutoff = (2*math.pi*self.cutoff)
        filtered = np.ones_like(fft,dtype=np.complex)
        for i,freq in enumerate(fft_freq):
            if(freq == 0):
                filtered[i] = complex(1e-30,0)
            else:
                w = freq * (2*math.pi)
                h=complex(1,0)
                for p in self.poles:
                    h *= complex(0,w)/(complex(0,w) + p)
                filtered[i] = h * fft[i]
        return filtered

    def _lpf(self, fft_freq, fft):
        #print("LPF Filter Order %d, Cutoff %.3e" % (self.order, self.cutoff)) 
        if(self.order < 1):
            print("LPF order < 1 : %d " % self.order)
            return fft

        Wcutoff = (2*math.pi*self.cutoff)
        filtered = np.ones_like(fft, dtype=np.complex)
        for i,freq in enumerate(fft_freq):
                w = freq * (2*math.pi)
                h=complex(1,0)
                for p in self.poles:
                    h *= Wcutoff / (complex(0,w) - p)
                filtered[i] = h * fft[i]
        return filtered

class dme_signal(object):
    def __init__(self):
        self.filters = []
        self.noise   = []
        self.transfer_functions = []
        #self.fft_value = []
        #self.fft_freq  = []
        #self.t_domain_mdi = None
        #self.t_domain_filtered = None

    def add_transfer_function(self, tf, label):
        self.transfer_functions.append({'tf':tf, 'label': label})

    def plot_transfer_functions(self,filename='tf.png', title='Tranfer Functions'):
        f, plt = pyplot.subplots(1,1, figsize=(10, 10))  # Create a figure and an axes.
        plt.set_title(title)
        plt.set_ylim([-50,50])
        plt.set_xlim([0,50e6])
        plt.xaxis.set_major_formatter(EngFormatter(unit = 'Hz'))
        #plt.set_xscale("log")
        for x in self.transfer_functions:
            plt.plot(self.fft_freq[1:], 20*np.log10(np.abs(x['tf'][1:])), label=x['label'])
        plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=2)  # Add a legend.
        pyplot.savefig(filename)
        pyplot.close(f)

    def add_filter(self,filter_type="lpf",cutoff=20e6,order=1):
        if(len(self.filter)==0):
            self.filter = np.ones_like(self.fft_freq,dtype=np.complex)
            print("#Creating Filter Container")
        self.filters.append(analog_filter_s_domain(filter_type, cutoff, order))
        self.filter = self.filters[-1].filter_fft(self.fft_freq, self.filter)

    def tx_psd_upper_limit(self,freq):
        lim = np.ones_like(freq)
        for i in range(freq.size):
            lim[i] = self._tx_ul(freq[i])
            #print("%.3e %.3e" % (freq[i], lim[i]))
        return lim

    def tx_psd_lower_limit(self,freq):
        lim = np.ones_like(freq)
        for i in range(freq.size):
            lim[i] = self._tx_ll(freq[i])
        return lim

    #piecewise linear description of transmitter upper limit PSD
    def _tx_ul(self,f):
        if(f < 0.3e6):
            return np.nan
        elif(f < 15e6):
            return -61
        elif(f < 25e6):
            return (-40-(1.4*(f/1e6)))
        elif(f < 40e6):
            return -75
        else:
            return np.nan

    #piecewise linear description of transmitter upper limit PSD
    def _tx_ll(self,f):
        if(f < 5e6):
            return np.nan
        elif(f < 10e6):
            return -87+(2*(f/1e6))
        elif(f <= 15e6):
            return -47-(2*(f/1e6))
        else:
            return np.nan


    def add_white_noise(self,noise_dBm_per_hz,noise_bandwidth):
        #get a the frequency step so noise can be spread across the spectrum
        df = self.fft_freq[1]-self.fft_freq[0]
       
        #dBm to Vrms (R=50Ohms):
        #dBm = 10*log10((Vrms^2/R)/0.001)
        #dBm = 20*log10(Vrms) - 10*log10(R) + 10*log10(1/0.001)
        #dBm = dBm/Hz + 10*log(noise_bandwidth)
        #-101 dBm/Hz at 40MHz Bandwidth = ~13mVrms

        #unwind the equations above to find Vrms noise levels per fft step (noise in 20kHz por ejemplo) 
        #noise as Vrms/Hz should be integrated as a root-sum-square to get final Vrms value
        #what is the factor of 1.83? I found it empirically.
        #1.83 = 10**(5.25/20) =  what is 5.25?? 
        nl_f = 1.83*np.sqrt(noise_bandwidth) * 10 ** ((noise_dBm_per_hz + 10*np.log10(df) - 30 + 10*np.log10(50))/(20)) 
        #(10*np.log10(np.abs(V)**2/50) + 30 - 10*np.log10(df*40e6)))
        #10**(-71/20) * 10**(10*log10(df))
        #nl_f = np.sqrt(df*1.99e-5)
        #print(nl_f)
        #print(df)

        #generate an array of random phases
        ph  = np.random.uniform(0,2*np.pi,len(self.fft_freq))
        mag = np.random.normal(0,nl_f,len(self.fft_freq))
        #add the real part (noise voltage) to the phases
        #print(nl_f)
        self.noise = np.full_like(self.fft_freq, nl_f, dtype='complex') 
        #change mag,angle into real,imag...
        #with open("noise_fft_j.txt", 'w') as out:
        #    for i in range(0,len(self.fft_freq)):
        #        out.write("%.12e %.12e\n" % 
        #                (self.fft_freq[i], np.real(self.noise[i])))

        for i in range(len(self.noise)):
            if(self.fft_freq[i] < noise_bandwidth):
                self.noise[i] = mag[i] * np.exp(1j*ph[i])
                #self.noise[i] = mag[i] * np.exp(0)
            else:
                self.noise[i] = complex(10e-31,0)

        self.noise[0] = complex(10e-31,0)

        #with open("noise_fft.txt", 'w') as out:
        #    for i in range(0,len(self.fft_freq)):
        #        out.write("%.12e %.12e %.12e\n" % 
        #                (self.fft_freq[i],
        #                    20*math.log10(np.abs(self.noise[i])),
        #                    np.angle(self.noise[i])
        #                    )
        #                )

        n_t = np.fft.irfft(self.noise)
        #print("Rms Noise: %e" % np.std(n_t))
        #with open("noise_%d.txt" % self.node.number, 'w') as out:
        #    for x in n_t:
        #        out.write("%.12e\n" % x)


    def get_filtered_fft(self):
        #self.filter = np.ones_like(self.fft_freq,dtype=np.complex)
        #for f in self.filters:
        #    self.filter = f.filter_fft(self.fft_freq, self.filter)
        self.fft_filtered = np.ones_like(self.fft_freq,dtype=np.complex)
        for i in range(self.filter.size):
            self.fft_filtered[i] = self.fft_value[i] * self.filter[i]
        return self.fft_filtered

    def process_mdi_data(self):
        self.eye_mdi = self.process_data(self.t_domain_mdi, filename="eye_mdi")

    def process_filtered_data(self):
        self.eye_filtered = self.process_data(self.t_domain_filtered,filename="eye_filtered")

    def process_data(self,t_domain,filename="eye"):
        #print(filename)
        eye = eye_diagram(
                [t_domain],
                [self.dme_transmitter],
                self.symbol_period,
                self.sample_period,
                node_number=self.node.number,
                imgDir=self.imgDir,
                filename=filename
                )

        min_corr_value_list = []
        #for i in range(0,len(self.t_domain_filtered)):
        self.corr_data_txt =  os.path.join(self.imgDir,("corr_data_%d.txt" % self.node.number))
        dc = dme_correlator(t_domain, self.sample_period,
                eye.t_offset, self.dme_transmitter, filename=self.corr_data_txt)

        self.corrpng =  os.path.join(self.imgDir,("corr_node_%d.png" % self.node.number))
        dc.plot_correlation(filename=self.corrpng, title=("Correlation Node %d" % self.node.number))
        min_corr_value_list.append(dc.min_corr_value)
        self.min_corr_value = np.amin(min_corr_value_list)
        print("%2d %.6e %.6e %6.3fnV*s : %6.3fnV*s %5.3f" % (
            self.node.number,
            eye.crossing1_width,
            eye.crossing2_width,
            eye.eye_area_1*1e9,
            eye.eye_area_2*1e9,
            self.min_corr_value))

        return eye

    def plot_filter(self, filename="filter.png", title='filter', xmax=None):
        f, plt = pyplot.subplots(1,1, figsize=(10, 10))  # Create a figure and an axes.
        plt.set_title(title)
        if(xmax):
            plt.set_xlim([self.fft_freq[1],xmax])
        plt.set_xscale("log")
        plt.plot(self.fft_freq[1:], 20*np.log10(np.abs(self.filter[1:])))
        pyplot.savefig(filename)
        pyplot.close(f)

    def plot_fft(self, filename="filter.png", title='fft'):
        f, plt = pyplot.subplots(1,1, figsize=(10, 10))  # Create a figure and an axes.
        plt.set_title(title)
        plt.set_xlim([0,50e6])
        plt.set_ylim([-120,-50])
        #plt.set_ylim([-50,20])
        #plt.set_xscale("log")
        #dBm = 20*log10(Vrms) - 10*log10(R) + 10*log10(1/0.001)
        df=self.fft_freq[1]-self.fft_freq[0]
        plt.plot(self.fft_freq[1:], (10*np.log10(np.abs(self.fft_filtered[1:])**2/50) +30 - 10*np.log10(40e6) - 10*np.log10(df)))
        plt.plot(self.fft_freq[1:], (10*np.log10(np.abs(self.noise[1:])**2/50)        +30 - 10*np.log10(40e6) - 10*np.log10(df)))
        plt.plot(self.fft_freq[1:], self.tx_psd_upper_limit(self.fft_freq[1:]))
        plt.plot(self.fft_freq[1:], self.tx_psd_lower_limit(self.fft_freq[1:]))
        print(np.median((10*np.log10(np.abs(self.noise[1:60])**2/50)        +30 - 10*np.log10(40e6) - 10*np.log10(df))))
        pyplot.savefig(filename)
        pyplot.close(f)

    def output_filter_to_file(self, filename="filter.txt"):
        with open(filename, 'w') as out:
            for i in range(0,len(self.fft_freq)):
                out.write("%.12e %.12e %.12e\n" % 
                        (self.fft_freq[i],
                            20*math.log10(np.abs(self.filter[i])),
                            np.angle(self.filter[i])
                            )
                        )

    def output_t_domain_to_file(self, filename="t_domain.txt"):
        with open(filename, 'w') as out:
            out.write("#time t_domain_mdi t_domain_filtered\n")
            for i in range(0,len(self.fft_freq)):
                out.write("%.12e %.12e %.12e\n" % 
                        (i * self.sample_period,
                            self.t_domain_mdi[i],
                            self.t_domain_filtered[i]))


class dme_transmitter(dme_signal):
    def __init__(self,ts=1/81.92e6,ns=8192,symbol_period=80e-9,n_symbols=1253,amplitude=0.5,zin=None):
        super(dme_transmitter, self).__init__()
        self.sample_period = ts #1/81.92e6
        self.ns = ns #8192
        self.symbol_period=symbol_period
        self.tstop=ts*ns 
        self.n_symbols=n_symbols
        self.amp=amplitude
        self.zin=zin
        self.tstop=ts*ns 

        self._generateRandomBits()
        self.filter = np.ones_like(self.fft_freq,dtype=np.complex)

    def _generateRandomBits(self):
        self.pattern = np.random.randint(2,size=self.n_symbols)
        self.pattern[0]=1
        self.pattern[-1]=0
        
        self.trise=10e-9 #make this an input parameter
        self.pwl = ["0 %.3f" % self.amp]
        t0 = 0

        #build up a piece wise linear version of the DME signal
        tflat = (self.symbol_period-(4*self.trise))/2
        for i in self.pattern:
            x = i * self.amp * 2
            self.pwl.append("%.12f %.2f" % (t0 +  self.trise           , x-self.amp))
            self.pwl.append("%.12f %.2f" % (t0 + (self.trise+tflat)    , x-self.amp))
            self.pwl.append("%.12f %.2f" % (t0 + (3*self.trise+1*tflat)  ,
                -self.amp+(2*self.amp*(1-i))))
            self.pwl.append("%.12f %.2f" % (t0 + (3*self.trise+2*tflat),
                -self.amp+(2*self.amp*(1-i))))
            t0 += self.symbol_period

        #pass the piece wise linear version of the DME signal to pwl_wave
        #use pwl_wave methods to get interpolated samples of the DME signal
        self.pwl_wave = pwlWave()
        self.pwl_wave.buildPwlFromText(self.pwl)

        #sample the pwl_wave based on the 1/self.ts passed to this method
        self._sample_dme()

        #make an FFT of the sampled signal
        self._fft_dme()

        #if the complex input impedance of a transmission line is passed to this
        #method modify the fft value by that impedance
        if(self.zin):
            self.fft_value = self.zin * self.fft_value

    def _sample_dme(self):
        self.sampled_times  = []
        self.t_domain_mdi = []
        for i in range(0,self.ns):
            tx = i * self.sample_period
            self.sampled_times.append(tx)
            self.t_domain_mdi.append(self.pwl_wave.pwlTimes(tx))

    def _fft_dme(self):
        values = np.array(self.t_domain_mdi, dtype=float)
        self.fft_value = np.fft.rfft(values)
        self.fft_freq  = np.fft.rfftfreq(n=values.size, d=self.sample_period)

    def output_pwl_to_file(self, filename="pwl.txt"):
        with open(filename, 'w') as out:
            for p in self.pwl:
                out.write("%s\n" % p)

    def output_sampled_pwl_to_file(self, filename="sampled_pwl.txt"):
        with open(filename, 'w') as out:
            for i in range(0,len(self.sampled_times)):
                out.write("%.12f %.12f\n" % 
                        (self.sampled_times[i], self.t_domain_mdi[i]))


#compare a dme wave, symbol by symbol, to an ideal symbol to recover data
class dme_receiver(dme_signal):
    def __init__(self, node, dme_transmitter, imgDir):
        super(dme_receiver, self).__init__()
        self.node = node
        self.dme_transmitter=dme_transmitter
        self.symbol_period=dme_transmitter.symbol_period
        self.sample_period=dme_transmitter.sample_period
        self.imgDir = imgDir #directory for graph outputs

        self.fft_freq = dme_transmitter.fft_freq
        self.filter = np.ones_like(self.fft_freq,dtype=np.complex)
        self.t_domain_mdi      = None
        self.t_domain_filtered = None

        #hold refs to input dme signals for comparison after rx
        self.eye=None

    #fft representing a signal at the input of this node.
    def rx_fft(self, fft):
        self.fft_value = fft
        if(len(self.noise)):
            #numpy arrays add element by element with this notation
            self.fft_value += self.noise
        self.t_domain_mdi      = (np.fft.irfft(fft))
        self.fft_value_filtered = self.get_filtered_fft()
        #if(len(self.noise)):
        #    #numpy arrays add element by element with this notation
        #    self.fft_value_filtered += self.noise
        self.t_domain_filtered = np.fft.irfft(self.fft_value_filtered)

class dme_correlator(object):
    def __init__(self, t_domain_dme, ts, delay=0, dme_input=None, filename='dme_wave.txt'):
        #make an ideal symbol for correlation of received signals
        self.filename = filename
        self.corr_pwl =     ["0.0 1.0"]
        self.corr_pwl.append("39.999e-9 1")
        self.corr_pwl.append("40.001e-9  -1")
        self.corr_pwl.append("80e-9      -1")
        self.corr_wave = pwlWave()
        self.corr_wave.buildPwlFromText(self.corr_pwl)

        period_last = -1000
        period      = -999
        csum=0
        ccount=-1
        self.corr_avg = []
        corr_count = []
        recovered = []
        corr_ratio = 0
        i=0
        with open(filename, 'w') as dme:
            dme.write("#%s %s %s %s %s %s %s %s %s %s %s\n" % 
                    ("time", " x", " dme_input.t_domain_mdi[i]", "sl", "c", "period",
                        "corr_meas", "offset_time", "csum", "ccount", "index>length"))
            #print(delay)
            length = len(t_domain_dme)
            stop   = length
            index=0
            #going 1 past 'stop' makes sure the last bit is fully interpreted
            while(index<=stop+1):
                i=index%length
                x=t_domain_dme[i]
                sl = -1
                if x > 0:
                    sl = 1
                time=(index*ts)
                offset_time = (time-delay-40e-9)
                period = math.floor((time-delay-40e-9)/80e-9)
                #align the 'perfect' correlator signal with the recovered data
                #subtracting delay here makes the clock transitions line up on
                # the 80ns marks
                c = self.corr_wave.pwlTimes(time-delay-40e-9)
                corr_meas = abs(sl-c)
                if(period != period_last and ccount>0):
                    corr_ratio = (csum/ccount) - 1.0

                    rec = -1
                    if(corr_ratio >= 0.0):
                        rec=1
                    else:
                        rec=0

                    #this section ignores partial bits at the beginning
                    #by detecting if there were too few samples for the period
                    #to have changed
                    #if there is a partial bit increase the 'stop' threshold by
                    #parital count and the partial bit will be picked up as part
                    #of the last bit
                    if(ccount>=math.floor(80e-9/ts)-1):
                        recovered.append(rec)
                        corr_count.append(ccount)
                        self.corr_avg.append(abs(corr_ratio))
                    else:
                        #print("Period %d : Stop ADDED %d,%d" % (period,ccount,math.floor(80e-9/ts)-1))
                        stop+=ccount
                    dme.write("\n")
                    period_last = period
                    csum=0
                    ccount=0
                csum+=corr_meas
                ccount+=1
                #output some data for verification / debugging
                dme.write("% .12f % .12f % .12f % d % d % d % d % .12f % .12f %d %s\n" % 
                        (time, x, dme_input.t_domain_mdi[i],sl,c,period,
                        corr_meas, offset_time, csum, ccount, (index>length) ))

                index+=1
            dme.write("#%s %s %s %s %s %s %s %s %s %s %s\n" % 
                    ("time", " x", " dme_input.t_domain_mdi[i]", "sl", "c", "period",
                        "corr_meas", "offset_time", "csum", "ccount", "index>length"))


        if(0):
            for i in range(len(recovered)):
                if(self.corr_avg[i] < 0.6):
                    print("Bad Correlation: %04d %5.3f %d %d %d" %
                        (i,self.corr_avg[i],dme_input.pattern[i],recovered[i],corr_count[i]))

        #print("delay = %e" % delay)
        #print("min=%e" % np.amin(corr_avg))
        self.min_corr_value = np.amin(self.corr_avg)

    def plot_correlation(self, filename="corr.png", title='Correlation'):
        f, plt = pyplot.subplots(1,1, figsize=(10, 3))  # Create a figure and an axes.
        plt.set_title(title)
        #plt.set_xscale("log")
        plt.plot(range(len(self.corr_avg)), self.corr_avg)
        pyplot.savefig(filename)
        pyplot.close(f)

#generate eye diagrams from a 1d (y points only) array where data was sampled with
#the specified sample rate and the data bit(s) have the specified sample period
#t_domain_sigs is a list of time domain signals.  Each one will be added to the eye diagram
class eye_diagram(object):
    def __init__(self,
            t_domain_sigs,
            dme_signals,
            symbol_period=80e-9,
            sample_period=1/81.92e6,
            node_number=0,
            imgDir=".",
            filename='eye'
            ):
            
        self.symbol_period=symbol_period
        self.sample_period=sample_period
        self.t_domain_sigs = t_domain_sigs
        self.number = node_number
        self.imgDir = imgDir
        self.imgfile =  os.path.join(imgDir, "%s%d.png" % (filename,self.number))
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
        self.filename = filename
        self.node_number=node_number
        #self.average_yp = []
        #self.average_yn = []
        #self.average_x = []

        self.eye_area_0 = 0
        self.eye_area_1 = 1 
        self._make_eye()

        min_corr_value_list=[]

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
                tn = i * self.sample_period
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
