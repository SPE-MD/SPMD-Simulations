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
import adisimlib.runspice as runspice
import adisimlib.mpUtil as mpUtil
from adisimlib.ltcsimraw import ltcsimraw as ltcsimraw
#from steptable import StepTable
from adisimlib.spifile import SpiFile as SpiFile
from micro_reflections import micro_reflections

from adisimlib.cable import Cable as Cable
from adisimlib.node import Node as Node
from adisimlib.termination import Termination as Termination
from adisimlib.transmitter import Transmitter as Transmitter
from adisimlib.trunk import Trunk as Trunk

class MultidropSimulationNetwork(object):
    """Contains a single node from a multidrop network"""
    def __init__(self):
        self.trunk = None
        self.term_start = None
        self.term_end = None
        self.nodes = None
        self.tx_node = None
        self.tx_index = None
        self.transmitter = None

    def __str__(self):
        returnString =  "\nNodeConfig\n"
        returnString += "trunk:       %d\n" % self.trunk
        returnString += "term_start:  %s\n" % self.term_start
        returnString += "term_end:    %s\n" % self.term_end
        returnString += "nodes:       %s\n" % self.nodes
        returnString += "tx_node:     %f\n" % self.tx_node
        returnString += "tx_index:    %s\n" % self.tx_index
        returnString += "transmitter: %f\n" % self.transmitter
        return returnString

class MultiDropSimulationNodeConfig(object):
    """Contains a single node from a multidrop network"""
    def __init__(self, nodeConfig):
        self.NodeIndex      = nodeConfig["NodeIndex"]
        self.NodeModel      = nodeConfig["NodeModel"]
        self.TeeModel       = nodeConfig["TeeModel"]
        self.StubCableModel = nodeConfig["StubCableModel"]
        self.StubLength     = nodeConfig["StubLength"]
        self.LineCableModel = nodeConfig["LineCableModel"]
        self.LineLength     = nodeConfig["LineLength"]

    def __str__(self):
        returnString =  "\nNodeConfig\n"
        returnString += "NodeIndex:       %d\n" % self.NodeIndex 
        returnString += "NodeModel:       %s\n" % self.NodeModel 
        returnString += "TeeModel:        %s\n" % self.TeeModel 
        returnString += "StubCableModel:  %s\n" % self.StubCableModel 
        returnString += "StubLength:      %f\n" % self.StubLength 
        returnString += "LineCableModel:  %s\n" % self.LineCableModel 
        returnString += "LineLength:      %f\n" % self.LineLength 
        return returnString



class CableSegmentModelConfig(object):
    """Contains a single cable model parameter set for a given base model"""
    def __init__(self, cableSegConfig):
        self.CableBaseModel = cableSegConfig["CableBaseModel"]
        self.CableModelKey  = cableSegConfig["CableModelKey"]
        self.Vendor         = cableSegConfig["Vendor"]
        self.Model          = cableSegConfig["Model"]
        self.Gauge          = cableSegConfig["Gauge"]
        self.SegmentSize    = cableSegConfig["SegmentSize"]
        self.Rcable         = cableSegConfig["Rcable"]
        self.Lcable         = cableSegConfig["Lcable"]
        self.Ccable         = cableSegConfig["Ccable"]
        self.TransferFunc   = cableSegConfig["TransferFunc"]
    
    def __str__(self):
        returnString =  "\nCableModel\n"
        returnString += "CableBaseModel: %s\n" % self.CableBaseModel
        returnString += "CableModelKey:  %s\n" % self.CableModelKey
        returnString += "Vendor:         %s\n" % self.Vendor
        returnString += "Model:          %s\n" % self.Model
        returnString += "Gauge:          %d\n" % self.Gauge
        returnString += "SegmentSize:    %f\n" % self.SegmentSize
        returnString += "Rcable:         %f\n" % self.Rcable
        returnString += "Lcable:         %f\n" % self.Lcable
        returnString += "Ccable:         %f\n" % self.Ccable
        returnString += "TransferFunc:   %s\n" % self.TransferFunc
        return returnString

class MultidropSimulationNetworkSpreadsheetDescription(object):
    """Contains an entire multidrop network model consisting of sveral nodes and cable 
    configureations."""
    def __init__(self, excelFileName):
        self.nodeConfigs = []
        self.cableSegConfigs = {}
        wb = load_workbook(excelFileName, data_only=True)

        sheet = wb['Cables']
        cableSegConfigDictList = self.sheetToListOfDictsKeyedByHeaderRow(sheet, 0)
        for cableSegConfigDict in cableSegConfigDictList:
            self.appendCableModelConfig(CableSegmentModelConfig(cableSegConfigDict))

        sheet = wb['Networks']

        nodeConfigDictList = self.sheetToListOfDictsKeyedByHeaderRow(sheet, 0)

        for nodeConfig in nodeConfigDictList:
            self.appendNodeConfig(MultiDropSimulationNodeConfig(nodeConfig))
    
    def __str__(self):
        returnString = "MultidropSimulationNetworkSpreadsheetDescription\n"
        returnString += "Node Configs:\n"
        for nodeConfig in self.nodeConfigs:
            returnString += str(nodeConfig)
        
        returnString += "Cable Segment Configs:\n"
        for cableSegConfigKey in self.cableSegConfigs.keys():
            returnString += str(self.cableSegConfigs[cableSegConfigKey])
        return returnString



    def appendNodeConfig(self, nodeConfig):
        """Appends a node config to the list of nodes"""
        self.nodeConfigs.append(nodeConfig)

    def appendCableModelConfig(self, cableSegConfig):
        """Add a cable model to the dict that stores them by their unique CableModelKey"""
        self.cableSegConfigs[cableSegConfig.CableModelKey] = cableSegConfig

    def getStubCableModelForNodeConfig(self, nodeConfig):
        """Retrieve a cable model from  the dict that stores them by their unique CableModelKey for stubs"""
        return self.cableSegConfig[nodeConfig.StubCableModel]

    def getLineCableModelForNodeConfig(self, nodeConfig):
        """Retrieve a cable model from  the dict that stores them by their unique CableModelKey for lines"""
        return self.cableSegConfig[nodeConfig.LineCableModel]


    def sheetToListOfDictsKeyedByHeaderRow(self, sheet, headerRowNumber=0):
        """Creates a list of ordered dicts using the header row of a worksheet as the keys.
        Note header row number is zero-based, thus 0 is the default for top row header."""
        sheetList = []
        rowDict = collections.OrderedDict()

        headerRow = [header.value for header in list(sheet.rows)[headerRowNumber]]
        for row in list(sheet.rows)[headerRowNumber+1:]:
            for (colNumber, cell) in enumerate(row):
                rowDict[headerRow[colNumber]] = cell.value
            sheetList.append(rowDict)
            rowDict = {}

        return sheetList
   
