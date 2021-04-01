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
#from multiprocessing import Process

sys.path.append(dirname(__file__)) #adds this file's director to the path
#import subprocess
import runspice
from ltcsimraw import ltcsimraw as ltcsimraw
#from steptable import StepTable
from spifile import SpiFile as SpiFile

def distribute_pds_even(start_attach_point, end_attach_point, n_pds, separation_min, tab=""):
    #there will be 1 separation between 2 pds, so subtract 1 from n_pds when calculating delta
    attach_points = [] 
    if n_pds==0:
        return attach_points
    if n_pds==1:
        return [int((end_attach_point + start_attach_point)/2)]
    delta = (end_attach_point - start_attach_point) / (n_pds - 1)
    for i in range(0,n_pds):
        attach_points.append(int(start_attach_point + (i * delta)))
    return attach_points

def distribute_pds_random(start_attach_point, end_attach_point, n_pds, separation_min, tab=""):
    #find where the 'center' pd should be
    #it has to be within ((n_pds/2 + 1)) * separation_min from the front and back
    #of the cable
    attach_points = []
    if n_pds <=0:
        return []

    
    #choose a 'half_point' which is a random location on the mixing segment 
    #where half of the PDs are to the right and half of the PDs are to the left
    #save room for the N/2 pds at the start and end of the mixing segment if
    #there is more than 1 pd

    print( "\n" )
    if(n_pds % 2):
        #print( "odd number of PDs")
        start_x = int((start_attach_point + ((n_pds+1)/2)*separation_min))
        end_x   = int((end_attach_point   - ((n_pds+1)/2)*separation_min))

        #when down to the last placement, min and max might switch places
        #the random number generator does not like this, so get them sorted out
        start = min(start_x,end_x)
        end   = max(start_x,end_x)

        #print( tab+"Satt   %d" % start_attach_point)
        #print( tab+"Eatt   %d" % end_attach_point)
        #print( tab+"Start  %d" % start)
        #print( tab+"End    %d" % end)
        #print( tab+"N_pds  %d" % n_pds)
        if(n_pds == 1):
            half_point   = random.randrange(start_attach_point, end_attach_point, 1)
        elif(start == end):
            half_point = start
        else:
            half_point   = random.randrange(start, end, 1)

        #print( tab+"Attach %d" % half_point)
        n_pds -= 1
        if(n_pds > 1):
            attach_points.extend(distribute_pds_random(start_attach_point, half_point-separation_min, n_pds/2, separation_min, tab+"\t"))

        attach_points.extend([half_point])

        if(n_pds > 1):
            attach_points.extend(distribute_pds_random(half_point+separation_min, end_attach_point, n_pds/2, separation_min, tab+"\t"))

    else: #must be 2 or more pds to get here
        start = int((start_attach_point + ((n_pds)/2)*separation_min))
        end   = int((end_attach_point   - ((n_pds)/2)*separation_min))

        #print( tab+"Satt   %d" % start_attach_point)
        #print( tab+"Eatt   %d" % end_attach_point)
        #print( tab+"Start  %d" % start)
        #print( tab+"End    %d" % end)
        #print( tab+"N_pds  %d" % n_pds)
        half_point   = random.randrange(start, end, 1)
        #print( tab+"Half   %d" % half_point)

        attach_points.extend(distribute_pds_random(start_attach_point, half_point, n_pds/2, separation_min, tab+"\t"))
        attach_points.extend(distribute_pds_random(half_point,   end_attach_point, n_pds/2, separation_min, tab+"\t"))


    #print( attach_points)
    return attach_points

def end_attach(end_attach_point, n_pds, separation_min):
    attach_points = []
    for i in range(1,n_pds+1):
        attach_points.append(int(end_attach_point - ((n_pds-i) * separation_min)))
    return attach_points

def start_attach(start_attach_point, n_pds, separation_min):
    attach_points = []
    for i in range(0,n_pds):
        attach_points.append(i * separation_min)
    return attach_points

def return_loss_limit(freq):
    rl=[]
    for x in freq:
        rl.append(_rl(x))
    return rl

def _rl(x):
    if(x < 0.3e6):
        return np.nan 
    elif(x < 10e6):
        return -14 
    elif(x < 40e6):
        return -1*(14 - 10 * math.log10(x / 10e6))
    else:
        return np.nan

def insertion_loss_limit(freq):
    il=[]
    for x in freq:
        il.append(_il(x))
    return il


def _il(x):

    if(x < 0.3e6):
        return np.nan 
    elif(x < 10e6):
        return -1*(1.0 + (1.6 * (x -  1e6)  / 9e6))
    elif(x < 33e6):
        return -1*(2.6 + (2.3 * (x - 10e6) / 23e6))
    elif(x < 40e6):
        return -1*(4.9 + (2.3 * (x - 33e6) / 33e6))
    else:
        return np.nan


