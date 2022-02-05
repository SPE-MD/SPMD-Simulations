#! /usr/bin/env python3

#Copyright  2021 <Michael Paul>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re
import sys
from os import listdir
from os.path import dirname
import os.path 
import shutil
import argparse
import time
import random
import numpy as np
import math

class CableModel(object):
    #"name"       : "panduit_18g",
    #"comment"    : "#18 gauge cable. Original data was for a 5cm segment.  Divide by ref_length to get 1m referenced values.", 
    #"gauge"      : 18,
    #"ref_length" : 0.05,
    #"rskin"     : 1.134268e-5,
    #"l"          : 20.6435e-9 ,
    #"c"          : 2.25026e-12,
    #"rdc"        : 0.0094
    def __init__(self, name="default", gauge=18, Zo=None, rdc=0.0094, l=20.6435e-9, c=2.25026e-12, rskin=1.134268e-5, ref_length=0.05):
        self.name = name
        self.gauge = gauge
        self.ref_length = ref_length
        self.rskin = rskin / ref_length
        self.l_m   = l / ref_length
        self.c_m   = c / ref_length
        self.rdc   = rdc / ref_length
        self.Zo = math.sqrt(self.l_m / self.c_m)

    #returns a string of params suitable for appending to a spice subcircuit call
    #must pass the reference length for the cable segment
    #if Zo!= None, the L and C parameters will be pulled to change the characteristic impedance to the specified Zo
    def getParams(self,length=0.05,Zo=None):
        err=0
        if(Zo):
            A = (Zo**2)*self.c_m / self.l_m
            err=(A-1)/(A+1)

        l_m    = self.l_m * (1+err)
        c_m    = self.c_m * (1-err)

        params = "params: lseg={%g} rskin={%g} cseg={%g} rser={%g}" % (
                l_m        * length,
                self.rskin * length,
                c_m        * length,
                self.rdc   * length
                )
        return params

    def getZo(self):
        return math.sqrt(self.l_m / self.c_m)



