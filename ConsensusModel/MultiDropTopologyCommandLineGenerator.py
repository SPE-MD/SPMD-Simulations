#! /usr/bin/env python3

#Copyright  2021 <Analog Devices>
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
import matplotlib.pyplot as plt
import datetime
import colorsys
#from multiprocessing import Process

sys.path.append(dirname(__file__)) #adds this file's director to the path
#import subprocess
import runspice
import mpUtil
from ltcsimraw import ltcsimraw as ltcsimraw
#from steptable import StepTable
from spifile import SpiFile as SpiFile
from micro_reflections import micro_reflections

from cable import Cable as Cable
from node import Node as Node
from termination import Termination as Termination
from transmitter import Transmitter as Transmitter
from trunk import Trunk as Trunk

from MultiDropTopologySpreadsheetImport import MultidropSimulationNetwork
from MultiDropTopologySpreadsheetImport import CableSegmentModelConfig
from MultiDropTopologySpreadsheetImport import MultiDropSimulationNodeConfig

from ConsensusModelSimulator import ConsensusModelSimulator
from ConsensusModelPlotter import ConsensusModelPlotter

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='802.3da network model generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

    parser.add_argument('--nodes', type=int, \
            help='Set the number of nodes in the simulation', \
            default=16
            )

    parser.add_argument('--random_attach',
            action='store_true',
            help='When set, nodes will attached at random locations on the mixing segment\
            after nodes specified by --start_attach and --end_attach flags have been added\
            to the mixing segment (if any).  Node placements should be reproducible by reusing\
            the seed value from another sim (see the --seed flag)\
            Otherwise, nodes will be evenly distributed across the mixing segment between nodes\
            specified by --start_attach and --end_attach flags',
            )

    parser.add_argument('--start_attach', type=int, \
            help='Specify an number of nodes to be placed at the start of the mixing\
            segment with \'separation_min\' spacing',
            default=0
            )

    parser.add_argument('--start_pad', type=float, \
            help='Specify the distance between start of cable and the 1st node',
            default=0
            )

    parser.add_argument('--end_pad', type=float, \
            help='Specify the distance between end of cable and the last node',
            default=0
            )

    parser.add_argument('--end_attach', type=int, \
            help='Specify an number of nodes to be placed at the end of the mixing\
            segment with \'separation_min\' spacing',
            default=0
            )

    parser.add_argument('--length', type=float, \
            help='Mixing segment length in meters, will be rounded to an integer\
            number of segments per meter',\
            default=50
            )

    parser.add_argument('--segments_per_meter', type=int, \
            help='Size of finite element cable model segments.  Be sure this\
            lines up with lump models',\
            default=20
            )

    parser.add_argument('--drop_max', type=float, \
            help='Drop length between mixing segment and PD attachment in\
            meters.  This number will be rounded to an interger number of\
            segments per meter',
            default=0.5
            )

    parser.add_argument('--random_drop',
            action='store_true',\
            help='When set, node drop length will be chosen at random between\
            zero and drop_max. Drop lengths should be reproducible by reusing\
            the seed value from another sim (see the --seed flag) Otherwise,\
            drop lengths will be evenly distributed across the mixing segment',
            )

    parser.add_argument('--separation_min', type=float, \
            help='Minimum separation between nodes in meters.  This number will\
            be rounded to an integer number of segments per meter',\
            default=1.0\
            )

    parser.add_argument('--cnode', type=float, \
            help='Node capacitance in Farads.  All nodes will be assigned this MDI interface capacitance',\
            default=15e-12\
            )

    parser.add_argument('--lpodl', type=float, \
            help='Node inducatnce in Henrys.  All nodes will be assigned this MDI interface inductance',\
            default=80e-6\
            )

    parser.add_argument('--rnode', type=float, \
            help='Node resistance in Ohms.  All nodes will be assigned this MDI interface resitance',\
            default=10000\
            )

    parser.add_argument('--seed', type=int, \
            help='Seed value for random number generator',\
            default=-1
            )

    parser.add_argument('--tx_node', type=int, \
            help='Set the transmitter node.',\
            default=1
            )

    parser.add_argument('--rx_node', type=int, \
            help='Not currently implemented because all non tx nodes are rx nodes',\
            default=0
            )

    parser.add_argument('--noplot', action='store_true', help='set this flag to\
            prevent plotting')
    
    parser.add_argument('--plot_png_filename', type=str, \
            help='Filename for plot image output as a .png file. Default is zcable.png',\
            default='zcable.png'
            )

    parser.add_argument('--noautoscale', action='store_true',\
            help='set this flag to lock the y-axis on IL/RL plots to -80dB/-70dB\
            respectively.  The xaxis on the network model will be locked at -1m to 101m'
            )

    parser.add_argument('--attach_error', type=float, \
            help='add gaussian error to attachment points.  Pass the the sigma value of the attachment\
            error or 0 for no error.  Ignored for randomly placed nodes.  If'\
            'attach_error is set to a large value, can separation_min be violated?'\
            'I don\'t know',\
            default=0
            )

    args = parser.parse_args()

    ###
    #Setup random seed in case this run has random parameters
    ###
    seed = args.seed
    if seed == -1:
        tim = datetime.datetime.now()
        seed = tim.hour*10000+tim.minute*100+tim.second
        random.seed(seed)
    else:
        random.seed(seed)
    print("#Random Seed = %s" % seed)

    #tpd=3.335e-9      #speed of light on this cable
    #z0 = 100          #cable impedance
    #l_m = tpd * z0    #inductance per meter
    #c_m = tpd / z0    #capacitance per meter
    #r_m = 0.188       #dc resistance per meter
    #r_m = 0.001       #dc resistance per meter

    #18 awg l and c data for a 5cm segment
    #l1 a t2p {1*20.6435n}
    #c1 t2p x {1*2.25026p}
    #l_m = 20.6435e-09 / 0.05
    #c_m = 2.25026e-12 / 0.05

    #llump = l_m / args.segments_per_meter
    #clump = c_m / args.segments_per_meter
    #rlump = r_m / args.segments_per_meter 

    ################################################################################
    #Make trunk segments that will connect the nodes
    ################################################################################
    t=Trunk( length=args.length
            , nodes=args.nodes
            , start_pad=args.start_pad
            , end_pad=args.end_pad
            , separation_min=args.separation_min
            , start_attach=args.start_attach
            , end_attach=args.start_attach
            , random_attach=args.random_attach
            , attach_error=args.attach_error
            )
    trunk_segments = t.get_cable_segments()
    for x in trunk_segments:
        print(x)
    
    ################################################################################
    #Connect termination Resistors (actually termination R/C) to then ends of
    #the trun
    ################################################################################
    term_start = Termination(name="start_term", port=trunk_segments[0].port1, stim_port="start")
    term_end   = Termination(name="end_term"  , port=trunk_segments[-1].port2, stim_port="end")

    ################################################################################
    #Attach nodes to the trunk
    ################################################################################
    nodes = []
    for n in range(1,args.nodes+1):
        port="t%d" % (n)
        node = Node(number=n,port=port, drop_length=args.drop_max, random_drop=args.random_drop,
                cnode=args.cnode, lpodl=args.lpodl, rnode=args.rnode)
        nodes.append(node)

    ################################################################################
    #Determine which node will be the transmitter for the simulation
    ################################################################################
    #boundary check the transmit node index
    tx_node = args.tx_node
    if tx_node<1: #choose a random transmit node
        tx_node = random.randint(1,args.nodes)
        print("Randomly Chose Node %d as the transmitter" % tx_node)
    tx_index=min(tx_node, args.nodes)
    tx_index=max(tx_index, 1)
    tx_node = nodes[tx_index-1]
    transmitter = Transmitter(port=tx_node.phy_port)
        
    ################################################################################
    #Write a spice file with the system setup
    ################################################################################
    with open("cable.p", 'w') as cable:
        cable.write("*lumped transmission line model with %d segments per meter at %d meters\n"\
        % (args.segments_per_meter, args.length))
        cable.write("*and a %f meter long cable\n" % args.length)
        cable.write(".include tlump2.p\n")
        cable.write(".include node.p\n")

        for s in trunk_segments:
            cable.write(s.subcircuit()+"\n")
        for n in nodes:
            cable.write(n.subcircuit()+"\n")

        cable.write(term_start.subcircuit()+"\n")
        cable.write(term_end.subcircuit()+"\n")
        cable.write("** MAIN NETWORK DESCRIPTION **\n")
        for s in trunk_segments:
            cable.write(s.instance()+"\n")
        for n in nodes:
            cable.write(n.instance()+"\n")
        cable.write(term_start.instance()+"\n")
        cable.write(term_end.instance()+"\n")

    sim = ConsensusModelSimulator()

    sim.transmitter = transmitter
    sim.nodes = nodes
    
    print ("Running Sim")
    sim.run()
    print ("Done Running Sim")

    print ("Fetching results...")
    simulationResult = sim.getResults()

    print ("Plotting results...")
    plotter = ConsensusModelPlotter()

    plotter.results = simulationResult
    plotter.nodes = nodes
    plotter.tx_node = tx_node
    plotter.transmitter = transmitter
    plotter.tx_index = tx_index
    plotter.trunk = t


    plotter.noautoscale = args.noautoscale
    plotter.noautoscale = args.noautoscale
    plotter.length = args.length
    plotter.plot_png_filename = args.plot_png_filename
    plotter.noplot = args.noplot

    print ("Plotting Plots")
    plotter.generatePlots()