if __name__ == '__main__':
    csvFile = os.path.join("zcable.csv")
    with open(csvFile, 'w') as csv:
        #delete the csvFile.  It gets filled up in append mode later...
        pass

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
            help='Minimum separation between nodes in meters.  This number will\
            be rounded to an integer number of segments per meter',\
            )

    parser.add_argument('--separation_min', type=float, \
            help='Minimum separation between nodes in meters.  This number will\
            be rounded to an integer number of segments per meter',\
            default=1.0\
            )

    parser.add_argument('--seed', type=int, \
            help='Seed value for random number generator',\
            default=-1
            )

    parser.add_argument('--tx_node', type=int, \
            help='Set the transmitter node, default is tx at the start of the cable.\
            (not implemented yet)',
            default=0
            )

    parser.add_argument('--noplot', action='store_true', help='set this flag to\
            prevent plotting')
    
    args = parser.parse_args()

    
    seed = args.seed
    if seed == -1:
        tim = datetime.datetime.now()
        seed = tim.hour*10000+tim.minute*100+tim.second
        random.seed(seed)
    else:
        random.seed(seed)
    print("#Random Seed = %s" % seed)

    length = args.length       #meters
    segs_per_meter=args.segments_per_meter #finite element lump size
    tpd=3.335e-9      #speed of light on this cable
    z0 = 100          #cable impedance
    l_m = tpd * z0               #inductance per meter
    c_m = tpd / z0               #capacitance per meter
    r_m = 0.188                  #dc resistance per meter
    llump = l_m / segs_per_meter
    clump = c_m / segs_per_meter
    rlump = r_m / segs_per_meter 
    max_segs = int(segs_per_meter * length)
    n_pds = args.nodes
    separation_min = args.separation_min
    drop_max = args.drop_max
    ndrop = int(drop_max * segs_per_meter)
    nsep = int(separation_min * segs_per_meter)
    #print(ndrop)
    #print(nsep)

    #containers to hold output data for plotting
    fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize=(9, 9))  # Create a figure and an axes.
    frequency = []
    s11_plot  = []
    s21_plot  = []
    plot_attach = []
    plot_drop = []

    #attach points are the node numbers 
    unattached = n_pds
    attach_start = 0
    attach_end = length*segs_per_meter
    end = []
    start = []
    if(args.end_attach):
        if(args.end_attach <= unattached and args.end_attach > 0):
            nend = args.end_attach
            end = end_attach(attach_end, nend , nsep)
            unattached -= nend
            attach_end = end[0]-nsep

    if(args.start_attach):
        if(args.start_attach <= unattached and args.start_attach > 0):
            nstart = args.start_attach
            start = start_attach(attach_start, nstart, nsep)
            unattached -= nstart
            attach_start = start[-1]+nsep

    mid = []
    if(args.random_attach):
        mid=distribute_pds_random(attach_start,attach_end, unattached, nsep)
    else:
        mid=distribute_pds_even(attach_start, attach_end, unattached, nsep)

    attach_points = start + mid + end

    #exit(1)

    #attach_points=[3,455,458,461,464,467,470,473,476,479,482,485,488,491,494,497,500]
    #attach_points=[12,832,844,856,868,880,892,904,916,928,940,952,964,976,988,1000]
    #attach_points=[1000]
    
    #for a in range(0,len(attach_points)+1):
    #for a in range(0,2):
        #attach_points_x = attach_points[0:a]
    if(True):
        attach_points_x = attach_points
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
            for pd in attach_points_x:
                npd+=1

                #randomize drop lengths
                if args.random_drop:
                    ndrop_x = random.randint(0, ndrop)
                else:
                    ndrop_x = ndrop

                #print attachment information
                att = "*PD %02d - attach at %.3f meters with %.3f meter drop" % \
                        (npd, pd/float(segs_per_meter), ndrop_x / float(segs_per_meter))
                cable.write("%s\n" % att)
                print(att)

                #keep track of attachment and drop for plotting later
                plot_attach.append(pd/float(segs_per_meter))
                if(npd % 2 == 0):
                    plot_drop.append(-1 * ndrop_x / float(segs_per_meter))
                else:
                    plot_drop.append(ndrop_x / float(segs_per_meter))

                i=-1 #need to define i=-1 here incase ndrop_x=0
                for i in range(0,ndrop_x):
                    if i==0:
                        cable.write("Xseg%04d_%04d p%04d n%04d p%04d_%04d n%04d_%04d 0 tlump\n" %\
                                        (pd, i, pd, pd, pd, i+1, pd, i+1)) 
                    else:
                        cable.write("Xseg%04d_%04d p%04d_%04d n%04d_%04d p%04d_%04d n%04d_%04d 0 tlump\n" %\
                                        (pd, i, pd, i, pd, i, pd, i+1, pd, i+1)) 
                if(ndrop_x == 0):
                    cable.write("rpdp%04d p%04d pdp_%04d 0.010\n" % (pd, pd, npd))
                    cable.write("rpdn%04d n%04d pdn_%04d 0.010\n" % (pd, pd, npd))
                else:
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
            zcable.write(".ac lin 200 1meg 40meg\n")

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
        #print( design_md5)
        if not os.path.exists("data"):
            print( "Data Folder does not exist")
            print( "Creating...." )
            try:
                os.makedirs("data")
            except:
                print( "Cannot create data folder")
                exit(1)

        if not os.path.exists(outputdb):
            print( "Regression Folder %s does not exist" % design_md5)
            print( "Creating...." )
            try:
                os.makedirs(outputdb)
                spi.outputToFile(spiSave)
            except:
                print( "Cannot create regression folder")
                exit(1)

        #if there is already raw and log data in the md5 directory then assume the sim has 
        #already been run, otherwise run the sim
        try:
            open(spiSave,"r")
            #print( spiSave)
            open(logSave,"r")
            #print( logSave)
            open(rawSave,"r")
            #print( rawSave)
            print( "Pulling Sim From database")

        except:
            print( "Running Simulation")
            runspice.runspice(spiSave)

        #determine the node names for the end of the cable
        endp = "p%04d" % ( max_segs)
        endn = "n%04d" % ( max_segs)

        #get the data out of the raw file
        rf=ltcsimraw(rawSave)
        (data, labels) = rf.getSignals(["p0000","n0000", endp, endn],["rp", "rend_term"],["S11(vac)", "s21(vac)"])


        #print( the s-parameters in a .csv file)

        with open(csvFile, 'a') as zcable:
            zcable.write("#freq, s11_mag, s21_mag, s11_mp_mag, s21_mp_mag\n")
            f = []
            s1 = []
            s2 = []
            for x in data:
                #print( x[1] )
                #print( x[2] )
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
                f.append(x[0])
                s1.append(s11_mp[0])
                s2.append(s21_mp[0])
            zcable.write("\n\n")
        frequency.append(f)
        s11_plot.append(s1)
        s21_plot.append(s2)
        #print(labels)

    if not args.noplot:
        rl_limit = return_loss_limit(frequency[0])
        il_limit = insertion_loss_limit(frequency[0])
        for i,p in enumerate(frequency):
            ax1.plot(frequency[i], s11_plot[i], label="test")  # Plot more data on the axes...
            ax2.plot(frequency[i], s21_plot[i], label="test")  # Plot more data on the axes...
            #ax1.plot(frequency[i], s11_plot[i])  # Plot more data on the axes...
            #ax2.plot(frequency[i], s21_plot[i])  # Plot more data on the axes...

        ax1.plot(frequency[0], rl_limit, label="clause 147 limit")  # Plot more data on the axes...
        ax2.plot(frequency[0], il_limit, label="clause 147 limit")  # Plot more data on the axes...
        ax1.set_ylabel('RL s11 (dB)')  # Add an x-label to the axes.
        ax1.set_xlim([0,40e6])
        #ax1.set_ylim([-50,0])

        ax2.set_ylabel('IL s21 (dB)')  # Add an x-label to the axes.
        ax2.set_xlabel('Frequency')  # Add a y-label to the axes.
        ax2.set_xlim([0,40e6])
        #ax2.set_ylim([-40,0])
        ax1.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=2)  # Add a legend.

        ax3.set_xlim([-1,int(args.length)+1])
        ax3.set_ylim([-1,1])
        ax3.set_xlabel('Attach (m)')  # Add a x-label to the axes.
        ax3.set_ylabel('Drop (m)')  # Add a x-label to the axes.

        #mixing segment line
        ax3.plot([0,args.length],[0,0], color="k")
        ax3.plot(plot_attach, np.zeros_like(plot_attach), "-o", color="k", markerfacecolor="w")

        #drop lines
        ax3.vlines(plot_attach, 0, plot_drop, color="tab:red")

        #text annotation
        #ax3.annotate(
        #     'N1'
        #     , xy=(10, 0)
        #     , xytext=(10, -0.5)
        #     , xycoords='data'
        #     , va='top'
        #     ) 

        plt.show()
        #print("#Seed: %d" % seed)
        print("#Close plot window to continue")
