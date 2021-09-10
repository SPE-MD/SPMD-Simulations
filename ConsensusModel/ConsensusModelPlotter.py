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


class ConsensusModelPlotter(object):
    """Takes results and makes graphs"""
    def __init__(self):
        self.results = None
        self.nodes = None
        self.tx_node = None
        self.trunk = None

        self.noautoscale = None
        self.noautoscale = None
        self.length = None
        self.plot_png_filename = None
        self.noplot = None

        ################################################################################
        #Set up containers to plot the output
        ################################################################################
        #containers to hold output data for plotting
        self.fig, (self.ax1, self.ax2, self.ax3, self.ax4) = plt.subplots(4,1, figsize=(9, 9))  # Create a figure and an axes.
        self.frequency = []
        self.s11_plot  = []
        self.s21_plot  = []
        self.plot_attach = []
        self.plot_drop = []
        self.csv_aoa = []

    def frequency_dom_to_time_dom(self,frequencies, s11Data):
        N_bins = 64
        N_seg = 4
        N_discard = 2
        return micro_reflections(frequencies, s11Data,  N_bins, N_seg, N_discard)

    def return_loss_limit(self,freq):
        rl=[]
        for x in freq:
            rl.append(self._rl(x))
        return rl

    def _rl(self,x):
        if(x < 0.3e6):
            return np.nan 
        elif(x < 10e6):
            return -14 
        elif(x < 40e6):
            return -1*(14 - 10 * math.log10(x / 10e6))
        else:
            return np.nan

    def insertion_loss_limit(self,freq):
        il=[]
        for x in freq:
            il.append(self._il(x))
        return il


    def _il(self,x):

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



    def generatePlots(self):
        ################################################################################
        #Extract data from the rawfile
        ################################################################################
        for n in self.nodes:
            if n != self.tx_node:
                sparams = self.results.scattering_parameters(
                        self.tx_node.phy_port_voltage(),
                        self.transmitter.transmitter_current(),
                        n.phy_port_voltage(),
                        n.termination_current(),
                        rin=50, rout=50)

                self.frequency.append(sparams['frequency'])
                self.s11_plot.append(sparams['s11'])
                self.s21_plot.append(sparams['gain'])

                ### complile data in an aoa for the csv file.
                if self.csv_aoa == []:
                    self.csv_aoa.append(["#frequency"]+sparams['frequency'])
                    self.csv_aoa.append(["#RL_node_%d" % self.tx_node.number]+sparams['s11'])
                self.csv_aoa.append(["#IL_node_%d" % n.number]+sparams['gain'])

        ################################################################################
        #Write the csv file
        ################################################################################
        csvFile = os.path.join("zcable.csv")
        with open(csvFile, 'w') as csv:
            csv.write(mpUtil.aoa2csv(mpUtil.transpose(self.csv_aoa)))

        ################################################################################
        #Plot the data
        ################################################################################
        #MatPlotLib Default
        # color_array = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', 
        #                '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', 
        #                '#bcbd22', '#17becf']

        #Sample static array of color values
        # color_array =['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6', 
        #               '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
        #               '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A', 
        #               '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
        #               '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC', 
        #               '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
        #               '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680', 
        #               '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
        #               '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3', 
        #               '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF']

        # Generate evenly spaced hue color list in spectral order
        color_array = []

        #Hue steps from 0 to 0.75 equate to 0 to 270 degrees Hue, or roughly red to violet
        #We don't go all the way to 1.0 because that would wrap back around to red

        for color_step in np.linspace(0, 0.75, num=len(self.nodes)):
            (red,green,blue) = colorsys.hsv_to_rgb(color_step,1,1)
            color_array.append('#%02X%02X%02X' % (int(red*255), int(green*255), int(blue*255)))  

        self.rl_limit = self.return_loss_limit(self.frequency[0])
        self.il_limit = self.insertion_loss_limit(self.frequency[0])
        self.ax1.plot(self.frequency[0], self.rl_limit, label="clause 147 limit")  # Plot more data on the axes...
        self.ax2.plot(self.frequency[0], self.il_limit, label="clause 147 limit")  # Plot more data on the axes...
        self.ax1.plot(self.frequency[0], self.s11_plot[0], label="test", color='k')  # Plot more data on the axes...
        timeDomainData = []
        self.ax4.set_ylim([-10e7,10e7])
        
        for i,p in enumerate(self.frequency):
            self.ax2.plot(self.frequency[i], self.s21_plot[i], label="test", color=color_array[i])  # Plot more data on the axes...
            #self.ax1.plot(self.frequency[i], self.s11_plot[i])  # Plot more data on the axes...
            #self.ax2.plot(self.frequency[i], self.s21_plot[i])  # Plot more data on the axes...
            timeDomainDataRaw = self.frequency_dom_to_time_dom(self.frequency[i],self.s11_plot[i])
            timeDomainData.append(timeDomainDataRaw[0:int(len(timeDomainDataRaw)/2)])
            #self.ax4.plot(range(len(timeDomainData[i])), timeDomainData[i], label="time", color=color_array[i])  # Plot more data on the axes...


        self.ax1.set_ylabel('RL (dB)')  # Add an x-label to the axes.
        self.ax1.set_xlim([0,40e6])
        if(self.noautoscale):
            self.ax1.set_ylim([-70,10])

        self.ax2.set_ylabel('Rx/Tx (dB)')  # Add an x-label to the axes.
        self.ax2.set_xlabel('Frequency')  # Add a y-label to the axes.
        self.ax2.set_xlim([0,40e6])
        if(self.noautoscale):
            self.ax2.set_ylim([-20,10])
        self.ax1.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=2)  # Add a legend.

        #self.ax3.set_xlim([-1,int(self.length)+1])
        if(self.noautoscale):
            self.ax3.set_xlim([-1,101])
        self.ax3.set_ylim([-1,1])
        self.ax3.set_xlabel('Attach (m)')  # Add a x-label to the axes.
        self.ax3.set_ylabel('Drop (m)')  # Add a x-label to the axes.

        #mixing segment line
        self.ax3.plot([0,self.length],[0,0], color="k")
        color_index = 0
        for node in self.trunk.attach_points:
            self.ax3.plot([node], np.zeros_like([node]), "-o", color=color_array[color_index])
            color_index += 1
        self.ax3.plot(self.trunk.attach_points[self.tx_index-1], np.zeros_like(self.trunk.attach_points[self.tx_index-1]),
                "-*",
                color="k",
                markerfacecolor="k",
                markersize=12
                )

        #generate a list with the drop lengths
        self.plot_drop=[]
        for node in self.nodes:
            #make every other drop go above/below the trunk line so it is easier to
            #see what is happening
            if(node.number % 2 == 0):
                self.plot_drop.append(-1 * node.drop_length)
            else:
                self.plot_drop.append(node.drop_length)

        #add the drop lengths to the plot
        self.ax3.vlines(self.trunk.attach_points, 0, self.plot_drop, color="tab:red")
        
        self.ax4.set_ylabel('Amplitude')  # Add an x-label to the axes.
        self.ax4.set_xlabel('Time')  # Add a y-label to the axes.

        #save the plot as a png file incase another script is making a gif
        plt.savefig(self.plot_png_filename)
        if not self.noplot:
            print("#Close plot window to continue")
            plt.show()
