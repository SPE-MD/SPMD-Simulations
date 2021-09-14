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
    rconn
    """

    def __init__(self, number=1, port1="t1b", port2="t2a", node_port='y1', subcircuit=None, rconn=0.010):
        self.number = number
        self.name = "tee%d" % number
        self.port1 = port1
        self.port2 = port2
        self.node_port = node_port
        self.rconn=rconn

    def subcircuit(self):
        """Generate the subcircuit definition for this cable segment"""
        netlist = [self.__str__()]

        netlist.append(".subckt %s ip in op on np nn rtn params: rconn=0.01" % (self.name))

        #generate the body of the cable
        netlist.append("r1p ip p {rconn}")
        netlist.append("r1n in n {rconn}")
        netlist.append("r2p p op {rconn}")
        netlist.append("r2n n on {rconn}")

        netlist.append("r3p p np {rconn}")
        netlist.append("r3n n nn {rconn}")

        netlist.append(".ends %s" % self.name)
        return "\n".join(netlist)

    def __str__(self):
        s = [
             "**********************"
            ,"* name        %s" % self.name
            ,"* port1       %s" % self.port1
            ,"* port2       %s" % self.port2
            ,"* node_port   %s" % self.node_port
            ,"**********************"
            ]
        return "\n".join(s)

    def instance(self):
        """Generate the instance call for this cable segment"""
        return "x%s %sp %sn %sp %sn %sp %sn rtn %s params: rconn=%g" % \
                (
                    self.name,
                    self.port1, self.port1,
                    self.port2, self.port2,
                    self.node_port, self.node_port,
                    self.name,
                    self.rconn
                )

if __name__ == '__main__':
    t0 = Termination(name="t0",port="t0", stim_port="ts")
    print(t0.subcircuit())
    print(t0.instance())
    print(t0.termination_resistor_current())#! /usr/bin/env python3
