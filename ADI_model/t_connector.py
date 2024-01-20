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

class T_connector(object):
    """Object representing a mixing segment trunk termination

    name            name of the cable segment.  This will be the name of the instance and the subcircuit
    port1           the name of the port connection, for example "t1" the connections at the port of this cable will then be called t1p and t1n
    port2           the name of the port connection, for example "t1" the connections at the port of this cable will then be called t1p and t1n
    node_port       the name of the port connection, for example "t1" the connections at the port of this cable will then be called t1p and t1n
    lcomp           compensation inductance value
    lcomp_match     copmensation inductance matching, 0 means perfectly matched, 1 means positive side lcomps are 1% high and neg side lcomps are 1% low
    """

    def __init__(self, number=1, port1="t1b", port2="t2a", node_port='y1', subcircuit=None ,lcomp=50e-9, lcomp_match=0):
        self.number = number
        self.name = "tee%d" % number
        self.port1 = port1
        self.port2 = port2
        self.node_port = node_port
        self.rconn=0.025
        self.lcomp_dcr=0.020 #42mOhm max
        self.lcomp=lcomp
        self.lcomp_match = lcomp_match
        self.lcomp_srf=1440e6

    def subcircuit(self):
        """Generate the subcircuit definition for this cable segment"""
        netlist = [self.__str__()]

        netlist.append(".subckt %s ip in op on np nn rtn" % (self.name))

        cpar = 1/ (self.lcomp * (self.lcomp_srf * 2 * math.pi)**2)
        #generate the body of the cable
        netlist.append("r1p ip iip %g" % (self.rconn))
        netlist.append("r1n in iin %g" % (self.rconn))
        #netlist.append("l1p iip p %g rser=%g cpar=%g" % (self.lcomp*(1+(self.lcomp_match/100.)), self.lcomp_dcr, cpar))
        #netlist.append("l1n iin n %g rser=%g cpar=%g" % (self.lcomp*(1-(self.lcomp_match/100.)), self.lcomp_dcr, cpar))
        #netlist.append("l2p p oop %g rser=%g cpar=%g" % (self.lcomp*(1+(self.lcomp_match/100.)), self.lcomp_dcr, cpar))
        #netlist.append("l2n n oon %g rser=%g cpar=%g" % (self.lcomp*(1-(self.lcomp_match/100.)), self.lcomp_dcr, cpar))
        if(self.lcomp <= 1e-9):
            netlist.append("rl1p iip p 68m")
            netlist.append("rl1n iin n 68m")
            netlist.append("rl2p p oop 68m")
            netlist.append("rl2n n oon 68m")
        else:

            netlist.append("xsegi  iip iin iiip iiin rtn tlump params: lseg=2.1533e-08 rskin=1.13427e-05 cseg=2.1533e-12 rser=100n")
            netlist.append("xl1p iiip iiiip coilcraft8085LS")
            netlist.append("xl1n iiin iiiin coilcraft8085LS")
            netlist.append("xsegii iiiip iiiin p n rtn tlump params: lseg=2.1533e-08 rskin=1.13427e-05 cseg=2.1533e-12 rser=100n")

            netlist.append("xsegoo p n oooop oooon rtn tlump params: lseg=2.1533e-08 rskin=1.13427e-05 cseg=2.1533e-12 rser=100n")
            netlist.append("xl2p oooop ooop coilcraft8085LS")
            netlist.append("xl2n oooon ooon coilcraft8085LS")
            netlist.append("xsego  ooop ooon oop oon rtn tlump params: lseg=2.1533e-08 rskin=1.13427e-05 cseg=2.1533e-12 rser=100n")

        netlist.append("r2p oop op %g" % (self.rconn))
        netlist.append("r2n oon on %g" % (self.rconn))
        
        netlist.append("r3p p np %g" % self.rconn)
        netlist.append("r3n n nn %g" % self.rconn)

        netlist.append(".ends %s" % self.name)
        return "\n".join(netlist)

    def __str__(self):
        s = [
             "**********************"
            ,"* name        %s" % self.name
            ,"* port1       %s" % self.port1
            ,"* port2       %s" % self.port2
            ,"* lcomp       %s" % self.lcomp
            ,"* lcomp_match %s" % self.lcomp_match
            ,"* node_port   %s" % self.node_port
            ,"**********************"
            ]
        return "\n".join(s)

    def instance(self):
        """Generate the instance call for this cable segment"""
        return "x%s %sp %sn %sp %sn %sp %sn rtn %s" % \
                (
                    self.name,
                    self.port1, self.port1,
                    self.port2, self.port2,
                    self.node_port, self.node_port,
                    self.name
                )

    def port1_current(self):
        return "ix(%s:ip)" % (self.name)

    def port2_current(self):
        return "ix(%s:op)" % (self.name) 

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
    t0 = T_connector(name="t0",port="t0", stim_port="ts")
    print(t0.subcircuit())
    print(t0.instance())
    print(t0.termination_resistor_current())#! /usr/bin/env python3
