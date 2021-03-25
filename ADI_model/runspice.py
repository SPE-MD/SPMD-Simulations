#! /usr/bin/env python

#Copyright  2021 <Analog Devices>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


#from multiprocessing.dummy import Pool as ThreadPool
#
#def countTo(x):
#    for i in range(x):
#        pass
#    return x
#
## Make the Pool of workers
#pool = ThreadPool(10) 
#
#results = pool.map(countTo, range(0000000,10000000,1000000))
#
#print results
##close the pool and wait for the work to finish 
#pool.close() 
#pool.join() 

import sys
import subprocess
import select
import time
import os
import os.path
from multiprocessing import Process, Pipe, Queue

def runLTspice(cirfile,executable,msgQueue):
    #print cirfile
    while not os.path.isfile(cirfile):
        print "waiting for cir: %s\r" % cirfile
        time.sleep(0.4)
    #subprocess.call(["touch",cirfile])
    msgQueue.put(None)
    executable.append(cirfile)
    try:
        #if "win" in sys.platform and sys.platform is not "darwin":
        if sys.platform == "darwin":
            print "darwin"
            exe = ' '.join(executable)
            print exe
            subprocess.call((exe) ,shell=True)
        elif "win" in sys.platform:
            print "windows"

            subprocess.call(executable, shell=True)
        else:
            subprocess.call(executable)
    except:
        print "Issue Running Spice"
        msgQueue.put("Done")
    msgQueue.put("Done")

def tail(logfile,pipe):

    while not os.path.isfile(logfile):
        print "waiting for log: %s\r" % logfile
        if(pipe.poll()):
                    rcv = pipe.recv()
                    if(rcv == "Done"):
                        return
        time.sleep(0.4)

    f=open(logfile, "r")

    print "following   %s" % logfile
    line = ""

    counter = 0;
    done = False

    filter = set([".step","WARNING","Error","Fail'ed", "Fatal", "Multiply", "Total elapsed time:", "Singular matrix"]) 
    while True:
            read = f.read(1)
            if(read == '\0'):
                pass
            elif(read == '\n'):
                #pipe.send(line)
                #sys.stdout.write("%-80s\n" % line)
                for m in filter:
                    if line.startswith(m):
                        sys.stdout.write("%-80s\n" % line)
                        #print ""
                line = ""
                counter = 0
            elif(len(read) > 0):
                line = line + read[0::2]
                counter = 0
            else:
                if(pipe.poll()):
                    rcv = pipe.recv()
                    if(rcv == "Done"):
                        done = True
                if(done): counter += 1
                else: time.sleep(0.01)
            if(counter >= 1000): break
    f.close

def makeNetlist(ascfile):
    print "*** " + ascfile
    """ ltspice path """
    #exe = os.path.join("C:\\","Program Files","LTC","LTspiceIV","scad3.exe")
    #exe = os.path.join("C:\\","Program Files (x86)","LTC","LTspiceIV","scad3.exe")
    exe = os.path.join("C:\\","Program Files","LTC","LTspiceXVII","XVIIx64.exe")

    #try:
    #    test = os.path.join(os.environ['HOME'],".wine","drive_c", \
    #            "Program Files (x86)","LTC","LTspiceIV","scad3.exe")
    #except:
    #    pass
    #if os.path.isfile(test) :

    """ linux/wine scad call """
    scad = ["wine",exe,'-wine','-netlist']

    """ for windows """
    windows = False
    if sys.platform is "darwin":
        pass
    elif "win" in sys.platform:
        windows = True
        scad = [exe,'-netlist']
   
    """
    TODO: 
    LTSPICE has to be run in whatever path the cir file is sitting or the library links dont work
    """
    ln = ascfile.split(".")
    extension = ln.pop()
    basename = ".".join(ln)
    logfile = basename + '.log'

    #setup subprocess to start ltspice
    spiceMsgQueue = Queue()
    spice = Process(target=runLTspice, args=(ascfile,scad,spiceMsgQueue))

    #os.remove the old log files
    if(not os.path.isfile(ascfile)):
        print "the ascfile %s does not exist" % ascfile
        return []
    
    spice.start()
    spiceDone = False
    while not spiceDone:
        try:
            xdone = spiceMsgQueue.get_nowait()
            if(xdone == "Done"):
                spiceDone = True
                break
        except: 
            pass

    spice.join()
    return 

