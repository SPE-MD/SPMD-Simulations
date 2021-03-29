#! /usr/bin/env python

import re
import sys
from os.path import dirname
import os.path 
import copy
import argparse
import hashlib

sys.path.append(dirname(__file__)) #adds this file's director to the path

class SpiFile(object):
    def __init__(self,spifile):
        self.spifile = spifile
        self.text = [] #raw spice file read in
        self.joined = [] #spice file without line breaks
        self.subckts = {} #hash of subcircuits vs their names
        self.instances = {} #hash of flattened instances in heirarchy
        self.includeFiles = []
        self.followInclude=True
        self.stop = set([])

    def readCircuit(self,infile=None):
        #print infile
        if(infile==None):
            infile = self.spifile
       
        #ntrys=0
        #file=None
        #while file==None and os.path.isfile(infile):
        #    try:
        #        file=open(infile)
        #        break
        #    except:
        #        print "rawfile: cannot open: %s" % infile
        #        ntrys += 1
        #        if(ntrys > 100):
        #            exit(1)

        try :
            file = open(infile)
        except:
            print "cannot open: %s" % infile
            return None

        with file as inf:
            for line in inf:
                line = line.rstrip()
                self.text.append(line)

    #cirfile is an array holding the lines from the spice/cir file
    def digestSpiceFile(self):
        #self.readCircuit()
        line_continue = re.compile('^\+')
        self.joined = []
        for i,line in enumerate(self.text):
            line = line.lower()
            cont = line_continue.match(line)
            if(cont):
                newline = " " + line[1:]
                #print "%d\t%s" % (i,newline)
                self.joined[-1] += newline
            else:
                self.joined.append(line)

            if self.joined[-1].startswith(".inc"):
                ln = self.joined[-1].split()
                self.includeFiles.append(ln[1])
                isCirFile = ln[1].endswith(".cir")
                if(self.followInclude or isCirFile):
                    print "FOLLOWING %s" % ln[1]
                    inc = self._followInclude(self.joined[-1])
                    self.joined.pop()
                    self.joined.extend(inc)

        return self.joined

    def _followInclude(self,line):
        #print self.spifile
        #print line
        print os.path.abspath(self.spifile)
        dir = os.path.dirname(os.path.abspath(self.spifile))
        ln = line.split()
        inc = ln[1]
        path = os.path.join(dir,inc)
        #print path
        #print os.path.isfile(path)
        circuit = SpiFile(path)
        circuit.readCircuit(path)
        circuit.digestSpiceFile()
        return list(circuit.joined)

    def outputToFile(self,fileName=None):
        if fileName==None:
            fileName = self.spifile
        try:
            with open(fileName,"w") as cir:
                #cir.write("* re-netlist of %s by SpiFile\n" % self.spifile)
                for i in self.joined:
                    cir.write(i+"\n")
        #############################
        except:
            print "issue creating new spifile : %s " % test.spifile


    def md5(self,skipParams=False,skipComments=False,skipSave=False):
        m = hashlib.md5()
        buf = ""
        for i in self.joined:
            if skipParams and i.startswith(".param"):
                continue
            if skipComments and i.startswith("*"):
                continue
            if skipSave and i.startswith(".save "):
                continue
            else:
                buf += i
        m.update(buf)
        return m.hexdigest()