class Cable(object):
    """Object representing a section of cable

    name            name of the cable segment.  This will be the name of the instance and the subcircuit
    length          length of the cable segment
    gauge            cable gauge, does nothing right now
    max_seg_length  max length for a finite element segment, 0.05m is a good choice here
    port1           the name of the 2nd port, for example "t1"
                    the connections at port2 of this cable will then be called t1p and t1n
    port2           the name of the 2nd port, for example "t2"
                    the connections at port2 of this cable will then be called t2p and t2n
    Zo              desired segment impedance.  l_m and c_m data will be skewed so the impedance is Zo
                    if Zo is not passed or is None, then the cable impedance is defiend by sqrt(l_m/cm)
                    there is no boundary cheking here, so keep it reasonable or the program will crash
    spice_model     specify the spice subcircuit model.  Including the correct model file is not handled by this function
    """

    def __init__(self, cableModel=None, name="trunk" ,length=10, gauge=18 ,max_seg_length=0.05, port1="t0", port2="t1", spice_model='tlump', Zo=None):
        self.name = name
        self.length = length
        self.gauge = gauge
        self.max_seg_length = max_seg_length
        self.nsegs = self.length / self.max_seg_length
        self.whole = int(self.nsegs)
        self.part  = self.nsegs - self.whole
        self.total_segs = self.whole
        self.port1 = port1
        self.port2 = port2
        self.spice_model = spice_model
        if(cableModel == None):
            cableModel = CableModel() #load a default cable model
        self.cableModel = cableModel

        if(Zo == None):
            Zo = self.cableModel.getZo()
        self.Zo = Zo

        #floating point errors can cause some silly small segments
        #limit minimum segment size to 100um
        if(self.part >= 0.0001):
            self.total_segs += 1
        else:
            self.part = 0

    #handle the generation of netlist text for the segment lumps
    def __make_segment__(self, seg_num, segment_length):
        return "xseg%04d %04dp %04dn %04dp %04dn rtn %s %s"\
                % (seg_num, seg_num, seg_num, seg_num+1, seg_num+1,
                        self.spice_model,
                        self.cableModel.getParams(segment_length, self.Zo)
                    )

    def subcircuit(self):
        """Generate the subcircuit definition for this cable segment"""
        netlist = [self.__str__()]

        netlist.append(".subckt %s %04dp %04dn endp endn rtn" % 
                    (self.name, 0, 0))

        netlist.append("rendp endp %04dp 1u" % self.total_segs)
        netlist.append("rendn %04dn endn 1u" % self.total_segs)

        #generate the body of the cable
        for i in range(0,self.whole):
            netlist.append(self.__make_segment__(i, self.max_seg_length))

        #handle fractional segments
        if(self.part > 0):
            netlist.append(self.__make_segment__(self.whole, self.part*self.max_seg_length))


        netlist.append(".ends %s" % self.name)
        return "\n".join(netlist)

    def __str__(self):
        s = [
             "**********************"
            ,"* name    %s" % self.name
            ,"* Zo      %s" % self.Zo
            ,"* length  %s" % self.length
            ,"* gauge    %s" % self.gauge
            ,"* seg_max %s" % self.max_seg_length
            ,"* nsegs   %f" % self.nsegs
            ,"* whole   %f" % self.whole
            ,"* part    %f" % self.part
            ,"* port1   %s" % self.port1
            ,"* port2   %s" % self.port2
            ,"**********************"
            ]
        return "\n".join(s)

    def instance(self):
        """Generate the instance call for this cable segment"""
        return "x%s %sp %sn %sp %sn rtn %s" % \
                (
                    self.name,
                    self.port1, self.port1,
                    self.port2, self.port2,
                    self.name
                )

    def port1_current(self):
        return "ix(%s:0000n)" % (self.name)

    def port2_current(self):
        return "ix(%s:endn)" % (self.name) 

    def port1_voltage(self):
        return [
                "v(%sp)" % (self.port1),
                "v(%sn)" % (self.port1)
                ]

    def port2_voltage(self):
        return [
                "v(%sp)" % (self.port2),
                "v(%sn)" % (self.port2)
                ]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='802.3da network model generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

    parser.add_argument('--nosim', \
            action='store_true',
            help='Don\'t run a sim, rely on data from previous sim'
            )

    args = parser.parse_args()

    from termination import Termination as Termination
    term0 = Termination(name="start_term", port="t0", stim_port="start", rterm=100)
    c0 = Cable(name="trunk0",length=2 ,gauge=18,max_seg_length=0.01,port1="t0",port2="t1",Zo=100)
    c1 = Cable(name="trunk1",length=40,gauge=18,max_seg_length=0.01,port1="t1",port2="t2",Zo=100)
    c2 = Cable(name="trunk2",length=8 ,gauge=18,max_seg_length=0.01,port1="t2",port2="t3",Zo=100)
    term1 = Termination(name="end_term", port="t3", stim_port="end", rterm=100)

    #term0 = Termination(name="start_term", port="t0", stim_port="start", rterm=100)
    #c0 = Cable(name="trunk0",length=2 ,gauge=18,max_seg_length=0.01,port1="t0",port2="t1",Zo=100)
    #c1 = Cable(name="trunk1",length=40,gauge=18,max_seg_length=0.01,port1="t1",port2="t2",Zo=96)
    #c2 = Cable(name="trunk2",length=9 ,gauge=18,max_seg_length=0.01,port1="t2",port2="t3",Zo=111)
    #term1 = Termination(name="end_term", port="t3", stim_port="end", rterm=100)

    spi = os.path.join("cable","junk.spi")
    raw = os.path.join("cable","junk.raw")
    with open(spi, 'w') as spifile:
        spifile.write("*cable model simulation"+"\n")
        spifile.write(".include ../tlump2.p"+"\n")
        spifile.write(c0.subcircuit()+"\n")
        spifile.write(c1.subcircuit()+"\n")
        spifile.write(c2.subcircuit()+"\n")
        spifile.write(term0.subcircuit()+"\n")
        spifile.write(term1.subcircuit()+"\n")
        spifile.write(c0.instance()+"\n")
        spifile.write(c1.instance()+"\n")
        spifile.write(c2.instance()+"\n")
        spifile.write(term0.instance()+"\n")
        spifile.write(term1.instance()+"\n")

        spifile.write("iac  acp acn 0 ac 1"+"\n")
        spifile.write("rracp t0p acp 220n"+"\n")
        spifile.write("rracn acn t0n 220n"+"\n")
        spifile.write("racp acp rtn 50k"+"\n")
        spifile.write("racn rtn acn 50k"+"\n")

        #spifile.write("cx t2p t2n 30p"+"\n")
        spifile.write(".save v(*) i(*)"+"\n")
        spifile.write("vrtn rtn 0 0"+"\n")
        spifile.write(".ac lin 4096 10k 40.96meg\n")

    if(args.nosim == False):
        import runspice
        runspice.runspice(spi)

    from ltcsimraw import ltcsimraw as ltcsimraw
    rf=ltcsimraw(raw)
    #sparams = rf.scattering_parameters(c1.port1_voltage()[0], c1.port1_voltage()[1], c1.port1_current(),
    #sparams = rf.scattering_parameters(c1.port1_voltage()[0], c1.port1_voltage()[1], "i(iac)",
    #sparams = rf.scattering_parameters(["v(acp)", "v(acn)"], c1.port1_current(),
    #   [c2.port2_voltage()[0], c2.port2_voltage()[1]], c2.port2_current(), rin=100, rout=100)

    sparams = rf.scattering_parameters(["v(acp)", "v(acn)"], "i(iac)",
       [c2.port2_voltage()[0], c2.port2_voltage()[1]], c2.port2_current(), rin=100, rout=100)

    import matplotlib.pyplot as plt
    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5,1, figsize=(9, 12))  # Create a figure and an axes.
    ax1.plot(sparams['frequency'], sparams['s11'] , label="test")  # Plot more data on the axes...
    ax1.set_ylabel('RL')
    ax2.plot(sparams['frequency'], sparams['gain'], label="test")  # Plot more data on the axes...
    ax2.set_ylabel('IL')
    ax3.plot(sparams['frequency'], sparams['phase'], label="test")  # Plot more data on the axes...
    ax3.set_ylabel('Phase')
    ax4.plot(sparams['frequency'], sparams['zin_mag'] , label="test")  # Plot more data on the axes...
    ax4.set_ylabel('Zcable')

    try :
        from dme import pulse_wave as pulse_wave
        #generate a coherantly sampled test pulse
        duty_cycle = 0.001
        pulse = pulse_wave(prime=83, duty_cycle=duty_cycle)

        #generate graph for pulse response
        fft_out = rf.fft_zin(
                pulse.fft_value,
                ["v(acp)","v(acn)"],
                "i(iac)"
                )

        signal = np.fft.irfft(fft_out)
        t=0 #used to adjust the eye placement
        lap=pulse.tper

        xt = []
        yt = []
        zt = []
        wt = []
        mean = np.mean(signal)
        print(mean)
        o = np.array(signal,dtype=float) +50*np.array(pulse.sampled_values,dtype=float)
        offset = np.mean(o)
        print(offset)
        for i in range(0,len(signal)):
            tn = i/81.92e6
            if (tn - t) > lap:
               t+=lap
               #add a NaN to the data to prevent lines being drawn from end to beginning time on the eye
               xt.append(float('NaN'))
               yt.append(float('NaN'))
               zt.append(float('NaN'))
               wt.append(float('NaN'))
               #print("")
            #print("%.12f %.12f" % (tn-t, signal[i]))
            rho = signal[i] - offset
            wt.append(-50 * (rho - 1)/(1 + rho))
            yt.append(signal[i])
            xt.append(tn-t)
            zt.append(pulse.sampled_values[i]*-50)
            #wt.append(rho)
            #print(pulse.sampled_values[i]*50)
        ax5.set_xlim([-20e-9,(pulse.tper)])
        ax5.set_ylim([0,150])
        ax5.grid(b=True)
        #ax5.scatter(xt, yt, s=1)  # Plot more data on the axes...
        #ax5.scatter(xt, zt, s=1)  # Plot more data on the axes...
        ax5.scatter(xt, wt, s=1)  # Plot more data on the axes...


    except Exception as e:
        print(e)
        print("issues generating pulse response")


    plt.show()
