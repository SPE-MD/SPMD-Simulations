#! /usr/bin/env python3

#Copyright  2021 <Analog Devices>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import re
import sys
from os.path import dirname
import os.path 
import copy
import argparse
import hashlib

sys.path.append(dirname(__file__)) #adds this file's director to the path
# sys.path.append(os.path.join(os.environ['MP_SCRIPTS'])) #adds this file's director to the path
# sys.path.append(os.path.join(os.environ['MP_SCRIPTS'],"ide")) #adds this file's director to the path
#import mpUtil
#from mcalc import Mcalc as mcalc
#from subcircuit import Subcircuit as subcircuit
#from instance import Instance as Instance

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
        #print( infile)
        if(infile==None):
            infile = self.spifile
       
        #ntrys=0
        #file=None
        #while file==None and os.path.isfile(infile):
        #    try:
        #        file=open(infile)
        #        break
        #    except:
        #        print( "rawfile: cannot open: %s" % infile)
        #        ntrys += 1
        #        if(ntrys > 100):
        #            exit(1)

        try :
            file = open(infile)
        except:
            print( "cannot open: %s" % infile)
            return None

        with file as inf:
            for line in inf:
                line = line.rstrip()
                self.text.append(line)

    def readStoplist(self,stoplist):
        try :
            file = open(stoplist)
        except:
            print( "cannot open: %s" % stoplist)
            return None

        with file as inf:
            for line in inf:
                line = line.rstrip()
                self.stop.add(line)

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
                #print( "%d\t%s" % (i,newline))
                self.joined[-1] += newline
            else:
                self.joined.append(line)

            if self.joined[-1].startswith(".inc"):
                ln = self.joined[-1].split()
                self.includeFiles.append(ln[1])
                isCirFile = ln[1].endswith(".cir")
                if(self.followInclude or isCirFile):
                    #print( "FOLLOWING %s" % ln[1])
                    inc = self._followInclude(self.joined[-1])
                    self.joined.pop()
                    self.joined.extend(inc)

        return self.joined

    def _followInclude(self,line):
        #print( self.spifile)
        #print( line)
        #print( os.path.abspath(self.spifile))
        dir = os.path.dirname(os.path.abspath(self.spifile))
        ln = line.split()
        inc = ln[1]
        path = os.path.join(dir,inc)
        #print( path)
        #print( os.path.isfile(path))
        circuit = SpiFile(path)
        circuit.readCircuit(path)
        circuit.digestSpiceFile()
        return list(circuit.joined)

    def modifyParameter(self,parameter,new_value):
        for i,l in enumerate(self.joined):
            if l.startswith(".param %s" % parameter):
                self.joined[i] = ".param %s=%s" % (parameter,new_value)
            elif parameter == "temp" and l.startswith(".temp"):
                self.joined[i] = ".temp %s" % (new_value)

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
            print( "issue creating new spifile : %s " % test.spifile)


    #creates a dictionary of sub-circuits using the sub-circuit name as the hash key
    #returns the dictionary
    def subCircuitHash(self):
        re_main_network = re.compile('main network description')
        re_subckt = re.compile('^.subckt',flags=re.IGNORECASE)
        re_ends = re.compile('^.ends',flags=re.IGNORECASE)
        re_model = re.compile('^.model',flags=re.IGNORECASE)
        re_param = re.compile('^.param',flags=re.IGNORECASE)
        re_lib = re.compile('^.lib',flags=re.IGNORECASE)
        re_endl = re.compile('^.endl',flags=re.IGNORECASE)
        re_comment = re.compile('^\*')
        re_leadspace = re.compile('^\s*$')
        re_nonword = re.compile('^\W')

        #name of the current subckt being parsed
        #sname  = None
        sname="main_network_description"
        self.subckts = {}
        self.subckts[sname] = subcircuit(sname)
        for line in self.joined:
            #print( sname)
            #print( line)
            if re_main_network.search(line):
                sname="main_network_description"
                self.subckts[sname].addSubcktDef(line)
                continue
            if(re_subckt.search(line)):
                ln = line.split()
                sname=ln[1]
                if(sname in self.stop):
                    #print( "stop: " + sname)
                    #sname  = None
                    sname="main_network_description"
                else:
                    #print( "add : " + sname)
                    #initalize new object here
                    self.subckts[sname] = subcircuit(sname)
                    self.subckts[sname].addSubcktDef(line)
                continue
            elif(re_ends.search(line)):
                sname="main_network_description"
                continue
            elif(re_comment.search(line)):
                #print( "comment")
                #print( line)
                continue
            elif(re_leadspace.search(line)):
                #print( "leadspace: %s" % line)
                continue
            elif(re_param.search(line)):
                #print( sname)
                #print( line)
                self.subckts[sname].addBodyParam(line)
                continue
            elif(re_model.search(line)):
                sname = None
                pass
            elif(re_lib.search(line)):
                sname = None
                pass
            elif(re_endl.search(line)):
                sname = None
                pass
            elif(re_nonword.search(line)):
                print( "nonword: |%s|" % line)
                continue
            if(sname is None) :
                sname="main_network_description"
                continue
            self.subckts[sname].addLine(line)

        #sort the bodies so that the print order is consistent
        for k,v in self.subckts.iteritems():
            v.sortBody()

        return self.subckts

    #def flatten(self):
    #flatten is a recursive-ish call
    #call it with inst=None when entering for the 1st time.
    #it would normally be entered with main_network_description as the subckt
    #inst is a dictionary that is made by parseInstance
    #it contains the info about the line that instantiated the subcircuit
    #flatten gets called within the subckt object that corresponds to the
    #instance

    #this makes the netlist heirarchical but instanced.
    def instantiate(self):
        mc = mcalc()
        self.instances = self.subckts["main_network_description"].flatten(mc,self.subckts)
        self._flatNetlist()
        return self.instances

    def findNet(self,net):
        for i in self.flat:
            if net in i:
                print( i)

    def netDevices(self,net,heirarchy=None):
        if(heirarchy == None):
            heirarchy = self.instances
        pins = []
        for k in heirarchy:
            pins.extend(k.getNetPin(net))
        return pins   

    #used to be called printHeirarchy
    #dont call this directly just read from spifile.flat
    def _flatNetlist(self,heirarchy=None):

        if(heirarchy == None):
            heirarchy = self.instances
            self.flat = []

        #keys = heirarchy.keys()
        for k in heirarchy:
            self.flat.extend(k.flatten())
        return self.flat

    def parseSettingsFile(self,settings):
        try :
            file = open(settings)
        except:
            print( "cannot open: %s" % settings)
            return None

        lib = None
        with file as inf:
            for line in inf:
                line = line.rstrip()
                if line.startswith("LIB"):
                    ln = line.split()
                    libfile = os.path.join(os.environ['PROJECTS'],ln[1]) #adds this file's director to the path
                    self.readCircuit(libfile)

        file.close()
        return lib

    #makes a new netlist with the main network description as defined by "subcircuit"
    def makeNewMain(self,subcircuit):
        #make sure the subcircuit hash exists
        self.subCircuitHash()

        #if subcircuit is not in subcircuit hash rebuild the netlist with the
        #existing main network description.  At least the new netlist will be
        #sorted
        if not subcircuit in self.subckts:
            subcircuit="main_network_description"

        #recursive call that builds a list of subcircuits needed by the new main
        subs = self.subckts[subcircuit].subcktTree(self.subckts)
        #sort and print so they show up the same way every time
        netlist = ["*renetlist of %s from %s to make %s top level" %\
                (subcircuit,self.spifile,subcircuit)]
        for s in sorted(subs):
            self.subckts[s].sortBody()
            netlist.extend(self.subckts[s].subcktToArray())
        netlist.append("* main network description")
        self.subckts[subcircuit].sortBody()
        netlist.extend(self.subckts[subcircuit].body)

        newspi = SpiFile("%s.spi" % subcircuit)
        newspi.joined = netlist

        return newspi


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
        m.update(buf.encode('utf-8'))
        return m.hexdigest()

if __name__ == '__main__':

    dot_ide = os.path.join(os.environ['PROJECTS'],".ide") #adds this file's director to the path

    if(len(sys.argv) > 1 and sys.argv[-1] != None) :
        infile = sys.argv.pop()
        if(not os.path.isfile(infile)):
            exit(1)
    else:
        exit(1)

    circuit = SpiFile(infile)
    circuit.readCircuit(infile)

    circuit.digestSpiceFile()

    circuit.subCircuitHash()
    instances = circuit.instantiate()

    #newspi = circuit.makeNewMain("ilim_dac3")
    #print( newspi.md5(True,True,True))
    #
    #newspi2 = circuit.makeNewMain("pm_tub5v5")
    #print( newspi2.md5(True,True,True))

    #newspi3 = circuit.makeNewMain("main_network_description")
    #print( newspi3.md5(True,True,True))
    #newspi3.outputToFile("main.spi")

    #exit(0)
    for i in circuit.flat:
        if(i.model == None):
            print( "wierd %s" % i)
        else:
            if i.children:
                print( "*%s" % i)
            else:
                print( i)
            pass
