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

class Termination(object):
    """Object representing a mixing segment trunk termination

    name            name of the cable segment.  This will be the name of the instance and the subcircuit
    port            the name of the port connection, for example "t1"
                    the connections at the port of this cable will then be called t1p and t1n
    stim_port       the name of the stimulus port connection, for example "ts"
                    the connections at the port of this cable will then be called t1p and t1n
                    this connects directly to a termination resistor.  This is
                    where a tx or rx would connect
    ccouple         value of dc-blocking capacitors
    cmatch          specify mismatch of dc-blocking caps in percent.  Positive cmatch makes the pos
    """

    def __init__(self, name="term0", port="t0", stim_port="ts", rterm=100, ccouple=220e-9, cmatch=0):
        self.name = name
        self.port = port
        self.port1 = port
        self.port2 = port
        self.stim_port = stim_port
        self.rterm = rterm
        self.ccouple = ccouple
        self.cmatch = cmatch
        self.ccp = self.ccouple * (1 + (self.cmatch/100.))
        self.ccn = self.ccouple * (1 - (self.cmatch/100.))

    def subcircuit(self):
        """Generate the subcircuit definition for this cable segment"""
        netlist = [self.__str__()]

        netlist.append(".subckt %s p n sp sn rtn" % (self.name))

        #generate the body of the cable
        netlist.append("ccp p sp %g" % self.ccp)
        netlist.append("ccn sn n %g" % self.ccn)
        netlist.append("rp sp rtn %g" % (self.rterm / 2.))
        netlist.append("rn rtn sn %g" % (self.rterm / 2.))

        netlist.append(".ends %s" % self.name)
        return "\n".join(netlist)

    def __str__(self):
        s = [
             "**********************"
            ,"* name    %s" % self.name
            ,"* rterm   %s" % self.rterm
            ,"* ccouple %s" % self.ccouple
            ,"* cmatch  %s" % self.cmatch
            ,"* ccp     %s" % self.ccp
            ,"* ccn     %s" % self.ccn
            ,"* port    %s" % self.port
            ,"**********************"
            ]
        return "\n".join(s)

    def instance(self):
        """Generate the instance call for this cable segment"""
        return "x%s %sp %sn %sp %sn rtn %s" % \
                (
                    self.name,
                    self.port, self.port,
                    self.stim_port, self.stim_port,
                    self.name
                )
    def termination_resistor(self):
        return "%s:rp" % self.name

    def termination_resistor_current(self):
        return "I(%s)" % self.termination_resistor()


if __name__ == '__main__':
    t0 = Termination(name="t0",port="t0", stim_port="ts")
    print(t0.subcircuit())
    print(t0.instance())
    print(t0.termination_resistor_current())
