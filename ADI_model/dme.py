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
import matplotlib
import mpUtil
from ltcsimraw import ltcsimraw as ltcsimraw

matplotlib.use('Agg') 
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

class analog_filter_raw_file(object):
    def __init__(self, rawfile, n2, n1):
        rf=ltcsimraw(rawfile)
        self.filter = rf.ac_gain(n1, n2)
        #return self.av

    def filter_fft(self, fft_freq, fft):

        filtered = np.ones_like(fft, dtype=np.complex)
        #print(self.filter['av'])
        try:
            for i,freq in enumerate(fft_freq):
                if(freq == 0):
                    pass
                    #filtered[i] = complex(1e-30,0)
                else:
                    filtered[i] = self.filter['av'][i-1] * fft[i]
        except Exception as e:
            print(e)
            print(i)
        return filtered

class dme_signal(object):
    def __init__(self):
        self.filters = []
        self.noise   = []
        self.transfer_functions = []
        self.pattern_delay = 0
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

    def add_filter_from_file(self,rawfile=None,node2='n2',node1='n1'):
        #print("HI!! FILTER FROM FILE")
        if(len(self.filter)==0):
            self.filter = np.ones_like(self.fft_freq,dtype=np.complex)
            print("#Creating Rawfile Filter Container")
        self.filters.append(analog_filter_raw_file(rawfile,node2,node1))
        self.filter = self.filters[-1].filter_fft(self.fft_freq,self.filter)

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
        self.eye = eye_diagram(
                [t_domain],
                [self.dme_transmitter],
                self.symbol_period,
                self.sample_period,
                node_number=self.node_number,
                imgDir=self.imgDir,
                filename=filename
                )

        corr_value_list = []
        #for i in range(0,len(self.t_domain_filtered)):
        self.corr_data_txt =  os.path.join(self.imgDir,("corr_data_%d.txt" %
            self.node_number))
        dc = dme_correlator(t_domain, self.sample_period, symbol_period=self.symbol_period,
                delay=self.eye.t_offset, dme_input=self.dme_transmitter, filename=self.corr_data_txt)

        #match the tx and rx patterns and figure out the time delay to the pattern
        self.pattern_offset_periods = self.find_pattern_delay(self.dme_transmitter.pattern,dc.recovered_bit_pattern)
        self.pattern_delay = self.pattern_offset_periods['offset'] * self.symbol_period #+ eye.t_offset
        #print(pattern_offset_periods['offset'] * 80e-9 + eye.t_offset)

        self.corrpng =  os.path.join(self.imgDir,("corr_node_%d.png" %
            self.node_number))
        #dc.plot_correlation(filename=self.corrpng, title=("Correlation Node %d"
        #    % self.node_number))
        corr_value_list.append(dc.min_corr_value) #why putting this in a list?
        self.min_corr_value = np.amin(corr_value_list)
        self.avg_corr_value = dc.avg_corr_value #avg_corr_value being treated differently than min_corr_value
        self.min_corr_period = dc.min_corr_period
        self.receive_delay = self.eye.t_offset + self.pattern_delay + (self.symbol_period/2)
        
        return self.eye

    def processed_data_summary_label_list(self):
        return([
            "%4s"  % "node",
            "%10s" % "crossing1",
            "%10s" % "crossing2",
            "%9s"  % "eye_area1",
            "%9s"  % "eye_area2",
            "%8s"  % "min_corr",
            "%8s"  % "avg_corr",
            "%12s" % "min_corr_per",
            "%9s"  % "o_periods",
            "%10s" % "eye_offset",
            "%13s" % "pattern_delay",
            "%13s" % "receive_delay"
            ]
            )

    def processed_data_summary_list(self):
        return([
            "%04d"    % self.node_number,
            "%8.3fns" % (self.eye.crossing1_width*1e9),
            "%8.3fns" % (self.eye.crossing2_width*1e9),
            "%9.3f"   % (self.eye.eye_area_1*1e9),
            "%9.3f"   % (self.eye.eye_area_2*1e9),
            "%8.3f"   % self.min_corr_value,
            "%8.3f"   % self.avg_corr_value, 
            "%12d"    % self.min_corr_period, 
            "%9d"     % self.pattern_offset_periods['offset'],
            "%10.3e"  % self.eye.t_offset,
            "%11.fns" % (self.pattern_delay*1e9),
            "%11.3fns"% ((self.eye.t_offset + self.pattern_delay+40e-9)*1e9)
            ]
            )

    def find_pattern_delay(self,tx_bit_pattern,rx_bit_pattern):
        #need to do a proper cast to numpy for array comparison, but I am doing
        #this on the plane - so no access to numpy manuals...
        matched = False
        short_match_length = 20
        #print(rx_bit_pattern[0:short_match_length])
        for i in range(len(tx_bit_pattern)-short_match_length):
            #do a short comparison before committing to the full pattern match
            compare = tx_bit_pattern[0:short_match_length] ==\
            rx_bit_pattern[i:i+short_match_length]
            if(not False in compare):
                #print(tx_bit_pattern[0:short_match_length])
                #print(rx_bit_pattern[i:i+short_match_length])
                matched=True
                break
        return {'matched':matched, 'offset' : i}

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
        #print("Median Noise Level: %5.1f" % np.median((10*np.log10(np.abs(self.noise[1:60])**2/50)        +30 - 10*np.log10(40e6) - 10*np.log10(df))))
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

    def output_tx_ifft_to_file(self, filename="tx_ifft.txt"):
        with open(filename, 'w') as out:
            out.write("#time t_domain_mdi t_domain_filtered\n")
            o = np.fft.irfft(self.fft_value)
            for i in range(0,len(self.fft_freq)):
                out.write("%.12e %.12e\n" % 
                        (i * self.sample_period, o[i])
                        )


