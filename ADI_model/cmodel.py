#! /usr/bin/env python

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
#from multiprocessing import Process

sys.path.append(dirname(__file__)) #adds this file's director to the path
#import subprocess
import runspice
from ltcsimraw import ltcsimraw as ltcsimraw
#from steptable import StepTable
from spifile import SpiFile as SpiFile

def distribute_pds(start_attach_point, end_attach_point, n_pds, separation_min):
    #find where the 'center' pd should be
    #it has to be within ((n_pds/2 + 1)) * separation_min from the front and back
    #of the cable
    attach_points = []

    
    #choose a 'half_point' which is a random location on the mixing segment 
    #where half of the PDs are to the right and half of the PDs are to the left
    #save room for the N/2 pds at the start and end of the mixing segment if
    #there is more than 1 pd

    #print "\nNumber of PDs = %d" % n_pds
    if(n_pds % 2):
        #print "odd number of PDs"
        start = int((start_attach_point + ((n_pds+1)/2)*separation_min))
        end   = int((end_attach_point   - ((n_pds+1)/2)*separation_min))
        #when down to the last placement, min and max might switch places
        #the random number generator does not like this, so get them sorted out
        start = min(start,end)
        end   = max(start,end)
        #print "Start  %d" % start
        #print "End    %d" % end
        #print "N_pds  %d" % n_pds
        if(start == end):
            half_point = start
        else:
            half_point   = random.randrange(start, end, 1)
        #print "Attach %d" % half_point
        n_pds -= 1
        if(n_pds > 1):
            attach_points.extend(distribute_pds(start_attach_point, half_point, n_pds/2, separation_min))

        attach_points.extend([half_point])

        if(n_pds > 1):
            attach_points.extend(distribute_pds(half_point, end_attach_point, n_pds/2, separation_min))

    else: #must be 2 or more pds to get here
        start = int((start_attach_point + ((n_pds)/2)*separation_min))
        end   = int((end_attach_point   - ((n_pds)/2)*separation_min))
        #print "Start  %d" % start
        #print "End    %d" % end
        #print "N_pds  %d" % n_pds
        half_point   = random.randrange(start, end, 1)
        #print "Half   %d" % half_point

        attach_points.extend(distribute_pds(start_attach_point, half_point, n_pds/2, separation_min))
        attach_points.extend(distribute_pds(half_point,   end_attach_point, n_pds/2, separation_min))


    #print attach_points
    return attach_points

