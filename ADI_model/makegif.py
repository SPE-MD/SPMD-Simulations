#! /usr/bin/env python3

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
import imageio
import subprocess
import shutil

#remove old gif generation files
if os.path.exists("gif"):
    try:
        shutil.rmtree("./gif")
    except:
        print( "Issue removing old files in './gif/'" )
        exit(1)

#recreate the directory to hold the gif files
if not os.path.exists("gif"):
    try:
        os.makedirs("gif")
    except:
        print( "Cannot create 'gif' folder")
        exit(1)

#loop through the sim and build up a library of png images to animate
pngfiles = []

#change the cable length
#for i in range(15,100+1):
#    try:
#        subprocess.run(["python","cmodel.py"\
#            ,"--seed=144704"\
#            ,"--nodes=16"\
#            ,"--length=%d" % i\
#            ,"--separation_min=1"\
#            ,"--drop_max=0.5"\
#            ,"--noplot"\
#            ])

#change the drop length
drop=0.10
for i in range(15,30+1,1):
    cnode = i * 1e-12
    try:
        command = ["python","cmodel.py"\
            ,"--seed=144704"\
            ,"--nodes=32"\
            ,"--length=100"\
            ,"--separation_min=1"\
            ,"--drop_max=%.02f" % drop\
            ,"--cnode=%.02g" % cnode\
            ,"--noplot"\
            ,"--noautoscale"\
            ]

        print(" ".join(command))
        subprocess.run(command)
    except:
        print( "Issue running simulation" )
        exit(1)

    try:
        new_file = os.path.join("gif","frame_%d.png" % i)
        shutil.move("zcable.png", new_file)
    except:
        print( "Issue copying file" )
        exit(1)

    pngfiles.append(new_file)

#setup the gif loop to go forward, then backwards, and loop forever
gif_file = 'zcable.gif'
loop = []
for png in pngfiles:
    loop.append(png)
for png in reversed(pngfiles):
    loop.append(png)

print("Compiling Gif")
images = []
for filename in loop:
    images.append(imageio.imread(filename))
imageio.mimsave(gif_file, images)
print("generated gif: %s" % gif_file)
