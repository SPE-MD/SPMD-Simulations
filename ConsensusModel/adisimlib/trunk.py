#! /usr/bin/env python3

#Copyright  2021 <Michael Paul>
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

from cable import Cable as Cable
from termination import Termination as Termination

class Segment(object):
    def __init__(self, length, pad_start, pad_end):
        self.length=length
        self.postition=0
        self.pad_start=pad_start
        self.pad_end=pad_end
        self.left=None
        self.right=None

    def split(self):
        if(self.left == None):
            if self.length > (self.pad_start + self.pad_end):
                div = random.uniform(self.pad_start, self.length-self.pad_end)
                div = round(div,4)
                self.left=Segment(div,self.pad_start,self.pad_end)
                self.right=Segment(self.length - div,self.pad_start,self.pad_end)
                return True
            else:
                return False
        else:
            self.choice1 = self.left
            self.choice2 = self.right
            if(random.randint(0,1) == 0):
                self.choice1 = self.right
                self.choice2 = self.left
            if(self.choice1.split() == False):
                return self.choice2.split()
            return True

    def build(self):
        if(self.left == None):
            return [self.length]
        lst = []
        lst += self.left.build()
        lst += self.right.build()
        return lst

    def build_positions(self):
        if(self.left == None):
            return [self.position]
        lst = []
        lst += self.left.build_positions()
        lst += self.right.build_positions()
        return lst

    def sum_length(self):
        if(self.left == None):
            return self.length
        length = self.left.sum_length()
        length += self.right.sum_length()
        return length

    def fix_left(self,adjust):
        if(self.left == None):
            self.length += adjust
        else:
            self.left.fix_left(adjust)

    def fix_right(self,adjust):
        if(self.right == None):
            self.length += adjust
        else:
            self.right.fix_right(adjust)

    def calc_position(self,start_offset):
        if(self.left == None):
            self.position = self.length+start_offset
            return self.position
        offset = self.left.calc_position(start_offset)
        offset = self.right.calc_position(offset)
        return offset

