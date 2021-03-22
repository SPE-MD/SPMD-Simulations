#! /usr/bin/env python

import re
import sys
from os import listdir
from os.path import dirname
import os.path 
import shutil
import argparse
import time
import random
#from multiprocessing import Process

sys.path.append(dirname(__file__)) #adds this file's director to the path
#import subprocess
#import runspice
#from steptable import StepTable
#from spifile import SpiFile as SpiFile

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
    seed = random.seed()
    length = 50       #meters
    segs_per_meter=10 #finite element lump size
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
    attach_points=[3,455,458,461,464,467,470,473,476,479,481,484,487,490,493,496,499]

    with open("cable.p", 'w') as cable:

        cable.write("*lumped transmission line model with %d segments per meter at %d meters\n"\
        % (segs_per_meter, length))
        cable.write("*and a %f meter long cable\n" % length)
        cable.write(".include tlump.p\n")
        cable.write(".include pd.p\n")
        cable.write(".param clump=%.6g\n" % clump)
        cable.write(".param llump=%.6g\n" % llump)
        cable.write(".param rg=100e6\n")
        cable.write(".param rser=%.6g\n" % r_m)
        for seg in range(0,max_segs):
            cable.write("Xseg%04d p%04d n%04d p%04d n%04d 0 tlump\n" % (seg, seg, seg, seg+1, seg+1)) 
        #cable.write("rstart_term p%04d n%04d %f\n" % (0, 0, z0))
        cable.write("rend_term p%04d n%04d %f\n" % (max_segs, max_segs, z0))


    with open("zcable.ac.cir", 'w') as zcable:
        zcable.write("*ac sim command for cable impedance measurement\n")
        zcable.write(".include cable.p\n")
        zcable.write("iac p%04d n%04d 0 AC 1\n" % (0, 0))
        zcable.write(".ac dec 20 1 10G\n")

    with open("zcable.tran.cir", 'w') as zcable:
        zcable.write("*tranient sim command for cable impedance measurement\n")
        zcable.write(".include cable.p\n")
        zcable.write("**************************\n")
        zcable.write("***** PD ATTACHMENTS *****\n")
        zcable.write("**************************\n")
        npd=0
        ndrop=6
        for pd in attach_points:
            npd+=1
            for i in range(0,ndrop):
                if i==0:
                    zcable.write("Xseg%04d_%04d p%04d n%04d p%04d_%04d n%04d_%04d 0 tlump\n" %\
                                    (pd, i, pd, pd, pd, i+1, pd, i+1)) 
                else:
                    zcable.write("Xseg%04d_%04d p%04d_%04d n%04d_%04d p%04d_%04d n%04d_%04d 0 tlump\n" %\
                                    (pd, i, pd, i, pd, i, pd, i+1, pd, i+1)) 
            zcable.write("rpdp%04d p%04d_%04d pdp_%04d 0.010\n" % (pd, pd, i+1, npd))
            zcable.write("rpdn%04d n%04d_%04d pdn_%04d 0.010\n" % (pd, pd, i+1, npd))
            zcable.write("xpd%04d pdp_%04d pdn_%04d 0 pd\n" % (npd, npd, npd))

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
