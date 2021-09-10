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


class ConsensusModelSimulator(object):
    """Stores topology, runs sim, stores results"""
    def __init__(self):
        self.network = None
        self.results = None
        self.design_md5 = None
        self.transmitter = None
        self.nodes = None

    def getResults(self):
        self.results = ltcsimraw(self.rawSave)
        return self.results

    def run(self):
        """Executes simulation using topology in self.network"""
        
        ################################################################################
        #Set up and run a simulation, but don't run it twice if it has already been
        #run
        ################################################################################
        
        self.createAcStimulusFile()
        self.compileSpice()
        if not self.wasSameSimPreviouslyRun():
            print( "Running Simulation")
            runspice.runspice(self.spiSave)

    def compileSpice(self):
        #condense the sim files into a single *.spi file
        self.spi = SpiFile(self.cirfile)
        self.spi.readCircuit()
        self.spi.followInclude = True
        self.spi.digestSpiceFile()


    def createAcStimulusFile(self):
        ################################################################################
        #Create an ac stimulus file
        #This is separate from the system spice file in case we also want to do
        # transient simulations.  Then another transient stimulus file will be
        # created
        ################################################################################
        with open("zcable.ac.cir", 'w') as zcable:
            zcable.write("*ac sim command for cable impedance measurement\n")
            zcable.write(".include cable.p\n")

            #differential signal input
            zcable.write(self.transmitter.instance()+"\n")

            #path to ground
            zcable.write("vrtn rtn 0 0\n")

            #simulation command
            zcable.write(".ac lin 400 1meg 40meg\n")

            #select nodes to save to speed up the sim and reduce file size
            zcable.write(".save v(*) i(*)\n")
            for n in self.nodes:
                zcable.write("+ %s\n" % n.termination_current())


        self.cirfile = "zcable.ac.cir"
        self.rawfile = "zcable.ac.raw"

    def wasSameSimPreviouslyRun(self):

        #crete a md5 of the spi file then make a unique directory to store this sim
        #If batches of sims are run more than once, just extract the data without 
        #running the sim again
        self.design_md5 = self.spi.md5(skipParams=False,skipComments=True,skipSave=False)
        self.spiSave  = os.path.join("data",self.design_md5,self.design_md5+".spi")
        self.logSave  = os.path.join("data",self.design_md5,self.design_md5+".log")
        self.rawSave  = os.path.join("data",self.design_md5,self.design_md5+".raw")
        self.outputdb = os.path.join("data",self.design_md5)
        #print( self.design_md5)

        if not os.path.exists("data"):
            print( "Data Folder does not exist")
            print( "Creating...." )
            try:
                os.makedirs("data")
            except:
                print( "Cannot create data folder")
                exit(1)

        if not os.path.exists(self.outputdb):
            print( "Regression Folder %s does not exist" % self.design_md5)
            print( "Creating...." )
            try:
                os.makedirs(self.outputdb)
                self.spi.outputToFile(self.spiSave)
            except:
                print( "Cannot create regression folder")
                exit(1)

        #if there is already raw and log data in the md5 directory then assume the sim has 
        #already been run, otherwise run the sim
        try:
            open(self.spiSave,"r")
            #print( self.spiSave)
            open(self.logSave,"r")
            #print( self.logSave)
            open(self.rawSave,"r")
            #print( self.rawSave)
            print( "Pulling Sim From database %s" % self.design_md5) 

        except:
            print( "Simulation Not in Cache")
            return False
            

        return True