class dme_transmitter(dme_signal):
    def __init__(self,ts=1/81.92e6,ns=8192,symbol_period=80e-9,n_symbols=1253,amplitude=0.5,zin=None,wake_signal=False):
        super(dme_transmitter, self).__init__()
        self.sample_period = ts #1/81.92e6
        self.ns = ns #8192
        self.symbol_period=symbol_period
        self.tstop=ts*ns 
        self.n_symbols=n_symbols
        self.amp=amplitude
        self.zin=zin
        self.tstop=ts*ns 

        self._generateWakeSignal()
        self._generateRandomBits(all_ones=wake_signal)
        self.filter = np.ones_like(self.fft_freq,dtype=np.complex)

    def _scrambler(self,pattern):
        scrambler = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        scrambled = []
        dl = 0
        dout_last=0
        x=0
        state=0
        dme_or=0
        
        for i in pattern:
            #state1

            #0
            dl = (0|dout_last) ^ dl
            dme_out = (~dl) & 0x01
            #1
            dout = i ^ scrambler[16] ^ scrambler[13]
            scrambler.pop()
            scrambler.insert(0,dout)
            dl = (1|dout) ^ dl
            dme_out2 = (~dl) & 0x01
            if(x<30):
                print("%03d %d %d %d %d" % (x, dout, dl, dme_out, dme_out2))
            scrambled.append(dme_out) 
            dout_last=dout
            x+=1
        return scrambled

    def _generateWakeSignal(self):

        wake_period=1.6e-6
        self.trise=10e-9 #make this an input parameter
        self.pwl = ["0 0"]
        tflat = (wake_period-(4*self.trise))/2
        t0 = 15.1e-6
        self.pwl.append("%.12f 0" % t0)
        for i in range(12):
            b = 0
            x = b * self.amp * 2
            self.pwl.append("%.12f %.2f" % (t0 +  self.trise           , x-self.amp))
            self.pwl.append("%.12f %.2f" % (t0 + (self.trise+tflat)    , x-self.amp))
            self.pwl.append("%.12f %.2f" % (t0 + (3*self.trise+1*tflat)  ,
                -self.amp+(2*self.amp*(1-b))))
            self.pwl.append("%.12f %.2f" % (t0 + (3*self.trise+2*tflat),
                -self.amp+(2*self.amp*(1-b))))
            t0 += wake_period
        self.pwl.append("%.12f 0" % t0)
        t0 += 15.1e-6
        self.pwl.append("%.12f 0" % t0)

    def _generateRandomBits(self,all_ones=False):
        #self.pattern = np.random.randint(2,size=self.n_symbols)
        self.pattern = np.zeros(self.n_symbols,dtype=np.int8)
        #self.pattern[::2] = 0
        #self.pattern[1::2] = 1
        print(self.pattern)
        self.pattern = self._scrambler(self.pattern)
        #self.pattern[0]=0
        #self.pattern[-1]=1
        print(self.pattern)
        #exit(1)
        #print(len(self.pattern))
        if(all_ones):
            #self.pattern = np.empty(self.n_symbols)
            #self.pattern[::2] = 0
            #self.pattern[1::2] = 1
            self.pattern = np.ones(self.n_symbols,dtype=np.int8)
            self.pattern[0:100] = 1
            self.pattern[101:] = 0
            print(self.pattern)
            print(len(self.pattern))
        
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

        if(all_ones):
            self._generateWakeSignal()

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
            #zl = 0+12e3j
            #zc = 0-48e3j
            #r = 20e3
            #zf = (1/((1/zl)+(1/zc)+(1/r)))
            #print(zf)
            #print(np.abs(zf))
            #print(np.absolute(zf))
            #print(np.angle(zf)*180/np.pi)
            #z_norton = 100 + 0j
            z = np.array(self.zin)
            #zx=[]
            #for i in range(len(z)):
            #    zx.append(1/((1/z_norton)+(1/z[i])))
            self.fft_value = z * self.fft_value
            #self.output_zin_to_file(self.zin,zx)



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

    def output_zin_to_file(self, z1, z2, filename="zin.txt"):
        with open(filename, 'w') as out:
            for x in range(len(z1)):
                out.write("%g %g %g %g\n" % (np.absolute(z1[x]),
                    np.angle(z1[x])*180/np.pi,
                    np.absolute(z2[x]), np.angle(z2[x])*180/np.pi))

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
    def __init__(self, node_number, dme_transmitter, imgDir):
        super(dme_receiver, self).__init__()
        #self.node = node
        self.node_number = node_number
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
    def __init__(self, t_domain_dme, ts, symbol_period=80e-9, delay=0, dme_input=None, filename='dme_wave.txt'):
        #make an ideal symbol for correlation of received signals
        self.filename = filename
        self.symbol_period=symbol_period
        self.corr_pwl =     ["0.0 1.0"]
        #print(self.symbol_period)
        #print((self.symbol_period/2) - 1e-12)

        self.corr_pwl.append("%g  1" % ((self.symbol_period/2) - 1e-12))
        self.corr_pwl.append("%g -1" % ((self.symbol_period/2) + 1e-12))
        self.corr_pwl.append("%g -1" % self.symbol_period)
        self.corr_wave = pwlWave()
        self.corr_wave.buildPwlFromText(self.corr_pwl)

        self.corr_pwl0 =     ["0.0 0.0"]
        self.corr_pwl0.append("%g  0" % ((self.symbol_period/2) - 1e-12))
        self.corr_pwl0.append("%g  1" % ((self.symbol_period/2) + 1e-12))
        self.corr_pwl0.append("%g  1" % self.symbol_period)
        self.corr_wave0 = pwlWave()
        self.corr_wave0.buildPwlFromText(self.corr_pwl0)

        self.corr_pwl1 =     ["0.0 1.0"]
        self.corr_pwl1.append("%g  1" % ((self.symbol_period/2) - 1e-12))
        self.corr_pwl1.append("%g  0" % ((self.symbol_period/2) + 1e-12))
        self.corr_pwl1.append("%g  0" % self.symbol_period)
        self.corr_wave1 = pwlWave()
        self.corr_wave1.buildPwlFromText(self.corr_pwl1)

        #self.corr_mask_pwl =     ["0.0 0.0"]
        #self.corr_mask_pwl.append("19.999e-9 0" % ((bit_per/4) - 1e-12))
        #self.corr_mask_pwl.append("20.000e-9 1" % ((bit_per/4) + 1e-12))
        #self.corr_mask_pwl.append("29.999e-9 1")
        #self.corr_mask_pwl.append("30.000e-9 0")
        #self.corr_mask_pwl.append("59.999e-9 0")
        #self.corr_mask_pwl.append("60.000e-9 1")
        #self.corr_mask_pwl.append("69.999e-9 1")
        #self.corr_mask_pwl.append("70.000e-9 0")
        #self.corr_mask_pwl.append("80.000e-9 0")
        #self.corr_mask = pwlWave()
        #self.corr_mask.buildPwlFromText(self.corr_mask_pwl)

        self.min_corr_period = -1000
        self.min_corr_value = 10

        #resample t_domain_dme
        resample_freq = 1000e6
        resample_period = 1/resample_freq
        #resample_period = ts
        dme_pwl = []
        t=0
        for x in t_domain_dme:
            dme_pwl.append("%.12g %.12g" % (t,x))
            t+=ts
        self.resample_dme = pwlWave()
        self.resample_dme.buildPwlFromText(dme_pwl)
        #print(dme_pwl[-1])
        tlast = t-ts

        resampled = []
        t=0
        while t<tlast:
            resampled.append(self.resample_dme.pwlTimes(t))
            t+=resample_period
        #exit(1)

        period_last = -1e9
        period      = -1e9+1
        csum=0
        csum0=0
        csum1=0
        ccount=-1
        self.corr_avg = []
        corr_count = []
        rx_len = len(dme_input.pattern)
        #print(rx_len)
        #self.pattern = np.random.randint(2,size=self.n_symbols)
        self.recovered_bit_pattern = np.zeros_like(dme_input.pattern)
        corr_ratio = 0
        i=0
        with open(filename, 'w') as dme:
            dme.write("%15s %15s %17s %5s %8s %6s %9s %15s %4s %6s %12s\n" % 
                    ("time", " x", "t_domain_mdi[i]", "slice", "corr_ref", "period",
                        "corr_meas", "offset_time", "csum", "ccount", "index>length"))

            #print(delay)
            signal = t_domain_dme
            time_step = ts
            if(True):
                signal = resampled
                time_step = resample_period
            #print(ts)
            #print(resample_period)
            length = len(signal)
            stop   = length
            index=0
            #going 1 past 'stop' makes sure the last bit is fully interpreted
            bit_index=0
            #print("delay: %.3f" % (delay*1e9))
            ##bound delays within +-40ns of 0 time
            if(delay > self.symbol_period/2):
                delay-=self.symbol_period
            #print("delay: %.3f" % (delay*1e9))

            #print("%d %g %g" % (math.floor(self.symbol_period/time_step),self.symbol_period,time_step))

            while(index<=stop+1):
                i=index%length
                x=signal[i]
                sln = 0
                if x > 0.0:
                    sln = 1

                sl = -1
                if x > 0:
                    sl = 1
                time=(index*time_step)
                offset_time = (time-delay+(self.symbol_period/2))
                period = math.floor(offset_time/self.symbol_period)
                #align the 'perfect' correlator signal with the recovered data
                #subtracting delay here makes the clock transitions line up on
                # the 80ns marks
                c = self.corr_wave.pwlTimes(offset_time)
                c0 = int(self.corr_wave0.pwlTimes(offset_time))
                c1 = int(self.corr_wave1.pwlTimes(offset_time))
                #m = self.corr_mask.pwlTimes(offset_time)
                corr_meas = abs(sl-c)
                corr_meas0 = sln ^ c0
                corr_meas1 = sln ^ c1
                if(period != period_last and ccount>0):

                    rec = -1
                    if(True):
                        corr_ratio = (csum/ccount)-1.0
                        if(corr_ratio >= 0.0):
                            rec=1
                        else:
                            rec=0
                    else:
                        corr_ratio = ((csum/2.)/ccount)
                        if(corr_ratio >= 0.5):
                            rec=1
                        else:
                            rec=0

                    #this section ignores partial bits at the beginning
                    #by detecting if there were too few samples for the period
                    #to have changed
                    #if there is a partial bit increase the 'stop' threshold by
                    #parital count and the partial bit will be picked up as part
                    #of the last bit
                    if(ccount>=math.floor(self.symbol_period/time_step)-1):
                        self.recovered_bit_pattern[bit_index] = rec
                        corr_count.append(ccount)
                        crr = abs(corr_ratio)
                        #if(crr < 0.5):
                        #    crr = 1-crr
                        self.corr_avg.append(crr)
                        if crr < self.min_corr_value:
                            self.min_corr_period = bit_index
                            self.min_corr_value = crr
                        bit_index +=1
                    else:
                        #print("Period %d : Stop ADDED %d,%d" % (period,ccount,math.floor(80e-9/time_step)-1))
                        dme.write("#not_stored\n")
                        stop+=ccount
                    dme.write("\n")
                    period_last = period
                    csum=0
                    ccount=0
                    csum0=0
                    csum1=0
                csum+=corr_meas
                csum0+=corr_meas0
                csum1+=corr_meas1
                ccount+=1
                #output some data for verification / debugging
                try:
                    dme.write("% 15.12f % 15.12f % 17.12f % 5d % 8d % 6d % 9d % 15.12f %4d %6d %12s %d %3d %d %3d %d\n" % 
                            #(time, x, dme_input.t_domain_mdi[i],sl,c,period,
                            (time, x, -999,sl,c,period,
                            corr_meas, offset_time, csum, ccount,
                            (index>length),
                            sln, csum0, corr_meas0, csum1, corr_meas1))
                except Exception as e:
                    print("index = %d" % i)
                    print(e)

                index+=1
            dme.write("%15s %15s %17s %5s %8s %6s %9s %15s %4s %6s %12s\n" % 
                    ("time", " x", "t_domain_mdi[i]", "slice", "corr_ref", "period",
                        "corr_meas", "offset_time", "csum", "ccount", "index>length"))


        if(0):
            for i in range(len(self.recovered_bit_pattern)):
                if(self.corr_avg[i] < 0.6):
                    print("Bad Correlation: %04d %5.3f %d %d %d" %
                        (i,self.corr_avg[i],dme_input.pattern[i],self.recovered_bit_pattern[i],corr_count[i]))

        #print("delay = %e" % delay)
        #print("min=%e" % np.amin(corr_avg))
        #self.min_corr_value = np.amin(self.corr_avg)
        self.avg_corr_value = np.mean(self.corr_avg)
        #exit(1)

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
        self.bin_width=self.symbol_period/self.nbins
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
        if(self.t_offset > self.symbol_period/2):
            self.t_offset-=self.symbol_period

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
        #print(a2)
        #print(len(a2))
        asum = 0
        #print(start_index)
        #print(end_index)
        for i in range(start_index,end_index+1):
            #assumes that nonzero returns nonzero indicies in ascending order
            p = np.nonzero(a2[i][128:])
            n = np.nonzero(a2[i][:128])
            #print(i)
            #print(p)
            #print(n)
            #print(p[0][0]+128)
            #print(n[0][-1])
            #exit(1)
            asum += (p[0][0]+128-n[0][-1])
        #exit(1)

        return(asum)

    def plot_eye(self, filename=None, saturation_level=12, offset_time=None):
        if offset_time==None:
            offset_time = self.t_offset
        #print(self.imgfile)
        if filename==None:
            filename=self.imgfile
        else:
            self.imgfile = filename
        f, eye = pyplot.subplots(1,1, figsize=(10, 10))  # Create a figure and an axes.
        s = "Node %d - toffset %.2fns" % (self.number, offset_time*1e9)
        eye.set_title(s)
        eye.imshow(self.heatmap, cmap='hot', origin='lower', vmin=0, vmax=saturation_level, aspect='auto')
        pyplot.savefig(filename)
        pyplot.close(f)

    def plot_reflections(self, filename=None, saturation_level=12, index=0, eye_stats=None):
        if filename==None:
            filename=self.imgfile
        else:
            self.imgfile = filename

        position = float(eye_stats['positions'][index]) #plot the 2d histogram
        f, (network_plot, eye_opening_plot, jitter_plot, corr_plot, delay_plot, eye ) = pyplot.subplots(6,1, figsize=(15, 18), gridspec_kw={'height_ratios': [1, 1, 1, 1, 1, 3]})
        ####mixing segment line
        network_plot.plot([0,eye_stats['length']],[0,0], color="k")
        color_index = 0
        for node in eye_stats['attach_points']:
            network_plot.plot([node], np.zeros_like([node]), "-o", color=eye_stats['color_array'][color_index-1])
            color_index += 1
            network_plot.plot(eye_stats['attach_points'][eye_stats['tx_index']-1],
                    np.zeros_like(eye_stats['attach_points'][eye_stats['tx_index']-1]),
                "-*",
                color="k",
                markerfacecolor="k",
                markersize=12
                )

        network_plot.plot([position,position], [-0.01,0.01], color="k")
        #### end mixing segment line

        eye_opening_plot.plot(eye_stats['positions'], eye_stats['eye_area_1'], label="eye1")  
        eye_opening_plot.plot(eye_stats['positions'], eye_stats['eye_area_2'], label="eye2")  

        eye_opening_plot.set_xlabel("Cable Position (m)")
        eye_opening_plot.set_ylabel("Eye Area (V*ns)")
        eye_opening_plot.plot([position,position], [eye_stats['eye_area_1'][index],eye_stats['eye_area_2'][index]],
                "-o" ,
                "-*",
                color="k",
                markerfacecolor="k",
                markersize=16)

        jitter_plot.plot(eye_stats['positions'], eye_stats['crossing_width_1'], label="jitter1")
        jitter_plot.plot(eye_stats['positions'], eye_stats['crossing_width_2'], label="jitter2")
        jitter_plot.set_xlabel("Cable Position (m)")
        jitter_plot.set_ylabel("Jitter (ns)")
        jitter_plot.plot([position,position], [eye_stats['crossing_width_1'][index],eye_stats['crossing_width_2'][index]],
                "-o" ,
                "-*",
                color="k",
                markerfacecolor="k",
                markersize=16)

        corr_plot.plot(eye_stats['positions'],eye_stats['corr_avg'], label="corr_avg")  
        corr_plot.plot(eye_stats['positions'],eye_stats['corr_min'], label="corr_min")  
        corr_plot.plot([eye_stats['positions'][0],eye_stats['positions'][-1]],[0.65,0.65], label="corr_limit")  
        corr_plot.set_xlabel("Cable Position (m)")
        corr_plot.set_ylabel("Correlation Factor")
        corr_plot.plot([position,position], [eye_stats['corr_avg'][index],eye_stats['corr_min'][index]],
                "-o" ,
                "-*",
                color="k",
                markerfacecolor="k",
                markersize=16)

        delay_plot.plot(eye_stats['positions'],eye_stats['pattern_delay'], label="pattern_delay")  
        delay_plot.set_xlabel("Cable Position (m)")
        delay_plot.set_ylabel("Pattern Delay")
        delay_plot.set_ylim([0,400])
        #print(pyplot.yticks())
        print(eye_stats['pattern_delay'][index])
        pyplot.yticks(ticks=range(0,400,80))
        delay_plot.plot([position,position], [eye_stats['pattern_delay'][index],eye_stats['pattern_delay'][index]],
                "-o" ,
                "-*",
                color="k",
                markerfacecolor="k",
                markersize=16)

        s = "%4d - %6.2fm - toffset %.2fns" % (self.number, self.number*0.05, eye_stats['pattern_delay'][index])
        eye.set_title(s)
        eye.imshow(self.heatmap, cmap='hot', origin='lower', vmin=0, vmax=saturation_level, aspect='auto')

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
        #print("Generating 2d Histogram")
        self._make_histogram_2d()
    
        vmax=0.75
        vmin=-0.75
        #print("Generating Heat Map")
        for i in range(0,len(self.bins)):
            index = (i+self.min_bin) % len(self.bins)
            for s in self.bins[index]:
                bin_y = self._digitize(vmax, vmin, self.nbits, s[1])
                self.heatmap[bin_y][i] += 1

        #determines 4 indicies indicating where the eyes open and close
        #print("Measure zero crossings")
        self._measure_zero_crossing()
        #print("Measure eye opening")
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
