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

class Transmitter(object):
    """Object representing a transmitter connected to a mixing segment

    name            name of the cable segment.  This will be the name of the instance and the subcircuit
    port            the name of the port connection, for example "t1"
                    the connections at the port of this cable will then be called t1p and t1n
    """

    def __init__(self, port="t0"):
        self.name = "iac"
        self.port = port

    def subcircuit(self):
        """Generate the subcircuit definition for this cable segment"""
        netlist = [self.__str__()]
        return "\n".join(netlist)

    def __str__(self):
        s = [
             "**********************"
            ,"* name    %s" % self.name
            ,"* port    %s" % self.port
            ,"**********************"
            ]
        return "\n".join(s)

    def instance(self):
        """Generate the instance call for this cable segment"""
        return "%s %sp %sn 0 ac 1" % \
                (
                    self.name,
                    self.port, self.port,
                )

    def transmitter_current(self):
        return "i(%s)" % self.name

if __name__ == '__main__':
    t0 = Transmitter(port="t0")
    print(t0.subcircuit())
    print(t0.instance())
