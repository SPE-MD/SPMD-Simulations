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

class Cable(object):
    """Object representing a section of cable

    name            name of the cable segment.  This will be the name of the instance and the subcircuit
    length          length of the cable segment
    gage            cable gage, does nothing right now
    max_seg_length  max length for a finite element segment, 0.05m is a good choice here
    port1           the name of the 2nd port, for example "t1"
                    the connections at port2 of this cable will then be called t1p and t1n
    port2           the name of the 2nd port, for example "t2"
                    the connections at port2 of this cable will then be called t2p and t2n
    """

    def __init__(self, name="trunk" ,length=10, gage=18 ,max_seg_length=0.05, port1="t0", port2="t1"):
        self.name = name
        self.length = length
        self.gage = gage
        self.max_seg_length = max_seg_length
        self.nsegs = self.length / self.max_seg_length
        self.whole = int(self.nsegs)
        self.part  = self.nsegs - self.whole
        self.total_segs = self.whole
        self.port1 = port1
        self.port2 = port2

        #floating point errors can cause some silly small segments
        #limit minimum segment size to 100um
        if(self.part >= 0.0001):
            self.total_segs += 1
        else:
            self.part = 0

        #18 gage cable
        self.r_skin = 1.134268e-5 / 0.05
        self.l_m    = 20.6435e-9  / 0.05
        self.c_m    = 2.25026e-12 / 0.05
        self.rdc    = 0.188

    #handle the generation of netlist text for the segment lumps
    def __make_segment__(self, seg_num, segment_length):
        return "xseg%04d %04dp %04dn %04dp %04dn rtn tlump params: lseg={%g} rskin={%g} cseg={%g} rser={%g}"\
                % (seg_num, seg_num, seg_num, seg_num+1, seg_num+1
                    , self.l_m * segment_length
                    , self.r_skin * segment_length
                    , self.c_m * segment_length
                    , self.rdc * segment_length
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
            ,"* length  %s" % self.length
            ,"* gage    %s" % self.gage
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
        return "ix(%s:%04dn)" % (self.name, self.total_segs)

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
    from termination import Termination as Termination
    term0 = Termination(name="start_term", port="t0", stim_port="start")
    c1 = Cable(name="trunk0",length=25.56,gage=18,max_seg_length=0.05,port1="t0",port2="t1")
    c2 = Cable(name="trunk1",length=25.55,gage=18,max_seg_length=0.05,port1="t1",port2="t2")
    term1 = Termination(name="end_term", port="t2", stim_port="end")

    spi = os.path.join("junk","junk.spi")
    raw = os.path.join("junk","junk.raw")
    with open(spi, 'w') as spifile:
        spifile.write("*cable model simulation"+"\n")
        spifile.write(".include ../tlump2.p"+"\n")
        spifile.write(c1.subcircuit()+"\n")
        spifile.write(c2.subcircuit()+"\n")
        spifile.write(term0.subcircuit()+"\n")
        spifile.write(term1.subcircuit()+"\n")
        spifile.write(c1.instance()+"\n")
        spifile.write(c2.instance()+"\n")
        spifile.write(term0.instance()+"\n")
        spifile.write(term1.instance()+"\n")

        spifile.write("iac  acp acn 0 ac 1"+"\n")
        spifile.write("cacp t0p acp 220n"+"\n")
        spifile.write("cacn acn t0n 220n"+"\n")
        spifile.write("racp acp rtn 5k"+"\n")
        spifile.write("racn rtn acn 5k"+"\n")

        spifile.write("cx t2p t2n 30p"+"\n")
        spifile.write(".save v(*) i(*)"+"\n")
        spifile.write("vrtn rtn 0 0"+"\n")
        spifile.write(".ac lin 200 300k 40Meg"+"\n")

    import runspice
    runspice.runspice(spi)

    from ltcsimraw import ltcsimraw as ltcsimraw
    rf=ltcsimraw(raw)
    #sparams = rf.scattering_parameters(c1.port1_voltage()[0], c1.port1_voltage()[1], c1.port1_current(),
    #sparams = rf.scattering_parameters(c1.port1_voltage()[0], c1.port1_voltage()[1], "i(iac)",
    sparams = rf.scattering_parameters("v(acp)", "v(acn)", "i(iac)",
            c2.port2_voltage()[0], c2.port2_voltage()[1], c2.port2_current(), rin=50, rout=50)

    import matplotlib.pyplot as plt
    fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize=(9, 9))  # Create a figure and an axes.
    ax1.plot(sparams['frequency'], sparams['s11'] , label="test")  # Plot more data on the axes...
    ax2.plot(sparams['frequency'], sparams['gain'], label="test")  # Plot more data on the axes...
    ax3.plot(sparams['frequency'], sparams['phase'], label="test")  # Plot more data on the axes...
    plt.show()