if __name__ == '__main__':
    csvFile = os.path.join("zcable.csv")
    with open(csvFile, 'w') as csv:
        #delete the csvFile.  It gets filled up in append mode later...
        pass
    seed = random.seed()
    length = 50       #meters
    segs_per_meter=20 #finite element lump size
    tpd=3.335e-9      #speed of light on this cable
    z0 = 100          #cable impedance
    l_m = tpd * z0               #inductance per meter
    c_m = tpd / z0               #capacitance per meter
    r_m = 0.188                  #dc resistance per meter
    llump = l_m / segs_per_meter
    clump = c_m / segs_per_meter
    rlump = r_m / segs_per_meter 
    max_segs = int(segs_per_meter * length)
    n_pds = 10
    separation_min = 0.1 #meters
    drop_max = 0.5 #meters

    #attach points are the node numbers 
    attach_points=distribute_pds(0,length*segs_per_meter, n_pds, 1)
    #attach_points=[3,455,458,461,464,467,470,473,476,479,482,485,488,491,494,497,500]
    attach_points=[12,832,844,856,868,880,892,904,916,928,940,952,964,976,988,1000]
    #attach_points=[1000]
    
    for a in range(0,len(attach_points)+1):
    #if(True):
        #a=len(attach_points)
        attach_points_x = attach_points[0:a]
        with open("cable.p", 'w') as cable:

            cable.write("*lumped transmission line model with %d segments per meter at %d meters\n"\
            % (segs_per_meter, length))
            cable.write("*and a %f meter long cable\n" % length)
            cable.write(".include tlump3.p\n")
            cable.write(".include pd.p\n")
            cable.write(".param clump=%.6g\n" % clump)
            cable.write(".param llump=%.6g\n" % llump)
            cable.write(".param rg=100e6\n")
            cable.write(".param rser=%.6g\n" % r_m)

            for seg in range(0,max_segs):
                cable.write("Xseg%04d p%04d n%04d p%04d n%04d 0 tlump\n" % (seg, seg, seg, seg+1, seg+1)) 
            cable.write("rend_term p%04d n%04d %f\n" % (max_segs, max_segs, z0))
            cable.write("**************************\n")
            cable.write("***** PD ATTACHMENTS *****\n")
            cable.write("**************************\n")
            npd=0
            ndrop=6
            for pd in attach_points_x:
                npd+=1
                cable.write("*PD %02d - attach at %.3f meters with %.3f meter drop\n" % \
                        (npd, pd/segs_per_meter, ndrop / segs_per_meter))

                print ("*PD %02d - attach at %.3f meters with %.3f meter drop" % \
                        (npd, pd/float(segs_per_meter), ndrop / float(segs_per_meter)))

                for i in range(0,ndrop):
                    if i==0:
                        cable.write("Xseg%04d_%04d p%04d n%04d p%04d_%04d n%04d_%04d 0 tlump\n" %\
                                        (pd, i, pd, pd, pd, i+1, pd, i+1)) 
                    else:
                        cable.write("Xseg%04d_%04d p%04d_%04d n%04d_%04d p%04d_%04d n%04d_%04d 0 tlump\n" %\
                                        (pd, i, pd, i, pd, i, pd, i+1, pd, i+1)) 
                cable.write("rpdp%04d p%04d_%04d pdp_%04d 0.010\n" % (pd, pd, i+1, npd))
                cable.write("rpdn%04d n%04d_%04d pdn_%04d 0.010\n" % (pd, pd, i+1, npd))
                cable.write("xpd%04d pdp_%04d pdn_%04d 0 pd\n" % (npd, npd, npd))

        with open("zcable.ac.cir", 'w') as zcable:
            zcable.write("*ac sim command for cable impedance measurement\n")
            zcable.write(".include cable.p\n")

            #differential signal input
            zcable.write("vac p0000_p n0000_n 0 AC 1\n")

            #current flows out of the positive terminal of rp or the s-parameters wont calculate correctly
            zcable.write("rp p%04d p%04d_p 50\n" % (0, 0))
            zcable.write("rn n%04d_n n%04d 50\n" % (0, 0))

            #the next 4 resistors help make the common mode voltage for the differential v-source
            zcable.write("rrpp p%04d_p refp 50\n" % 0)
            zcable.write("rrpn refp 0 50\n")
            zcable.write("rrnp n%04d_n refn 50\n" % 0)
            zcable.write("rrnn refn 0 50\n")

            #simulation command
            zcable.write(".ac lin 500 1meg 100meg\n")

            #this .net expression isn't helping anymore, the s-parameters are being calculated from phasors
            #in the .ac output
            zcable.write(".net I(rend_term) vac\n")

            #select nodes to save to speed up the sim and reduce file size
            zcable.write(".save \n")
            zcable.write("+ v(refp) v(refn)\n")
            zcable.write("+ I(vac) I(rp) I(rend_term)\n")
            zcable.write("+ v(p0000) v(n0000)\n")
            zcable.write("+ S11(vac) S21(vac)\n")
            zcable.write("+ v(p%04d) v(n%04d)\n" % (max_segs, max_segs))

        with open("zcable.tran.cir", 'w') as zcable:
            zcable.write("*tranient sim command for cable impedance measurement\n")
            zcable.write(".include cable.p\n")

            zcable.write("vap ap 0 0\n")
            zcable.write("+pwl 0 0\n")
            zcable.write("++50n  0.0\n")
           
            #start one
            zcable.write("++10n  1.0\n")
            zcable.write("++20n  1.0\n")
            zcable.write("++20n -1.0\n")
            zcable.write("++20n -1.0\n")

            #zero
            zcable.write("++20n -1.0\n")
            zcable.write("++20n -1.0\n")
            zcable.write("++20n  1.0\n")
            zcable.write("++20n  1.0\n")

            #zero
            zcable.write("++20n -1.0\n")
            zcable.write("++20n -1.0\n")
            zcable.write("++20n  1.0\n")
            zcable.write("++20n  1.0\n")

            #one
            zcable.write("++20n  1.0\n")
            zcable.write("++20n  1.0\n")
            zcable.write("++20n -1.0\n")
            zcable.write("++20n -1.0\n")

            #zero
            zcable.write("++20n -1.0\n")
            zcable.write("++20n -1.0\n")
            zcable.write("++20n  1.0\n")
            zcable.write("++20n  1.0\n")

            #one
            zcable.write("++20n  1.0\n")
            zcable.write("++20n  1.0\n")
            zcable.write("++20n -1.0\n")
            zcable.write("++20n -1.0\n")

            #one
            zcable.write("++20n  1.0\n")
            zcable.write("++20n  1.0\n")
            zcable.write("++20n -1.0\n")
            zcable.write("++20n -1.0\n")

            #zero
            zcable.write("++20n -1.0\n")
            zcable.write("++20n -1.0\n")
            zcable.write("++20n  1.0\n")
            zcable.write("++20n  1.0\n")

            #end
            zcable.write("++10n  0.0\n")



            
            zcable.write("van 0 an 0\n")
            zcable.write("+pwl 0 0\n")
            zcable.write("++50n  0.0\n")
           
            #start one
            zcable.write("++10n  1.0\n")
            zcable.write("++20n  1.0\n")
            zcable.write("++20n -1.0\n")
            zcable.write("++20n -1.0\n")

            #zero
            zcable.write("++20n -1.0\n")
            zcable.write("++20n -1.0\n")
            zcable.write("++20n  1.0\n")
            zcable.write("++20n  1.0\n")

            #zero
            zcable.write("++20n -1.0\n")
            zcable.write("++20n -1.0\n")
            zcable.write("++20n  1.0\n")
            zcable.write("++20n  1.0\n")

            #one
            zcable.write("++20n  1.0\n")
            zcable.write("++20n  1.0\n")
            zcable.write("++20n -1.0\n")
            zcable.write("++20n -1.0\n")

            #zero
            zcable.write("++20n -1.0\n")
            zcable.write("++20n -1.0\n")
            zcable.write("++20n  1.0\n")
            zcable.write("++20n  1.0\n")

            #one
            zcable.write("++20n  1.0\n")
            zcable.write("++20n  1.0\n")
            zcable.write("++20n -1.0\n")
            zcable.write("++20n -1.0\n")

            #one
            zcable.write("++20n  1.0\n")
            zcable.write("++20n  1.0\n")
            zcable.write("++20n -1.0\n")
            zcable.write("++20n -1.0\n")

            #zero
            zcable.write("++20n -1.0\n")
            zcable.write("++20n -1.0\n")
            zcable.write("++20n  1.0\n")
            zcable.write("++20n  1.0\n")

            #end
            zcable.write("++10n  0.0\n")

            zcable.write("rap ap p0000 50\n")

            zcable.write("ran an n0000 50\n")

            zcable.write("rrefp ap refp 50\n")
            zcable.write("rrefn an refn 50\n")
            zcable.write("rref  refp refn 100\n")
            zcable.write(".save V(*)\n")
            zcable.write(".tran 2000n\n")

        cirfile = "zcable.ac.cir"
        rawfile = "zcable.ac.raw"

        #condense the sim files into a single *.spi file
        #crete a md5 of the spi file then make a unique directory to store this sim
        #If batches of sims are run more than once, just extract the data without 
        #running the sim again
        spi = SpiFile(cirfile)
        spi.readCircuit()
        spi.followInclude = True
        spi.digestSpiceFile()
        design_md5 = spi.md5(False, True, True)
        spiSave  = os.path.join("data",design_md5,design_md5+".spi")
        logSave  = os.path.join("data",design_md5,design_md5+".log")
        rawSave  = os.path.join("data",design_md5,design_md5+".raw")
        outputdb = os.path.join("data",design_md5)
        print design_md5
        if not os.path.exists("data"):
            print "Data Folder does not exist"
            print "Creating...." 
            try:
                os.makedirs("data")
            except:
                print "Cannot create data folder"
                exit(1)

        if not os.path.exists(outputdb):
            print "Regression Folder %s does not exist" % design_md5
            print "Creating...." 
            try:
                os.makedirs(outputdb)
                spi.outputToFile(spiSave)
            except:
                print "Cannot create regression folder"
                exit(1)

        #if there is already raw and log data in the md5 directory then assume the sim has 
        #already been run, otherwise run the sim
        try:
            open(spiSave,"r")
            print spiSave
            open(logSave,"r")
            print logSave
            open(rawSave,"r")
            print rawSave
            print "Pulling Sim From database"

        except:
            print "Running Simulation"
            runspice.runspice(spiSave)

        #determine the node names for the end of the cable
        endp = "p%04d" % ( max_segs)
        endn = "n%04d" % ( max_segs)

        #get the data out of the raw file
        rf=ltcsimraw(rawSave)
        (data, labels) = rf.getSignals(["p0000","n0000", endp, endn],["rp", "rend_term"],["S11(vac)", "s21(vac)"])

        #print the s-parameters in a .csv file
        with open(csvFile, 'a') as zcable:
            zcable.write("#freq, s11_mag, s21_mag, s11_mp_mag, s21_mp_mag\n")
            for x in data:
                #print x[1] 
                #print x[2] 
                s11  = rf.decodeComplex(x[7])
                s21 =  rf.decodeComplex(x[8])

                vend   = x[3]-x[4]
                iend   = x[6]
                vin    = x[1]-x[2]
                iin    = x[5]
                zin    = vin/iin
                zin    = 100
                zend   = 100
                zin_x  = np.conjugate(zin)
                zend_x = np.conjugate(zend)
                a1 = (vin - (iin*zin_x))
                b1 = (vin + (iin*zin))
                a2 = (vend - (iend*zend_x))
                b2 = (vend + (iend*zend))
                s11_mp = rf.decodeComplex(b1 / a1)
                s21_mp = rf.decodeComplex(b2 / a1)
                zcable.write("%.12g, %.12g, %.12g, %.12g, %.12g\n" % (
                        x[0], s11[0], s21[0], s11_mp[0], s21_mp[0]
                        ))
            zcable.write("\n\n")
        print labels