class Trunk(object):
    """Object representing a section of cable

    name            name of the trunk segment.  This will be the name of the instance and the subcircuit
    length          length of the trunk segment
    gage            cable gage, does nothing right now
    max_seg_length  max length for a finite element segment, 0.05m is a good choice here
    separation_min  minimum separation between nodes attached to the trunk
    start_pad       minimum distance between the start of the cable and the 1st node
    end_pad         minimum distance between the end of the cable and the last node
    start_attach    number of nodes to connect at the start of the trunk with separation_min spacing
    end_attach      number of nodes to connect at the end of the trunk with separation_min spacing
    random_attach   if true, nodes not forced to beginning or end of the trunk will be spaced randomly
    """

    def __init__(self, name="trunk" ,length=10, nodes=16, gage=18, max_seg_length=0.05, separation_min=1, random_seed=-1, start_pad=0, end_pad=0\
            , start_attach=0, end_attach=0, random_attach=True, attach_error=0):
        self.name = name
        self.length = length
        self.gage = gage
        self.max_seg_length = max_seg_length
        self.separation_min = separation_min
        self.start_pad = start_pad
        self.end_pad = end_pad
        self.attach_error = attach_error
        self.segs = []

        unattached = nodes
        attach_start = start_pad
        attach_end = length-end_pad
        end = []
        start = []
        if(end_attach <= unattached and end_attach > 0):
            nend = end_attach
            end = self.end_attach(attach_end, nend , separation_min)
            unattached -= nend
            attach_end = end[0]-separation_min

        if(start_attach <= unattached and start_attach > 0):
            nstart = start_attach
            start = self.start_attach(attach_start, nstart, separation_min)
            unattached -= nstart
            #print(attach_start)
            attach_start = start[-1]+separation_min

        mid = []
        if(random_attach):
            #print(attach_start)
            #print(attach_end)
            mid=self.distribute_pds_random(attach_start,attach_end, unattached,
                    separation_min)
        else:
            mid=self.distribute_pds_even(attach_start, attach_end, unattached,
                    separation_min)

        self.attach_points = start + mid + end

    def distribute_pds_random(self, attach_start, attach_end, nodes, separation_min):
        #remove start and end pads from the total length before 
        available_length = (attach_end - attach_start) + (2*self.separation_min)
        #print(available_length)
        self.segments = Segment(available_length,self.separation_min,self.separation_min)
        for i in range(0,nodes):
            if(not self.segments.split()):
                print("Cannot fit anymore segments on this trunk")
                return

        #adjust the start and end segments to put in the start pads and remove the extra separation minimums 
        self.segments.fix_left( (-1*self.separation_min))
        self.segments.fix_right((-1*self.separation_min))

        #segments are in units of length.  Need to convert to units of absolute position
        #print(self.segments.build())
        self.segments.calc_position(attach_start)

        #since segments lengths were converted to positions, the last entry is not a real position
        return self.segments.build_positions()[:-1]

    def distribute_pds_even(self, start_attach_point, end_attach_point, n_pds, separation_min, tab=""):
        #there will be 1 separation between 2 pds, so subtract 1 from n_pds when calculating delta
        attach_points = [] 
        if n_pds==0:
            return attach_points
        if n_pds==1:
            return [(end_attach_point + start_attach_point)/2]
        delta = (end_attach_point - start_attach_point) / (n_pds - 1)
        for i in range(0,n_pds):
            point = start_attach_point + (i * delta) + random.gauss(0, self.attach_error)
            point = min(point,self.length)
            point = max(point,0)
            attach_points.append(point)
        return attach_points

    def end_attach(self, end_attach_point, n_pds, separation_min):
        attach_points = []
        for i in range(1,n_pds+1):
            attach_points.append(end_attach_point - ((n_pds-i) * separation_min))
        return attach_points

    def start_attach(self, start_attach_point, n_pds, separation_min):
        attach_points = []
        for i in range(0,n_pds):
            attach_points.append(start_attach_point + (i * separation_min))
        return attach_points

    def get_cable_segments(self):
        trunk_segments=[]
        #is there space between the start termination and the 1st node?
        if(self.attach_points[0] > 0):
            #make segment 0
            t=Cable(name="trunk0",length=self.attach_points[0],port1="t0a",port2="t0b")
            trunk_segments.append(t)

        for l in range(1,len(self.attach_points)):
            length = self.attach_points[l] - self.attach_points[l-1]
            if length < self.separation_min:
                print("violation of min separation on segment %d" % l)
                print("%.5f - %.5f" % (self.attach_points[l], self.attach_points[l-1]))
                exit(1)
            port1="t%da" % l
            port2="t%db" % l
            t=Cable(name="trunk%d" % l,length=length,port1=port1 ,port2=port2)
            trunk_segments.append(t)

        #is there space between the end termination and the last node?
        if(self.attach_points[-1] < self.length):
            #make segment nsegs+1
            name="trunk%d" % (l+1)
            length = (self.length - self.attach_points[-1])
            port1="t%da" % (l+1)
            port2="t%db" % (l+1)
            t=Cable(name=name,length=length,port1=port1 ,port2=port2)
            trunk_segments.append(t)
        return trunk_segments

    def subcircuit(self):
        """Generate the subcircuit definition for this cable segment"""
        netlist = [self.__str__()]

        netlist.append(".subckt %s %04dp %04dn endp endn rtn" % 
                    (self.name, 0, 0))

        netlist.append("rendp endp %04dp 1u" % self.total_segs)
        netlist.append("rendn %04dn endn 1u" % self.total_segs)

        #generate the body of the cable
        for i in range(0,self.whole):
            netlist.append(self.__make_segment__(i, self.max_seg_length))

        #handle fractional segments
        if(self.part > 0):
            netlist.append(self.__make_segment__(self.whole, self.part*self.max_seg_length))


        netlist.append(".ends %s" % self.name)
        return "\n".join(netlist)

    def __str__(self):
        s = [
             "**********************"
            ,"* name    %s" % self.name
            ,"* length  %s" % self.length
            ,"* gage    %s" % self.gage
            ,"* seg_max %s" % self.max_seg_length
            ,"* nsegs   %f" % self.nsegs
            ,"* whole   %f" % self.whole
            ,"* part    %f" % self.part
            ,"**********************"
            ]
        return "\n".join(s)

    def instance(self):
        """Generate the instance call for this cable segment"""
        return "x%s %sp %sn %sp %sn rtn %s" % \
                (
                    self.name,
                    self.port1, self.port1,
                    self.port2, self.port2,
                    self.name
                )

    def port1_current(self):
        return "ix(%s:0000n)" % (self.name)

    def port2_current(self):
        return "ix(%s:%04dn)" % (self.name, self.total_segs)

    def port1_voltage(self):
        return [
                "v(%sp)" % (self.port1),
                "v(%sn)" % (self.port1)
                ]

    def port2_voltage(self):
        return [
                "v(%sp)" % (self.port2),
                "v(%sn)" % (self.port2)
                ]


if __name__ == '__main__':
    Trunk(length=100, start_pad=0, end_pad=0, separation_min=1, start_attach=4, end_attach=1, random_attach=True)
    Trunk(length=100, start_pad=0, end_pad=0, separation_min=1, start_attach=4, end_attach=3, random_attach=True)
    Trunk(length=15, start_pad=0, end_pad=0, separation_min=1, start_attach=0, end_attach=0, random_attach=False)
    Trunk(length=100, nodes=32, start_pad=0, end_pad=0, separation_min=1, start_attach=0, end_attach=0, random_attach=False)