class ConsensusModelTopologyBuilder(object):
    """Creates topology"""
    def __init__(self):
        self.initRandomness()
        self.simNetwork = None
        self.args = None

    def initRandomness(self, seed=-1):
        ###
        #Setup random seed in case this run has random parameters
        ###
        if seed == -1:
            tim = datetime.datetime.now()
            seed = tim.hour*10000+tim.minute*100+tim.second
            random.seed(seed)
        else:
            random.seed(seed)
        print("#Random Seed = %s" % seed)

    def buildFromCommandLineArguments(self, args):
        self.simNetwork = MultidropSimulationNetwork()
        self.args = args

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

        #llump = l_m / self.args.segments_per_meter
        #clump = c_m / self.args.segments_per_meter
        #rlump = r_m / self.args.segments_per_meter 

        ################################################################################
        #Make trunk segments that will connect the nodes
        ################################################################################
        self.simNetwork.trunk=Trunk( length=self.args.length
                , nodes=self.args.nodes
                , start_pad=self.args.start_pad
                , end_pad=self.args.end_pad
                , separation_min=self.args.separation_min
                , start_attach=self.args.start_attach
                , end_attach=self.args.start_attach
                , random_attach=self.args.random_attach
                , attach_error=self.args.attach_error
                )
        trunk_segments = self.simNetwork.trunk.get_cable_segments()
        # for x in trunk_segments:
        #     print(x)
        
        ################################################################################
        #Connect termination Resistors (actually termination R/C) to then ends of
        #the trun
        ################################################################################
        self.simNetwork.term_start = Termination(name="start_term", port=trunk_segments[0].port1, stim_port="start")
        self.simNetwork.term_end   = Termination(name="end_term"  , port=trunk_segments[-1].port2, stim_port="end")

        ################################################################################
        #Attach nodes to the trunk
        ################################################################################
        self.simNetwork.nodes = []
        for n in range(1,self.args.nodes+1):
            port="t%d" % (n)
            node = Node(number=n,port=port, drop_length=self.args.drop_max, random_drop=self.args.random_drop,
                    cnode=self.args.cnode, lpodl=self.args.lpodl, rnode=self.args.rnode)
            self.simNetwork.nodes.append(node)

        ################################################################################
        #Determine which node will be the transmitter for the simulation
        ################################################################################
        #boundary check the transmit node index
        self.simNetwork.tx_node = self.args.tx_node
        if self.simNetwork.tx_node<1: #choose a random transmit node
            self.simNetwork.tx_node = random.randint(1,self.args.nodes)
            print("Randomly Chose Node %d as the transmitter" % self.simNetwork.tx_node)
        self.simNetwork.tx_index=min(self.simNetwork.tx_node, self.args.nodes)
        self.simNetwork.tx_index=max(self.simNetwork.tx_index, 1)
        self.simNetwork.tx_node = self.simNetwork.nodes[self.simNetwork.tx_index-1]
        self.simNetwork.transmitter = Transmitter(port=self.simNetwork.tx_node.phy_port)
        
    def renderNetlist(self):
        ################################################################################
        #Write a spice file with the system setup
        ################################################################################
        with open("cable.p", 'w') as cable:
            cable.write("*lumped transmission line model with %d segments per meter at %d meters\n"\
            % (self.args.segments_per_meter, self.args.length))
            cable.write("*and a %f meter long cable\n" % self.args.length)
            cable.write(".include tlump2.p\n")
            cable.write(".include node.p\n")

            trunk_segments = self.simNetwork.trunk.get_cable_segments()

            for s in trunk_segments:
                cable.write(s.subcircuit()+"\n")
            for n in self.simNetwork.nodes:
                cable.write(n.subcircuit()+"\n")

            cable.write(self.simNetwork.term_start.subcircuit()+"\n")
            cable.write(self.simNetwork.term_end.subcircuit()+"\n")
            cable.write("** MAIN NETWORK DESCRIPTION **\n")
            for s in trunk_segments:
                cable.write(s.instance()+"\n")
            for n in self.simNetwork.nodes:
                cable.write(n.instance()+"\n")
            cable.write(self.simNetwork.term_start.instance()+"\n")
            cable.write(self.simNetwork.term_end.instance()+"\n")
   

if __name__ == '__main__':
    
    network = MultidropSimulationNetworkSpreadsheetDescription("MultiDropTopologySampleInput.xlsx");
    print(network)


