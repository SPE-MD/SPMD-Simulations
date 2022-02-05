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

from cable import Cable as Cable

class Node(object):
    """Object representing a node connected to a mixing segment

    number          node number.  The name of the instance and the subcircuit will be "node<number"
    port            the name of the port connection, for example "t1"
                    the connections at the port of this cable will then be called t1p and t1n
    drop_length     length of cable connecting the node to the mixing segment
    drop_gauge       cable gauge connecting node to the mixing segment
    spice_model     name of the spice subcircuit to envoke when creating the model
    """

    def __init__(self, number=0, port="t0", drop_length=0.0, drop_gauge=18,
            spice_model="node", random_drop=False,
            cnode=30e-12, lpodl=80e-6, rnode=10000):
        self.name = "node%d" % number
        self.number = number
        self.port = port
        self.phy_port = "phy_%d_" % number
        self.drop_name = "drop%d" % self.number
        self.drop_length = drop_length
        self.random_drop = random_drop
        if(random_drop):
            self.drop_length = random.uniform(0,drop_length)
        self.drop_gauge = drop_gauge
        self.spice_model = spice_model
        self.cnode = cnode
        self.lpodl = lpodl
        self.rnode = rnode

    def subcircuit(self):
        """Generate the subcircuit definition for this node segment"""
        netlist = [self.__str__()]
        drop = Cable(name=self.drop_name,length=self.drop_length,gauge=18,max_seg_length=0.05,port1="t0",port2="t1")
        netlist.append(drop.subcircuit())
        return "\n".join(netlist)

    def __str__(self):
        s = [
             "********* NODE *********"
            ,"* number      %s" % self.number
            ,"* name        %s" % self.name
            ,"* port        %s" % self.port
            ,"* drop_name   %s" % self.drop_name
            ,"* drop_length %f" % self.drop_length
            ,"* random_drop %s" % self.random_drop
            ,"* drop_gauge  %d" % self.drop_gauge
            ,"* spice_model %s" % self.spice_model
            ,"* cnode       %s" % self.cnode
            ,"* lpodl       %s" % self.lpodl
            ,"* rnode       %s" % self.rnode
            ,"************************"
            ]
        return "\n".join(s)

    def instance(self):
        """Generate the instance call for this node and drop segment"""
        instance = []
        instance.append("x%s %sp %sn node_%d_mdi_p node_%d_mdi_n rtn %s" % \
                (
                    self.drop_name,
                    self.port, self.port,
                    self.number, self.number,
                    self.drop_name
                )
                )
        instance.append("x%s node_%d_mdi_p node_%d_mdi_n %sp %sn rtn %s params: cnode=%g lpodl=%g rnode=%g" % \
                (
                    self.name,
                    self.number, self.number,
                    self.phy_port, self.phy_port,
                    self.spice_model,
                    self.cnode,
                    self.lpodl,
                    self.rnode
                )
                )
        return "\n".join(instance)

    def phy_port_voltage(self):
        return [
                "v(%sp)" % self.phy_port,
                "v(%sn)" % self.phy_port,
                ]

    def termination_current(self):
        return ("i(%s:rnodep)" % self.name)

if __name__ == '__main__':
    from termination import Termination as Termination
    n0 = Node(number=0,port="t0", drop_length=0.5)
    t0 = Termination(name="t0",port="t0", phy_port="ts")

    
    spi = os.path.join("junk","junk.spi")
    raw = os.path.join("junk","junk.raw")
    with open(spi, 'w') as spifile:
        spifile.write("*cable model simulation"+"\n")
        spifile.write(".include ../tlump2.p"+"\n")
        spifile.write(".include ../node.p"+"\n")
        spifile.write(n0.subcircuit()+"\n")
        spifile.write(t0.subcircuit()+"\n")
        spifile.write(n0.instance()+"\n")
        #spifile.write(t0.instance()+"\n")

        spifile.write("iac t0p t0n 0 ac 1"+"\n")
        #spifile.write("r0p phy_0_p 0 50"+"\n")
        #spifile.write("r0n 0 phy_0_n 50"+"\n")

        spifile.write(".save v(*) i(*)"+"\n")
        spifile.write("vrtn rtn 0 0"+"\n")
        spifile.write(".ac lin 2000 30k 40Meg"+"\n")

    import runspice
    runspice.runspice(spi)

    from ltcsimraw import ltcsimraw as ltcsimraw
    rf=ltcsimraw(raw)
    sparams = rf.scattering_parameters("v(t0p)", "v(t0n)", "i(iac)",
            "v(phy_0_p)", "v(phy_0_n)", "ix(node0:phyp)", rin=10000, rout=10000)

    import matplotlib.pyplot as plt
    fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize=(9, 9))  # Create a figure and an axes.
    ax1.plot(sparams['frequency'], sparams['s11'] , label="test")  # Plot more data on the axes...
    ax2.plot(sparams['frequency'], sparams['s11_phase'], label="test")  # Plot more data on the axes...
    ax3.plot(sparams['frequency'], sparams['zin_mag'], label="test")  # Plot more data on the axes...
    plt.show()
    plt.show()
