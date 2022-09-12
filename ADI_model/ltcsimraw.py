#! /usr/bin/env python3

#Copyright  2021 <Michael Paul>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import sys
import string
import struct
import math
import re
import numpy as np
import argparse

from os.path import dirname
import os.path 
sys.path.append(dirname(__file__)) #adds this file's director to the path
import mpUtil

class ltcsimraw():

    def __init__(self,rawfile):
        self.rawfile = rawfile
        self.preamble = {}

        #hash of variable names to number in the rawfile
        self.variableNumber = {}
        self.variables = []
        self.binary_start = 0
        self.nvars = 0
        self.points = 0
        #differently

        self.filehandle = None
        self.timePoint = 0
        #self.mcalc = Mcalc()
        

        ntrys=0
        file=None
        if not os.path.isfile(self.rawfile):
            print("Raw File does not exist!\n-> ",self.rawfile)
            exit(1)

        while file==None and os.path.isfile(self.rawfile):
            try:
                file=open(self.rawfile, "rb")
                break
            except:
                print( "rawfile: cannot open: %s" % rawfile)
                ntrys += 1
                if(ntrys > 100):
                    exit(1)

        with file as inf:
            self.x64 = self.detectX64File(inf)
            self.readPreamble(inf)
            self.readVariables(inf)
            
            self.binary_start = inf.tell()

        file.close()
        self.complex_data = False
        if "complex" in self.preamble['Flags']:
            self.complex_data = True

    
    #If the First 2
    def detectX64File(self,file):
        fpointer = file.tell()
        file.seek(0,0)
        r = file.read(2)
        file.seek(fpointer,0)
        if r[0]== ord('T') and  r[1]==0:
                return True
        return False

    def lt_readline(self,file):
        line = ""
        keep_reading=True
        nread=1

        #In ltcsim x64 the ascii characters are being written as 16bit
        #chars, for example 'T' is written to the file as 'T\0'
        #If x64 is detected read the chars as 16 bits and throw away the 
        #trailing '\0'
        if self.x64==True:
            #print("Reading x64 file")
            nread=2
        else:
            pass
            #print("Reading x32 file")
        while(keep_reading):
            r = file.read(nread)
            #print("r len: ", len(r))
            r = r[0]
            if(r==ord('\n')):
                keep_reading=False
            elif(r==ord('\0')):
                print( "Should never get here!!!")
                pass
            else:
                line += chr(r)
        #print(line)
        return line

    def readPreamble(self,file):
        self.preamble = {}
        #for line in iter(file.readline, ''):
        while(True):
            line = self.lt_readline(file)
            #print( line)
            if line.startswith("Variables:"):
                break
            line = line.rstrip()
            #print( "#" + line)
            ln = line.split(": ") 
            print( line)
            #print( ln)
            self.preamble.update({ln[0]:ln[1]})

        self.nvars =  int(self.preamble['No. Variables'])
        self.points = int(self.preamble['No. Points'])
        #self.x64 = int(


    def readVariables(self,file):
        self.variables = [] 
        #for line in iter(file.readline, ''):
        while(True):
            line = self.lt_readline(file)
            if line.startswith("Binary:"):
                break
            line = line.rstrip()
            #print( line)
            ln = line.split()
            #variableNumber[ln[1].lower()] = ln[0]
            self.variables.append(ln[1].lower())

        for i,v in enumerate(self.variables):
            self.variableNumber[v] = i


    
    #pass a variable number to be extracted from the file
    def getSignal(self,varnums):

        sig = []
        time = []
        with open(self.rawfile, "rb") as f:
            #print( self.binary_start)
            f.seek(self.binary_start)
            size = self.getChunkSize(f)
            ans = []
            tp = []
            
            for n in range(self.points):
                chunk = f.read(size)
                if chunk:
                    if self.complex_data:
                        p = self.readComplex(chunk,varnums)
                        tp.append(p[0])
                        for i,v in enumerate(varnums):
                            #readComplex adds the frequency to the list
                            #the +1 in the following line corrects for it.
                            tp.append(p[i+1])
                        ans.append(tp)
                        tp = []
                    else:
                        p = self.readReal(chunk,varnums)
                        ans.append(p)
            f.close()
        
        return ans

    #parses complex number from a chunk of the file.
    def readComplex(self, chunk, signals):
        x = struct.unpack('d',chunk[0:8])[0]
        ret = [abs(x)]
        for y in signals:
            start = y * 16 
            end = start + 16
            p = struct.unpack('dd',chunk[start:end])
            ret.append(complex(p[0],p[1]))
        return ret

    def readReal(self,chunk,signals):
        x = struct.unpack('d',chunk[0:8])[0]
        ret = [abs(x)]
        #print( x)
        for y in signals:
            start = (y * 4) + 4
            end = start + 4
            p = struct.unpack('f',chunk[start:end])[0]
            #print( p)
            ret.append(p)
        return ret

    #returns the size of 1 data point in the file
    #this is the x-axis info plus all of the variables for one point on the
    #x-axis
    def getChunkSize(self,handle):
        x = handle.tell()
        handle.seek(0,2) #seeks to the end of the file
        end = handle.tell()
        nbytes = end-self.binary_start
        handle.seek(x)
        return nbytes//self.points

    def readLastTimePoint(self):
        if self.filehandle == None:
            self.filehandle = open(self.rawfile, "rb")
            self.filehandle.seek(self.binary_start,0)
            self.chunkSize = self.getChunkSize(self.filehandle)
            self.filehandle.seek(-1 * self.chunkSize,2)

            #tstop = float(mpUtil.decodeEngineeringNotation(args.tstop))
            #istop = rf.searchTime(tstop)

        chunk = self.filehandle.read(self.chunkSize)
        readFunc = self.readReal
        if self.complex_data:
            readFunc = self.readComplex

        if chunk:
            v = range(1,self.nvars)
            self.tp = readFunc(chunk,v)
            return True
        return False

    def readTimePoint(self):
        if self.filehandle == None:
            self.filehandle = open(self.rawfile, "rb")
            self.filehandle.seek(self.binary_start,0)
            self.chunkSize = self.getChunkSize(self.filehandle)

        chunk = self.filehandle.read(self.chunkSize)
        readFunc = self.readReal
        if self.complex_data:
            readFunc = self.readComplex

        if chunk:
            v = range(1,self.nvars)
            self.tp = readFunc(chunk,v)
            return True
        return False

    def copyRawFile(self):
        if self.filehandle == None:
            self.filehandle = open(self.rawfile, "rb")
            self.filehandle.seek(self.binary_start,0)
            self.chunkSize = self.getChunkSize(self.filehandle)

        self.filehandle.seek(0)
        header = self.filehandle.read(self.binary_start)
        of = open("concat.raw", "wb")
        of.write(header)
        data = self.filehandle.read(4096)
        of.write(data)
        of.write(struct.pack('d',0.0))
        of.write(data)
        of.close()
        exit(0)

    #works with readTimePoint....
    def getVal(self,var):
        i = self.variableNumber[var]
        return self.tp[i]

    def getSignals(self, vlist, ilist, others=[]):

        y = []
        labels = ["time"]
        for v in vlist:
            s = "v(%s)" % v.lower()
            for i in self.variables:
                if s in i:
                    #print( i)
                    y.append(self.variableNumber[i])
                    labels.append(s)
                    continue

        for i in ilist:
            s = "(%s)" % i.lower()
            for i in self.variables:
                if i.startswith("i") and s in i:
                    y.append(self.variableNumber[i])
                    labels.append(i)
                    continue

        for x in others:
            s = x.lower()
            for i in self.variables:
                if s in i:
                    #print( self.variableNumber[i])
                    y.append(self.variableNumber[i])
                    labels.append(i)
                    continue

        #print( y)
        sig = self.getSignal(y)
        return (sig, labels)

    def scattering_parameters(self, vport1, iport1, vport2, iport2, rin=50,
            rout=50):
        (data,labels) = self.getSignals([],[],[vport1[0],vport1[1],vport2[0],vport2[1],iport1,iport2])
        index = dict(zip(labels, range(0,len(labels))))
        #print(labels)
        frequency=[]
        s11=[]
        s11_phase=[]
        dm_cm=[]
        s21=[]
        gain=[]
        phase=[]
        zin=[50]
        zin_mag=[]
        zin_phase=[]
        for x in data:
            vend_cm = (x[index[vport2[0]]]+x[index[vport2[1]]])/2
            vend    = x[index[vport2[0]]]-x[index[vport2[1]]]
            iend    = x[index[iport2]]
            vin     = x[index[vport1[0]]]-x[index[vport1[1]]]
            iin     = x[index[iport1]]
            rin     = 50
            rout    = 50
            a1 = (vin + (iin*rin))
            b1 = (vin - (iin*rin))
            a2 = (vend + (iend*rout))
            b2 = (vend - (iend*rout))
            s11_mp  = self.decodeComplex(a1 / b1)
            s21_mp  = self.decodeComplex(b2 / a1)
            gain_mp = self.decodeComplex(vend/vin)
            dm_cm_mp = self.decodeComplex(vend_cm/vin)
            frequency.append(x[0])
            s11.append(s11_mp[0])
            s11_phase.append(s11_mp[1])
            s21.append(s21_mp[0])
            gain.append(gain_mp[0])
            phase.append(gain_mp[1])
            dm_cm.append(dm_cm_mp[0])
            zin.append(vin / iin)
            zin_mag.append(pow(10,self.decodeComplex(vin/iin)[0]/20))
            zin_phase.append(self.decodeComplex(vin/iin)[1])

        return {
            "frequency" : frequency,
            "s11" : s11,
            "s11_phase" : s11_phase,
            "s21" : s21,
            "gain" : gain,
            "phase" : phase,
            "zin" : zin,
            "zin_mag" : zin_mag,
            "zin_phase" : zin_phase,
            "dm_cm" : dm_cm,
            }

    def fft_transfer(self, fft, vport1, vport2):
        (data,labels) = self.getSignals([],[],[vport1[0],vport1[1],vport2[0],vport2[1]])
        index = dict(zip(labels, range(0,len(labels))))
        #print(labels)
        #frequency=[]
        #fft_out = [0]
        fft_out =  [complex(1e-30,0)]
        for i in range(0,len(data)):
            vend   = data[i][index[vport2[0]]]-data[i][index[vport2[1]]]
            vin    = data[i][index[vport1[0]]]-data[i][index[vport1[1]]]
            #gain_mp = self.decodeComplex(vend/vin)
            phasor_out = fft[i+1] * (vend/vin)
            fft_out.append(phasor_out)
            #frequency.append(data[i][0])

        return fft_out

    def fft_zin(self, fft, vport1, iport):
        (data,labels) = self.getSignals([],[],[vport1[0],vport1[1],iport])
        index = dict(zip(labels, range(0,len(labels))))
        #print(labels)
        #frequency=[]
        #fft_out = [0]
        fft_out =  [complex(1e-30,0)]
        for i in range(0,len(data)):
            zin    = data[i][index[vport1[0]]]-data[i][index[vport1[1]]] / data[i][index[iport]]
            #gain_mp = self.decodeComplex(vend/vin)
            phasor_out = fft[i+1] * zin
            fft_out.append(phasor_out)
            #frequency.append(data[i][0])

        return fft_out

    #changes the data from an aoa to an array of strings suitable for feeding to
    #gnuplot
    def setGnuplotFormat(self,sig,labels):
        out = []
        out.append( "#" + " ".join(labels))
        timelast = -1000000;
        nsteps = 1
        for i in sig:
            if timelast > i[0]:
                out.append("e\n\n")
                nsteps += 1
            out.append(" ".join(format("%.6e" % x) for x in i))
            timelast = i[0];
        out.append("e\n\n")
        out.append("#" + " ".join(labels))
        return (out, nsteps)

    #changes real/imag into db/degrees
    def decodeComplex(self,cmplx):
        a=np.array([cmplx.real,cmplx.imag])
        a.dtype = complex
        ans = (20*math.log10(np.absolute(a)), \
            np.angle(a,deg=True)[0])
        return ans

    def plotComplex(self,sigs,nsteps,names,corners):
        import subprocess
    
        for c in corners:
            print( c)
        gnuplot_bin = ['/usr/bin/env', 'gnuplot','-persist', '-']
        gp = subprocess.Popen(gnuplot_bin,stdin = subprocess.PIPE,
        stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        title = "set title '%s'\n" % names[0]
        #gp.stdin.write(title)
        gp.stdin.write("set multiplot layout 2,1 title 'AC Response'\n")
        #gp.stdin.write("unset key\n")
        gp.stdin.write("set key outside right\n")
        #gp.stdin.write("set xlabel 'time'\n")
        gp.stdin.write("set format x \"%.0s%c\" \n")
        gp.stdin.write("set logscale x\n")
        #gp.stdin.write("labels = \"%s\"" % corners)
    
        #gp.stdin.write("plot for [corner in labels] '-' u 1:2 w l" % nsteps)
        gp.stdin.write("plot for [corner=1:%d] '-' u 1:2 w l t sprintf(\"%%d\",corner)" % nsteps)
        #gp.stdin.write("plot for [corner=1:%d] '-' u 1:2 w l" % nsteps)
    
        for i in sigs:
            line = i + "\n"
            #line = i 
            gp.stdin.write(line)
            gp.stdin.flush()
    
        gp.stdin.write("set yrange [-180:180] \n")
        gp.stdin.write("set ytics -180,60,180\n")
        gp.stdin.write("set xlabel 'frequency'\n")
        #gp.stdin.write("plot for [corner=1:%d] '-' u 1:3 w l" % nsteps)
        gp.stdin.write("plot for [corner=1:%d] '-' u 1:3 w l t sprintf(\"%%d\",corner)" % nsteps)
        for i in sigs:
            line = i + "\n"
            #line = i 
            gp.stdin.write(line)
            gp.stdin.flush()
    
        gp.stdin.write("unset multiplot")
        #for line in iter(gp.stderr.readline,''):
               #print( line.rstrip())
        gp.communicate('e\nquit\n')

    #pass the rawfile object
    def searchTime(self,time):
        s = self.getSignal([0])
        index=0
        return _binarySearch(s,time,0,len(s))

def _binarySearch(timeSeries,time,start,end):
    mid = (end + start) / 2 
    #print( "%d\t%e\t%e" % (mid, timeSeries[mid][0],time))
    if(mid == start or mid == end):
        return mid
    if(time < timeSeries[mid][0]):
        return _binarySearch(timeSeries,time,start,mid)
    elif(time > timeSeries[mid][0]):
        return _binarySearch(timeSeries,time,mid,end)
    else:
        return mid

if __name__ == '__main__':

    #if(len(sys.argv) > 1):#ys.argv[1]):
    #    rawfile = sys.argv[1]
    #    if(not os.path.isfile(rawfile)):
    #        rawfile = None

        
    ## example:
    #for b in bytes_from_file('filename'):
    #    do_stuff_with(b)

    dot_ide = os.path.join(os.environ['PROJECTS'],".ide") #adds this file's director to the path
    parser = argparse.ArgumentParser(
        description='extract data from an ltspice .raw file'
        )

    parser.add_argument('--xfer', type=str, \
            help='open loop gain analysis using impedance sensitive probe\n \
            pass the subcircuit name of the probe (xp for example)')

    parser.add_argument('-b', '--bias', action='store_true', help='print out\
            bias voltages suitable for a .loadbias call')

    parser.add_argument('-c', '--copy', action='store_true', help='\
            copies a rawfile. not really useful')

    parser.add_argument('-s', '--sub', action='store_true', help='print\
            substrate currents')

    parser.add_argument('--preamble', action='store_true', help='print\
    the preamble')

    parser.add_argument('--plot', action='store_true', help='send the output to\
    gnuplot.  only works with the -i or -v options')

    parser.add_argument('--multiplot', action='store_true', help='send the output to\
    gnuplot.  Each distict waveform is in its own window. Only works with the -i or -v options')

    parser.add_argument('-l', '--list', action='store_true', help='print\
    the signal names')

    parser.add_argument('-m', '--match', metavar='match', type=str, 
        help='node name to match.  Match starts with I and ends with "match")')

    parser.add_argument('-t', '--stats', metavar='signal', dest='signal', type=str,
        help='USE ISLEUTH.py instead full signal names to match.  Prints out stats on the names. \
    Example: Use spifile.py to get a list of nodes that sink current. \
    Then feed the list to this to find the ones that are talking too much current' \
            )

    parser.add_argument('--tstart', metavar='time', help=' \
    time to start extraction')

    parser.add_argument('--tstop', metavar='time', help=' \
    time to end extraction')

    parser.add_argument('-v', '--volt', metavar='volt', type=str, nargs='+',
        default=[],
        help='list of voltages to extract (whitespace delimited)\
    separate two names with a comma (,) to have the nodes plotted differentially')

    parser.add_argument('-i', '--current', metavar='current', type=str, nargs='+',
        default=[],
        help='list of currents to extract')

    if(len(sys.argv) > 1 and sys.argv[-1] != None):
        rawfile = sys.argv.pop()
        #print( rawfile)
    else:
        parser.print_help()
        exit(1)

    args = parser.parse_args()
    #print( "*" + args)

    rf = ltcsimraw(rawfile)

    if args.signal:
        print( "Stats:")
        sigs = args.signal.split()
        ans = []
        for i in sigs:
            i = i.lower()
            if i in rf.variables:
                y = rf.variableNumber[i]
                s = rf.getSignal([y])
                sig = np.transpose(np.array(s,np.float))

                #argmin gives the index at min
                median = np.median(sig[1])
                min = np.amin(sig[1])
                max = np.amax(sig[1])
                std = np.std(sig[1])
                charge = np.trapz(sig[1],sig[0])
                ans.append([y,std,min,max,charge,median])
                #print( "%s %e %e %e %e" % (y ,std, min, max, charge))
        print( len(ans))
        a = np.array(ans)
        index = np.argsort(a[:,1])
        index = index[::-1]
        print( "%13s %13s %13s %13s %13s %13s" % ("RMS","Min","Max","Charge","Median","Name"))
        for n,i in enumerate(index):
            print( "% e % e % e % e % e %s" % (a[i][1], a[i][2], a[i][3],
                    a[i][4], a[i][5], rf.variables[int(a[i][0])]))
            if n > 10:
                break
        exit(0)

    if args.sub:
        print( "Substrate Currents")
        ans = []
        for i in rf.variables:
            i = i.lower()
            if i.startswith("i") and i.endswith("sub)"):
                y = rf.variableNumber[i]
                s = rf.getSignal([y])
                sig = np.transpose(np.array(s,np.float))

                #argmin gives the index at min
                min = np.amin(sig[1])
                max = np.amax(sig[1])
                std = np.std(sig[1])
                charge = np.trapz(sig[1],sig[0])
                ans.append([y,std,min,max,charge])
                #print( "%s %e %e %e %e" % (y ,std, min, max, charge))
        a = np.array(ans)
        index = np.argsort(a[:,1])
        index = index[::-1]
        print( "%13s %13s %13s %13s %13s" % ("RMS","Min","Max","Charge","Name"))
        for n,i in enumerate(index):
            print( "% e % e % e % e %s" % (a[i][1], a[i][2], a[i][3], a[i][4], rf.variables[int(a[i][0])]))
            if n > 10:
                break
        exit(0)

    if args.match:
        print( "Node(s) Matching: " + args.match)
        ans = []
        for i in rf.variables:
            if i.startswith("i") and i.endswith(args.match.lower() + ")"):
                y = rf.variableNumber[i]
                s = rf.getSignal([y])
                sig = np.transpose(np.array(s,np.float))

                #argmin gives the index at min
                min = np.amin(sig[1])
                max = np.amax(sig[1])
                std = np.std(sig[1])
                charge = np.trapz(sig[1],sig[0])
                ans.append([y,std,min,max,charge])
                #print( "%s %e %e %e %e" % (y ,std, min, max, charge))
        if(len(ans)):
            a = np.array(ans)
            index = np.argsort(a[:,1])
            index = index[::-1]
            print( "%13s %13s %13s %13s %13s" % ("RMS","Min","Max","Charge","Name"))
            for n,i in enumerate(index):
                print( "% e % e % e % e %s" % (a[i][1], a[i][2], a[i][3], a[i][4], rf.variables[int(a[i][0])]))
                if n > 10:
                    break
        else:
            print( "No Match")
        exit(0)

    elif args.xfer:
        print( "Use the script \"acAnalysis.py\" instesd")
        exit (0)

    elif args.volt or args.current:
        differential = []
        diffExtract = []
        #scan for arguements that have commas
        #if a comma is found the string needs to broken up so that the signals
        #can be plotted differentailly
        removeSigs = []
        for s in args.volt:
            if ',' in s:
                ln = s.split(',')
                #make a list of diff signals to remove from the single ended list
                removeSigs.append(s)
                
                #list of single ended signals to extract
                diffExtract.extend(ln)

                #2D list. Rows are diff signals
                #column 0 is the + signal
                #column 1 is the - signal
                differential.append(ln)

        #remove the diff signals from the single ended list
        for s in removeSigs:
            args.volt.remove(s)

        #extract the single ended and differental data
        (data,labels) = rf.getSignals(args.volt,args.current)
        (diff_data,diff_labels) = rf.getSignals(diffExtract,[])

        #convert extracted single ended signals into diff signals
        #append the diff signals to the single ended data
        for d in differential:
            try:
                indexp = diff_labels.index("v(%s)" % d[0])
                indexn = diff_labels.index("v(%s)" % d[1])
                for i,a in enumerate(diff_data):
                    x = a[indexp]-a[indexn]
                    data[i].append(x)
                labels.append("v(%s,%s)" % (d[0],d[1]))
            except:
                print( "problem extracting signal: v(%s,%s)" % (d[0],d[1]))


        istart = 0
        istop = rf.points-1
        if args.tstart:
            tstart = float(mpUtil.decodeEngineeringNotation(args.tstart))
            #istart = rf.searchTime(tstart)
            #tstart = data[istart][0]
        else:
            tstart = data[0][0]

        if args.tstop:
            tstop = float(mpUtil.decodeEngineeringNotation(args.tstop))
            #istop = rf.searchTime(tstop)
            #tstop = data[istop][0]
        else:
            tstop = data[-1][0]

        (sigs,nsteps) = rf.setGnuplotFormat(data[istart:istop],labels)
        names = labels
        names.pop(0)

        if(args.plot and rf.complex_data):
            ln = rawfile.split(".")
            extension = ln.pop()
            basename = ".".join(ln)
            logfile = basename + '.log'
            from steptable import StepTable 
            table = StepTable()
            table.readLogfile(logfile)
            print( table.steps)

            rf.plotComplex(sigs,nsteps,names,table.steps)
        elif(args.plot):
            from os import linesep as nl

            import subprocess
            gnuplot_bin = ['/usr/bin/env', 'gnuplot','-persist', '-']
            gp = subprocess.Popen(gnuplot_bin,stdin = subprocess.PIPE, \
                stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            
            gp.stdin.write( \
"set terminal qt size 640,480 enhanced font 'Linear Helv Cond Bold,9'\n")

            pstrings = []
            for i,n in enumerate(names):
                #gp.stdin.write("unset key\n")
                #gp.stdin.write("set xlabel 'time'\n")
                #title = "set title '%s'\n" % n
                #gp.stdin.write(title)
                gp.stdin.write("set xrange [%e:%e]\n" % (tstart, tstop))
                pstrings.append("for [corner=1:%d] '-' u 1:%d w l t '%s'" % \
                        (nsteps, 2+i ,n ))

            plotstring = ",".join(pstrings)
            plotstring = "plot %s\n" % (plotstring)
            print( plotstring)
            gp.stdin.write(plotstring)

            for i,n in enumerate(names):
                for l in sigs:
                    line = l + "\n"
                    #line = i 
                    gp.stdin.write(line)
                    gp.stdin.flush()

            print( len(names))
            gp.communicate('e\nquit\n')
            
        elif(args.multiplot):
            from os import linesep as nl

            import subprocess
            gnuplot_bin = ['/usr/bin/env', 'gnuplot','-persist', '-']
            gp = subprocess.Popen(gnuplot_bin,stdin = subprocess.PIPE, \
                stdout = subprocess.PIPE, stderr = subprocess.PIPE)

            height = 480 + 120*(len(names)-1)
            if height > 900:
                height = 900
            print( height)
            gp.stdin.write( \
"set terminal qt size 640,%d enhanced font 'Linear Helv Cond Bold,9'\n" % \
            height)

            gp.stdin.write("set multiplot layout %d,1 \n" % \
                (len(names)))

            for i,n in enumerate(names):
                #gp.stdin.write("set size 1.0,0.5\n")
                gp.stdin.write("unset key\n")
                #gp.stdin.write("set xlabel 'time'\n")
                title = "set title '%s'\n" % n
                gp.stdin.write(title)
                gp.stdin.write("set xrange [%e:%e]\n" % (tstart, tstop))
                gp.stdin.write("plot for [corner=1:%d] '-' u 1:%d w l t '%s\'n" % \
                        (nsteps, 2+i ,n ))

                for l in sigs:
                    line = l + "\n"
                    #line = i 
                    gp.stdin.write(line)
                    gp.stdin.flush()

            print( len(names))
            gp.stdin.write("unset multiplot\n")
            gp.communicate('e\nquit\n')

        elif rf.complex_data == False:
            pass
            #mpUtil.aoaPrint((sigs))
            for i in sigs:
                print( i)

    elif args.copy:
        rf.copyRawFile()

    elif args.preamble:
        print( rf.preamble )
        exit(0)

    elif args.list:
        for v in rf.variables:
            print( v)
        exit(0)

    elif args.bias:
        rf.readLastTimePoint()
        for i,v in enumerate(rf.tp):
            if i == 0:
                print( "*%s=%s" % (rf.variables[i],rf.tp[i]))
                print( ".ic")
                continue
            if(rf.variables[i].startswith("v")):
                print( "+%s=%s" % (rf.variables[i],rf.tp[i]))

    else:
        rf.readTimePoint()
        rf.readLastTimePoint()
        for i,v in enumerate(rf.tp):
            #print( rf.getVal("time"))
            print( "%d %s %s" % (i,rf.variables[i],rf.tp[i]))
