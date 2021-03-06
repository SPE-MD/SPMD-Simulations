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
from pprint import pprint as pprint
from scipy import constants
#from multiprocessing import Process

sys.path.append(dirname(__file__)) #adds this file's director to the path
#import subprocess
import adisimlib.runspice as runspice
import adisimlib.mpUtil as mpUtil
from adisimlib.ltcsimraw import ltcsimraw as ltcsimraw
#from steptable import StepTable
from adisimlib.spifile import SpiFile as SpiFile
from micro_reflections import micro_reflections

from adisimlib.cable import Cable as Cable
from adisimlib.node import Node as Node
from adisimlib.termination import Termination as Termination
from adisimlib.transmitter import Transmitter as Transmitter
from adisimlib.trunk import Trunk as Trunk

class ConsensusModelPlotterConfig(object):
    """Contains all the parameters used when plotting graphs"""
    def __init__(self):
        self.noautoscale = None
        self.noautoscale = None
        self.length = None
        self.plot_png_filename = None
        self.noplot = None

    def __str__(self):
        returnString =  "\nPlotterConfig\n"
        returnString += "noautoscale:       %d\n" % self.noautoscale
        returnString += "noautoscale:       %s\n" % self.noautoscale
        returnString += "length:            %s\n" % self.length
        returnString += "plot_png_filename: %s\n" % self.plot_png_filename
        returnString += "noplot:            %f\n" % self.noplot
        return returnString

    def configureWithCommandLineArguments(self,args):
        self.noautoscale = args.noautoscale
        self.length = args.length
        self.plot_png_filename = args.plot_png_filename
        self.noplot = args.noplot

class ConsensusModelPlotter(object):
    """Takes results and makes graphs"""
    def __init__(self, topology=None, results=None):
        self.topology = topology
        self.results = results
        self.nodes = None
        self.tx_node = None
        self.trunk = None

        self.config = ConsensusModelPlotterConfig()

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

    def configureWithCommandLineArguments(self,args):
        self.config.configureWithCommandLineArguments(args)

    def frequency_dom_to_time_dom(self, frequencies, s11Data):
        N_samples = 800
        
        # print("frequencies[0]")
        # pprint(frequencies[0])
        # print("s11Data[0]")
        # pprint(s11Data[0])

        nonuniform_spacing = np.sum(np.abs(np.diff(np.abs(np.diff(frequencies)))))
        if abs(nonuniform_spacing) > 1e-6:
            print ("F Length: ",len(frequencies))
            print("F Contents:\n",frequencies)
            raise ValueError('Spacing of frequency points is not uniform')
        else:
            # print ("F Length: ",len(frequencies))
            frequency_spacing = frequencies[1] - frequencies[0]
            # print("Frequency Spacing: ", frequency_spacing, " Hz")
            max_frequency = frequencies[len(frequencies)-1]
            # print("Max Frequency: ", max_frequency, " Hz")

        h_echo = micro_reflections(frequencies, s11Data, N_samples)
        sample_array = range(0,int(len(frequencies)))
        t_echo = np.array(sample_array)/(2*max_frequency)

        # print("h_echo[0]")
        # pprint(h_echo)
        # print("t_echo[0]")
        # pprint(t_echo)

        return (t_echo, 20*np.log10(abs(h_echo[0:int(len(h_echo)/2)])))

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

        
        self.nodes = self.topology.simNetwork.nodes
        self.tx_node = self.topology.simNetwork.tx_node
        self.transmitter = self.topology.simNetwork.transmitter
        self.tx_index = self.topology.simNetwork.tx_index
        self.trunk = self.topology.simNetwork.trunk

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
        # self.ax4.set_ylim([-5,10])
        
        for i,p in enumerate(self.frequency):
            (timeDomainTimeAxis, timeDomainData) = self.frequency_dom_to_time_dom(self.frequency[i],self.s21_plot[i])
            # self.ax4.plot(range(len(timeDomainData[i])), timeDomainData[i], label="time", color=color_array[i])  # Plot more data on the axes...
            self.ax4.plot(timeDomainTimeAxis*1e6, timeDomainData, label="time (ms)", color=color_array[i])  # Plot more data on the axes...
            #timeDomainTimeAxis
            
            # DC Point is garbage
            self.s21_plot[i][0] = 0

            self.ax2.plot(self.frequency[i], self.s21_plot[i], label="test", color=color_array[i])  # Plot more data on the axes...
            #self.ax1.plot(self.frequency[i], self.s11_plot[i])  # Plot more data on the axes...
            #self.ax2.plot(self.frequency[i], self.s21_plot[i])  # Plot more data on the axes...

        self.ax1.plot(self.frequency[0], self.rl_limit, label="clause 147 limit")  # Plot more data on the axes...
        self.ax2.plot(self.frequency[0], self.il_limit, label="clause 147 limit", color='k')  # Plot more data on the axes...
        self.ax1.plot(self.frequency[0], self.s11_plot[0], label="test", color='k')  # Plot more data on the axes...
        
        self.ax1.set_ylabel('RL (dB)')  # Add an x-label to the axes.
        self.ax1.set_xlim([0,40e6])
        if(self.config.noautoscale):
            self.ax1.set_ylim([-70,10])

        self.ax2.set_ylabel('Rx/Tx (dB)')  # Add an x-label to the axes.
        self.ax2.set_xlabel('Frequency')  # Add a y-label to the axes.
        self.ax2.set_xlim([0,40e6])
        
        if(self.config.noautoscale):
            # if True:
            self.ax2.set_ylim([-20,10])
        self.ax1.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=2)  # Add a legend.

        #self.ax3.set_xlim([-1,int(self.config.length)+1])
        if(self.config.noautoscale):
            self.ax3.set_xlim([-1,101])
        self.ax3.set_ylim([-1,1])
        self.ax3.set_xlabel('Attach (m)')  # Add a x-label to the axes.
        self.ax3.set_ylabel('Drop (m)')  # Add a x-label to the axes.

        #mixing segment line
        self.ax3.plot([0,self.config.length],[0,0], color="k")
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
        
        self.ax4.set_ylabel('Amp (pseudo db)')  # Add an x-label to the axes.
        self.ax4.set_xlabel('Time (us)')  # Add a y-label to the axes.
        self.ax4.minorticks_on()
        cable_velocity_factor = 0.75
        segment_propagation_time = self.config.length / (constants.speed_of_light * cable_velocity_factor)
        xticks = np.arange(0,timeDomainTimeAxis[len(timeDomainTimeAxis)-1]*1e6,segment_propagation_time*1e6)
        # print("xticks")
        # print(xticks)
        
        #draw xticks every full cable length  propagation time interval
        self.ax4.set_xticks(xticks,minor=True)
        self.ax4.set_xticklabels(["%d OWT" % x for x in range(len(xticks))],minor=True)
        self.ax4.xaxis.set_tick_params(which='minor', direction='in', pad=-20, labelbottom=False, labeltop=False, rotation=0)
        self.ax4.grid(axis='x', which='minor')
        # self.ax4.set_xticks([0.35,0.7,1.05],minor=True)

        #save the plot as a png file incase another script is making a gif
        plt.savefig(self.config.plot_png_filename)
        if not self.config.noplot:
            print("#Close plot window to continue")
            plt.show()
