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
        self.rconn=0.050
        self.lcomp=lcomp
        self.lcomp_match = lcomp_match

    def subcircuit(self):
        """Generate the subcircuit definition for this cable segment"""
        netlist = [self.__str__()]

        netlist.append(".subckt %s ip in op on np nn rtn" % (self.name))

        #generate the body of the cable
        netlist.append("l1p ip p %g rser=%g" % (self.lcomp*(1+(self.lcomp_match/100.)), self.rconn))
        netlist.append("l1n in n %g rser=%g" % (self.lcomp*(1-(self.lcomp_match/100.)), self.rconn))
        netlist.append("l2p p op %g rser=%g" % (self.lcomp*(1+(self.lcomp_match/100.)), self.rconn))
        netlist.append("l2n n on %g rser=%g" % (self.lcomp*(1-(self.lcomp_match/100.)), self.rconn))

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

if __name__ == '__main__':
    t0 = Termination(name="t0",port="t0", stim_port="ts")
    print(t0.subcircuit())
    print(t0.instance())
    print(t0.termination_resistor_current())#! /usr/bin/env python3