#expects the name of the cirfile 
#strips off the .cir and uses the basename to monitor .log
def runspice(cirfile,batch=True):

    print "*** " + cirfile
    """ ltspice path """
    exe = os.path.join("C:\\","Program Files","LTC","LTspiceIV","scad3.exe")
    exe = os.path.join("C:\\","Program Files (x86)","LTC","LTspiceIV","scad3.exe")
    exe = os.path.join("C:\\","Program Files","LTC","LTspiceXVII","XVIIx64.exe")
    #test = os.path.join(os.environ['HOME'],".wine","drive_c", \
    #        "Program Files (x86)","LTC","LTspiceIV","scad3.exe")
    #if os.path.isfile(test) :
    #    exe = os.path.join("C:\\","Program Files (x86)","LTC","LTspiceIV","scad3.exe")

    """ linux/wine scad call """
    scad = ["wine",exe,'-wine','-b']

    """ for windows """
    windows = False
    print sys.platform
    if sys.platform == "darwin":
        #exe = os.path.join("C:","Program\ Files","LTC","LTspiceXVII","XVIIx86.exe")

        exe = os.path.join(os.environ['HOME'],".wine","drive_c", \
                "Program Files (x86)","LTC","LTspiceIV","scad3.exe")
        exe = os.path.join(os.environ['HOME'],".wine","drive_c", \
                "Program Files (x86)","LTC","LTspiceXVII","XVIIx86.exe")
        scad = ["wine",exe,'-wine','-b']
        scad = ['wine C:/Program\ Files/LTC/LTspiceXVII/XVIIx86.exe -wine -b']
        print scad
    elif "win" in sys.platform :
        print "Windows"
        windows = True
        scad = [exe,'-b']
        if not batch:
            scad = [exe]
   
    if not os.path.isfile(exe):
        print exe

    """
    TODO: 
    LTSPICE has to be run in whatever path the cir file is sitting or the library links dont work
    """
    ln = cirfile.split(".")
    extension = ln.pop()
    basename = ".".join(ln)
    logfile = basename + '.log'

    #setup subprocess to start ltspice
    spiceMsgQueue = Queue()
    spice = Process(target=runLTspice, args=(cirfile,scad,spiceMsgQueue))

    #os.remove the old log files
    if(not os.path.isfile(cirfile)):
        print "the cirfile %s does not exist" % cirfile
        return []
    if(os.path.isfile(logfile)): os.remove(logfile)

    spice.start()
    
    #setup subprocess to follow the log file
    parent_conn, child_conn = Pipe()
    follow = Process(target=tail, args=(logfile,child_conn))
    follow.start()

    spiceDone = False
    log = []
    while not spiceDone:
        try:
            xdone = spiceMsgQueue.get_nowait()
            if(xdone == "Done"):
                spiceDone = True
                break
        except: 
            pass

        if parent_conn.poll():
            rcv = parent_conn.recv()
            log.append(rcv)
            #print "%s" % rcv
            ##sys.stdout.write("%-80s\r" % rcv)
        time.sleep(0.01)
    
    parent_conn.send("Done")
    while parent_conn.poll():
        rcv = parent_conn.recv()
        #print "%s" % rcv
        log.append(rcv)
        #time.sleep(0.02)

    spice.join()
    follow.join()
    return log

if __name__ == '__main__':
    circuit = sys.argv[1]
    runspice(circuit)
