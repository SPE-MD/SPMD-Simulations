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
#from scipy.signal import butter, lfilter, freqz
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
import datetime
import colorsys
import json
#from multiprocessing import Process


sys.path.append(dirname(__file__)) #adds this file's director to the path
#import subprocess
import runspice
import mpUtil
from ltcsimraw import ltcsimraw as ltcsimraw
#from steptable import StepTable
from spifile import SpiFile as SpiFile
#from micro_reflections import micro_reflections

from cable import Cable as Cable
from cable import CableModel as CableModel
from node import Node as Node
from termination import Termination as Termination
from transmitter import Transmitter as Transmitter
from trunk import Trunk as Trunk
from t_connector import T_connector as T_connector
from dme import dme_transmitter as dme_transmitter
from dme import eye_diagram 
from dme import dme_receiver

def _readTxt(infile):
    try :
        file = open(infile)
    except:
        print("cannot open: %s" % infile)
        return ""

    text = ""
    with file as inf:
        #self.text = []
        for line in inf:
            #line = line.rstrip()
            text += line
    inf.close
    return text

def writeHtml(config, eye_data, min_corr_value):
        header_txt = _readTxt(os.path.join(config['htmlTemplates'],config['headerHtml']))
        tailer_txt = _readTxt(os.path.join(config['htmlTemplates'],config['tailerHtml']))
        css_file = os.path.join(config['htmlTemplates'],config['cssFile'])
        try:
            dst = os.path.join("data",config['design_md5'],config['cssFile'])
            src = css_file
            shutil.copyfile(src, dst)

        except:
            print("Cannot copy .css file")
            exit(1)

        html = header_txt
        html += "<body>"
        html += "<DIV class=content>"
        html += "<DIV class=main>"
        html += "<p class=label>%s</p>" % (config['design_md5'])
        html += "<p class=label>MinCorr=%.3f</p>" % (min_corr_value)
        html += "<p class=label>Nodes=%d</p>" % (config['nodes'])
        html += "<p class=label>Length=%.2f</p>" % (config['length'])
        html += "</DIV>"
        html += "</DIV>"

        if('eye_gif_mdi' in config):
            html += "<DIV class=content>"
            html += "<DIV class=main>"

            html += "<p class=label>%s</p>" % ("Eye @ MDI")
            html += "<a href=\"img/%s\">" %config['eye_gif_mdi']
            html += "<img src=\"img/%s\" alt=\"img/%s\" width=\"800\"></img>" % (config['eye_gif_mdi'], config['eye_gif_mdi'])
            html += "</a>"
            html += "</DIV>"
            html += "</DIV>"

        html += "<DIV class=content>"
        html += "<DIV class=main>"
        html += "<p class=label>%s</p>" % ("Eye after filter")
        html += "<a href=\"img/%s\">" %config['eye_gif_filtered']
        html += "<img src=\"img/%s\" alt=\"img/%s\" width=\"800\"></img>" % (config['eye_gif_filtered'], config['eye_gif_filtered'])
        html += "</a>"

        html += "</DIV>"
        html += "</DIV>"

        html += "<DIV class=content>"
        html += "<DIV class=main>"
        html += "<a href=\"img/%s\">" % config['plot_png_filename']
        html += "<img src=\"img/%s\" alt=\"img/%s\" width=\"800\"></img>" % (config['plot_png_filename'], config['plot_png_filename'])
        html += "</a>"
        html += "</DIV>"
        html += "</DIV>"

        html += "<DIV class=content>"
        html += "<DIV class=main>"
        html += "<a href=\"img/%s\">" % config['corr_png_filename']
        html += "<img src=\"img/%s\" alt=\"img/%s\" width=\"800\"></img>" % (config['corr_png_filename'], config['corr_png_filename'])
        html += "</a>"
        html += "</DIV>"
        html += "</DIV>"

        html += "<HR>"

        html += "<table align=\"center\">"
        html += "<TR>"
        n=0
        for e in eye_data:
            #html += e.getHtmlOutput()
            eye_plot = "%s%d.png" % (e.filename, e.node_number)
            html += "<TD>"
            html += "<a href=\"img/%s\">" % eye_plot
            html += "<img src=\"img/%s\" alt=\"img/%s\" width=\"200\"></img>" % (eye_plot, eye_plot)
            html += "</a>"
            html += "</TD>"
            n+=1
            if(n % 4 == 0):
                html += "</TR><TR>"
        html += "</TR>"
        html += "</table>"
        html += tailer_txt

        htmlFile = os.path.join("data",config['design_md5'],'report.html')
        f = open(htmlFile,"w")
        f.write(html)
        f.close()
        import webbrowser
        webbrowser.open(htmlFile, new=0, autoraise=True)


def butter_lowpass(cutoff, fs, order=1):
    return butter(order, cutoff, fs=fs, btype='lowpass', analog=False)

def frequency_dom_to_time_dom(data):
    return micro_reflections(data, T=0.10, N=256)

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

    #dictionary to hold test specific json settings
    config = {}
    #read in default settings from defaults.json
    config_default = {}
    try:
        with open("defaults.json") as json_file:
            config_default = json.load(json_file)
            #print(config_default)
    except Exception as e:
        print(e)
        print("Issue loading 'defaults.json'")
        exit(1)


    with open(csvFile, 'w') as csv:
        #delete the csvFile.  It gets filled up in append mode later...
        pass

    parser = argparse.ArgumentParser(
        description='802.3da network model generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

    parser.add_argument('--nodes', type=int, \
            help='Set the number of nodes in the simulation', \
            #default=config_default['nodes']
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

    parser.add_argument('--start_pad', type=float, \
            help='Specify the distance between start of cable and the 1st node',
            #default=config_default['start_pad']
            )

    parser.add_argument('--end_pad', type=float, \
            help='Specify the distance between end of cable and the last node',
            #default=config_default['end_pad']
            )

    parser.add_argument('--start_attach', type=int, \
            help='Specify an number of nodes to be placed at the start of the mixing\
            segment with \'separation_min\' spacing',
            #default=config_default['start_attach']
            )

    parser.add_argument('--end_attach', type=int, \
            help='Specify an number of nodes to be placed at the end of the mixing\
            segment with \'separation_min\' spacing',
            #default=config_default['end_attach']
            )

    parser.add_argument('--length', type=float, \
            help='Mixing segment length in meters, will be rounded to an integer\
            number of segments per meter',\
            #default=config_default['length']
            )

    parser.add_argument('--segments_per_meter', type=int, \
            help='Size of finite element cable model segments.  Be sure this\
            lines up with lump models',\
            #default=config_default['segments_per_meter']
            )

    parser.add_argument('--drop_max', type=float, \
            help='Drop length between mixing segment and PD attachment in\
            meters.  This number will be rounded to an interger number of\
            segments per meter',
            #default=config_default['drop_max']
            )

    parser.add_argument('--random_drop',
            action='store_true',\
            help='When set, node drop length will be chosen at random between\
            zero and drop_max. Drop lengths should be reproducible by reusing\
            the seed value from another sim (see the --seed flag) Otherwise,\
            drop lengths will be evenly distributed across the mixing segment',
            )

    parser.add_argument('--separation_min', type=float, \
            help='Minimum separation between nodes in meters.  This number will\
            be rounded to an integer number of segments per meter',\
            #default=1.0\
            )

    parser.add_argument('--lcomp', type=float, \
            help='Compensation inductance added to tconnector ports',
            #default=config_default['default_node']['lcomp']
            )

    parser.add_argument('--cnode', type=float, \
            help='Node capacitance in Farads.  All nodes will be assigned this MDI interface capacitance',\
            #default=config_default['default_node']['cnode']
            )

    parser.add_argument('--lpodl', type=float, \
            help='Node inducatnce in Henrys.  All nodes will be assigned this MDI interface inductance',\
            #default=config_default['default_node']['lpodl']
            )

    parser.add_argument('--rnode', type=float, \
            help='Node resistance in Ohms.  All nodes will be assigned this MDI interface resitance',\
            #default=config_default['default_node']['rnode']
            )

    parser.add_argument('--seed', type=int, \
            help='Seed value for random number generator',\
            #default=config_default['seed']
            )

    parser.add_argument('--tx_node', type=int, \
            help='Set the transmitter node.',\
            #default=config_default['tx_node']
            )

    parser.add_argument('--noplot', action='store_true', help='set this flag to\
            prevent plotting')
    
    parser.add_argument('--plot_png_filename', type=str, \
            help='Filename for plot image output as a .png file. Default is zcable.png',\
            #default=config_default['plot_png_filename']
            )

    parser.add_argument('--noautoscale', action='store_true',\
            help='set this flag to lock the y-axis on IL/RL plots to -80dB/-70dB\
            respectively.  The xaxis on the network model will be locked at -1m to 101m'
            )

    parser.add_argument('--attach_error', type=float, \
            help='add gaussian error to attachment points.  Pass the the sigma value of the attachment\
            error or 0 for no error.  Ignored for randomly placed nodes.  If'\
            'attach_error is set to a large value, can separation_min be violated?'\
            'I don\'t know',\
            #default=config_default['attach_error']
            )

    parser.add_argument('--fft', type=str, \
            help='fft of and input signal in text form to be multiplied against the insertion loss\
            then ifft is applied to reconstruct the time domain signal shape',
            default=None
            )

    parser.add_argument('--attach_points', type=float, nargs='+',\
            help='specify the mixing segment attachment points with a space separated list\
            --nodes is overridden by the length of this list.  Make sure this list is ordered',\
            #default=config_default['attach_points']
            )

    parser.add_argument('--eye_adjust', type=float, nargs=2,\
            help='adjust eye diagram delay, set the delay to be positive because the parser cannot handle\
            negative numbers',
            #default=[0,0]
            )

    parser.add_argument('--json', type=str, \
            help='specify a json file containing a system description',
            default=None
            )


    args = parser.parse_args()


    ################################################################################
    #Setup a list of node descriptions for easier access during the netlist build phase
    #make a list of nodes with 'default_node' configuration
    #then override node settings with specific node settings from the test specific json file
    ################################################################################
    #read in the json file if it is defined
    #config = dict()
    if(args.json):
        try:
            with open(args.json) as json_file:
                config = json.load(json_file)
                #print(config)
                #exit(1)
        except Exception as e:
            print(e)
            exit(1)

    #args.json overrides defaults, command line args override everything
    #all necessary information to make the model run needs to be defined in defaults.json
    #but let test specific json data override default json data
    for key in config_default:
        if key in config:
            config_default[key] = config[key]

    #not all of the default config is required in the test specific json file
    #copy the default (with overrides) json data back into the test specifc json data
    #to make sure the config data is complete
    for key in config_default:
        config[key] = config_default[key]
        #print("%s = %s" % (key, config[key]))

    #let command line data override any other json data
    if args.nodes:
        config['nodes']                       = args.nodes
    if args.length:
        config['length']                      = args.length
    if args.random_attach:
        config['random_attach']               = args.random_attach
    if args.start_attach:
        config['start_attach']                = args.start_attach
    if args.end_attach:
        config['end_attach']                  = args.end_attach
    if args.start_pad:
        config['start_pad']                   = args.start_pad
    if args.end_pad:
        config['end_pad']                     = args.end_pad
    if args.separation_min:
        config['separation_min']              = args.separation_min
    if args.segments_per_meter:
        config['segments_per_meter']          = args.segments_per_meter
    if args.drop_max:
        config['drop_max']                    = args.drop_max
    if args.random_drop:
        config['random_drop']                 = args.random_drop
    if args.seed:
        config['seed']                        = args.seed
    if args.tx_node:
        config['tx_node']                     = args.tx_node
    if args.attach_error:
        config['attach_error']                = args.attach_error
    if args.attach_points:
        config['attach_points']               = args.attach_points
    if args.drop_max:
        config['default_node']['drop_length'] = args.drop_max
    if args.random_drop:
        config['default_node']['random_drop'] = args.random_drop
    if args.cnode:
        config['default_node']['cnode']       = args.cnode
    if args.lcomp:
        config['default_node']['lcomp']       = args.lcomp
    if args.lpodl:
        config['default_node']['lpodl']       = args.lpodl
    if args.rnode:
        config['default_node']['rnode']       = args.rnode
    if args.rnode:
        config['noplot']                      = args.noplot

    if not "htmlTemplates" in config: 
        config["htmlTemplates"] = "htmlTemplates"
    if not "headerHtml" in config:
        config["headerHtml"] = "header.html"
    if not "tailerHtml" in config:
        config["tailerHtml"] = "tailer.html"
    if not "cssFile" in config:
        config["cssFile"] = "promis.css"
    if not "corr_png_filename" in config:
        config["corr_png_filename"] = "corr.png"
    ################################################################################
    #Setup random seed in case this run has random parameters
    ################################################################################
    seed = config['seed']
    if seed == -1:
        tim = datetime.datetime.now()
        seed = tim.hour*10000+tim.minute*100+tim.second
        config['seed'] = seed #is this a bad idea? Should the seed stay consistent or stay random?
        random.seed(seed)
    else:
        random.seed(seed)
    np.random.seed(seed)
    print("#Random Seed = %s" % seed)
    ################################################################################

    ################################################################################
    #Setup a list of node descriptions for easier access during the netlist build phase
    #make a list of nodes with 'default_node' configuration
    #then override node settings with specific node settings from the test specific json file
    ################################################################################
    nds = []
    #stick default node at index 0, I have no intention of it being accessed because node 
    #numbering starts at '1', but nds[0]==None bugs me.
    nds.append(config['default_node'])

    #make a list of nodes with default configuration
    for i in range(1,config['nodes']+1):
        n = dict(config['default_node'])
        n['number'] = i
        nds.append(n)

    #override node settings with specific node settings from the test specific json file
    if(config['node_descriptions']):
        for i in config['node_descriptions']:
            if not 'number' in i:
                continue
            #check if the node number is present in the test.
            #the node number could be out of range if a command line argument overrode
            #the number of nodes described in the test specific json file
            try:
                for key in i:
                    nds[i['number']][key] = i[key]
            except:
                print("WARN: Node %d ignored from '%s'. Command line arguments set --nodes=%d" 
                        % (i['number'],args.json,config['nodes']))

    #copy the node list back to the config dict
    config['node_descriptions'] = nds
    ################################################################################
    # End Node data shructure setup
    ################################################################################

    ################################################################################
    # Termination data structure
    ################################################################################
    terms = dict()
    for side in ['start','end']:
        terms[side] = dict(config['default_termination'])
        try:
            for key in config['termination'][side]:
                terms[side][key] = config['termination'][side][key]
        except:
            pass
    config['termination'] = terms
    ################################################################################
    # End termination data shructure setup
    ################################################################################


    #tpd=3.335e-9      #speed of light on this cable
    #z0 = 100          #cable impedance
    #l_m = tpd * z0    #inductance per meter
    #c_m = tpd / z0    #capacitance per meter
    #r_m = 0.188       #dc resistance per meter
    #r_m = 0.001       #dc resistance per meter

    #18 awg l and c data for a 5cm segment
    #l1 a t2p {1*20.6435n}
    #c1 t2p x {1*2.25026p}
    #l_m = 20.6435e-09 / 0.05
    #c_m = 2.25026e-12 / 0.05

    #llump = l_m / args.segments_per_meter
    #clump = c_m / args.segments_per_meter
    #rlump = r_m / args.segments_per_meter 


    ################################################################################
    #Make trunk segments that will connect the nodes
    ################################################################################
    #a list of specific attachment points overrides the number of nodes argument
    if(config['attach_points']):
        config['nodes'] = len(config['attach_points'])
   
    #this object figures out how many cable segments are needed and what length each segment
    #should be.
    #trunk object figures out a list of attach_points after this object is instantiated
    trunk=Trunk( length=config['length']
            , nodes=config['nodes']
            , start_pad=config['start_pad']
            , end_pad=config['end_pad']
            , separation_min=config['separation_min']
            , start_attach=config['start_attach']
            , end_attach=config['end_attach']
            , random_attach=config['random_attach']
            , attach_error=config['attach_error']
            , attach_points=config['attach_points']
            , max_seg_length=(1/config['segments_per_meter'])
            )

    #feed back precise attach points into json data structure
    config['attach_points'] = trunk.attach_points

    #Prepare a data structure to hold cable models and trunk segment parameters
    #actual number of cables segments is between nnodes-1 and nnodes+1
    #add an extra cable segment if attach_point[0] != 0
    #add an extra cable segment if attach_point[-1] != config['length']
    #always declare space for segment[0] and segment[nodes+1] 
    #expect that segment[0] and segment[nodes+1] will be ignored later if they are not needed
    
    #build a list of default segments
    nsegs=config['nodes']+1
    trunk_segments = []
    for x in range(nsegs):
        trunk_segments.append(dict(config['default_segment']))
        #make sure segments with a default config get a segment number assigned
        trunk_segments[-1]['segment']=x
    #print(trunk_segments)

    #override default segment description with any segments described specifically in the json files
    for s in config['trunk_description']['segments']:
        #print(s)
        index = s['segment']
        for key in s:
            #print(key)
            trunk_segments[index][key] = s[key]

    #print(trunk_segments)
    config['trunk_description']['segments'] = trunk_segments

    #load cable models from the json files
    #json.dump(config['cable_models'], sys.stdout, indent=2)
    cable_models = dict()
    for cm in config['cable_models']:
        try:
            cable_models[cm] = CableModel(
                    name=cm
                    , gauge      = config['cable_models'][cm]['gauge']
                    , rdc        = config['cable_models'][cm]['rdc']
                    , l          = config['cable_models'][cm]['l']
                    , c          = config['cable_models'][cm]['c']
                    , rskin      = config['cable_models'][cm]['rskin']
                    , ref_length = config['cable_models'][cm]['ref_length']
                    )
        except Exception as e:
            print("Missing data in cable model : %s" % cm)
            print(e)
                                
    #this function instantiates Cable objects representing the cables that connect each node or termination
    #and returns the cable objects in a list
    trunk_segments = trunk.get_cable_segments(config['trunk_description']['segments'], cable_models)
    #json.dump(config, sys.stdout, indent=2)
    
    #make a copy of the trunk segments list because it will be destroyed during the next step
    trunk_temp = list(trunk_segments) 
    
    ################################################################################
    #Using the cable segements from Trunk, build up the mixing segment, including 
    #end terminations, t-connectors and cable segments.
    #The t-connectors have ports that will connect to the nodes in spice.
    #The mixing segment comes back as an ordered list describing the components from start to end
    ################################################################################
    mixing_segment = []
    node_iter=0

    cond1 = (config['attach_points'] == None and config['start_pad'] == 0)
    cond2 = (config['attach_points'] != None and config['attach_points'][0] == 0)

    #is there 0 distance between the 1st node and the start termination?
    #if so change the name of the termination's start terminal
    ccouple =  config['termination']['start']['ccouple']
    rterm   =  config['termination']['start']['rterm']
    if(cond1 or cond2):
        term_start = Termination(
                name="start_term"
                , port="ts"
                , stim_port="start"
                , ccouple=ccouple
                , rterm=rterm
                )
        mixing_segment.append(term_start)
    else: 
        term_start = Termination(
                name="start_term"
                , port=trunk_temp[0].port1
                , stim_port="start"
                , ccouple=config['termination']['start']['ccouple']
                )
        mixing_segment.append(trunk_temp.pop(0))
        mixing_segment.append(term_start)

    node_iter=1
    while(trunk_temp):
        port = "y%d" % node_iter
        #see if there is a unique node description in the json data
        tee = T_connector(
                number=node_iter
                , port1=mixing_segment[-1].port2
                , port2=trunk_temp[0].port1
                , node_port=port
                , lcomp       = config['node_descriptions'][node_iter]['lcomp']
                , lcomp_match = config['node_descriptions'][node_iter]['lcomp_match']
                )
        node_iter+=1
        #put a t-connector on the mixing segment
        mixing_segment.append(tee)
        #put a cable segment in the mixing segement
        mixing_segment.append(trunk_temp.pop(0))

    #is there 0 distance between the last node and the end termination?
    #if so add a t-connector to the last cable segment
    #cond1: pad between the last node and end term is set to '0' and another node needs to be placed
    #cond2: attach points were specified and the last point is at the same spot as the cable end
    cond1 = (config['end_pad'] == 0 and node_iter <= config['nodes'])
    cond2 = (config['attach_points'] != None and config['attach_points'][-1] == config['length'])
    #print("cond1: %s" % cond1)
    #print("cond2: %s" % cond2)
    if( cond1 or cond2 ):
        port = "y%d" % node_iter
        tee = T_connector(
                number=node_iter
                ,port1=mixing_segment[-1].port2
                ,port2="end"
                ,node_port=port
                ,lcomp=config['node_descriptions'][node_iter]['lcomp']
                )
        node_iter+=1
        mixing_segment.append(tee)
 
    #attach the termination to the last piece of the mixing segment
    ccouple =  config['termination']['end']['ccouple']
    rterm   =  config['termination']['end']['rterm']
    term_end   = Termination(name="end_term", port=mixing_segment[-1].port2, stim_port="end_stim", ccouple=ccouple, rterm=rterm)
    mixing_segment.append(term_end)

    #for m in mixing_segment:
    #    print(m)


    ################################################################################
    #Attach nodes to the mixing segment
    #Nodes don't actually get attached to the mixing segment list, but they get linked
    #to the t-connectors through port names when the netlist gets built
    ################################################################################
    nodes = []
    for n in range(1,config['nodes']+1):
        port="y%d" % (n)
        node = Node(number=n
                , port=port
                , drop_length = config['node_descriptions'][n]['drop_length']
                , random_drop = config['node_descriptions'][n]['random_drop']
                , cnode       = config['node_descriptions'][n]['cnode']
                , lpodl       = config['node_descriptions'][n]['lpodl']
                , rnode       = config['node_descriptions'][n]['rnode']
                , spice_model = config['node_descriptions'][n]['spice_model']
                )
        nodes.append(node)
        #print(node)

    ################################################################################
    #Determine which node will be the transmitter for the simulation
    ################################################################################
    #boundary check the transmit node index
    tx_node = config['tx_node']
    if tx_node<1: #choose a random transmit node
        tx_node = random.randint(1,config['nodes'])
        print("Randomly Chose Node %d as the transmitter" % tx_node)
    tx_index=min(tx_node, config['nodes'])
    tx_index=max(tx_index, 1)
    tx_node = nodes[tx_index-1]
    transmitter = Transmitter(port=tx_node.phy_port)


    ################################################################################
    #Save all settings complied from defaults, test specific json and command line args as "last_run.json"
    ################################################################################
    with open("last_run.json", 'w') as f:
        json.dump(config, f, indent=2)
       
    ################################################################################
    #Write a spice file with the system setup
    ################################################################################
    with open("cable.p", 'w') as cable:
        cable.write("*lumped transmission line model with %d segments per meter at %d meters\n"\
        % (config['segments_per_meter'], config['length']))
        cable.write("*and a %f meter long cable\n" % config['length'])

        for m in mixing_segment:
            cable.write(m.subcircuit()+"\n")
        for n in nodes:
            cable.write(n.subcircuit()+"\n")

        cable.write("** MAIN NETWORK DESCRIPTION **\n")
        for m in mixing_segment:
            cable.write(m.instance()+"\n")
        for n in nodes:
            cable.write(n.instance()+"\n")

    ################################################################################
    #Create an ac stimulus file
    #This is separate from the system spice file in case we also want to do
    # transient simulations.  Then another transient stimulus file will be
    # created at some point
    ################################################################################

    if(config['analysis'] != 'ac'):
        exit(0)

    cirfile = "zcable.%s.cir" % config['analysis']
    rawfile = "zcable.%s.raw" % config['analysis']
    with open(cirfile, 'w') as zcable:
        zcable.write("*ac sim command for cable impedance measurement\n")
        if(not config['includes']):
            zcable.write(".include tlump2.p\n")
            zcable.write(".include node.p\n")
        else:
            for i in config['includes']:
                zcable.write("%s\n" % i)

        zcable.write(".include cable.p\n")

        #differential signal input
        zcable.write(transmitter.instance()+"\n")

        #path to ground
        zcable.write("vrtn rtn 0 0\n")

        #set up coherant sample parameters for the time domain data
        bits_to_prime = [[13, 1253],[14,617],[15,313]]
        Ns = 2**14
        per = 80e-9
        prime = 313
        Fs = Ns / (prime * per)
        
        #ac simulation command using coherant sample parameters
        zcable.write(".ac lin %d %.6g %.6g\n" % ((Ns/2), (Fs/Ns), Fs/2.))

        #select nodes to save to speed up the sim and reduce file size
        zcable.write(".save v(*) i(*)\n")
        for n in nodes:
            zcable.write("+ %s\n" % n.termination_current())



    ################################################################################
    #Set up and run a simulation, but don't run it twice if it has already been
    #run
    ################################################################################
    #condense the sim files into a single *.spi file
    #crete a md5 of the spi file then make a unique directory to store this sim
    #If batches of sims are run more than once, just extract the data without 
    #running the sim again
    spi = SpiFile(cirfile)
    spi.readCircuit()
    spi.followInclude = True
    spi.digestSpiceFile()
    design_md5 = spi.md5(skipParams=False,skipComments=True,skipSave=False)
    spiSave  = os.path.join("data",design_md5,design_md5+".spi")
    logSave  = os.path.join("data",design_md5,design_md5+".log")
    rawSave  = os.path.join("data",design_md5,design_md5+".raw")
    jsonSave = os.path.join("data",design_md5,design_md5+".json")
    outputdb = os.path.join("data",design_md5)
    imgDir   = os.path.join("data",design_md5,"img")
    config['design_md5'] = design_md5


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
            #save all settings complied from defaults, test specific json, and command line args in the outputdb folder"
            with open(jsonSave, 'w') as f:
                json.dump(config, f, indent=2)

        except:
            print( "Cannot create regression folder")
            exit(1)

    if not os.path.exists(imgDir):
        print( "img Folder %s does not exist" % imgDir)
        print( "Creating...." )
        try:
            os.makedirs(imgDir)
        except:
            print( "Cannot create img folder")
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
        print( "Pulling Sim From database %s" % design_md5) 

    except:
        print( "Running Simulation")
        runspice.runspice(spiSave)

    ################################################################################
    #Set up containers to plot the output
    ################################################################################
    #containers to hold output data for plotting
    fig, (rl_plot, il_plot, cm_plot, pspec_plot, network_plot) = plt.subplots(5,1, figsize=(9, 10))  # Create a figure and an axes.

    #set the simulation command as the window title.
    fig.canvas.manager.set_window_title(" ".join(sys.argv))

    frequency = []
    s11_plot  = []
    s21_plot  = []
    dm_cm_plot = []
    plot_attach = []
    plot_drop = []
    csv_aoa = []

    ################################################################################
    #Extract data from the rawfile
    ################################################################################
    rf=ltcsimraw(rawSave)
    sparams=None
    for n in nodes:
        if n != tx_node:
            sparams = rf.scattering_parameters(
                    tx_node.phy_port_voltage(),
                    transmitter.transmitter_current(),
                    n.phy_port_voltage(),
                    n.termination_current(),
                    rin=50, rout=50)

            frequency.append(sparams['frequency'])
            s11_plot.append(sparams['s11'])
            s21_plot.append(sparams['gain'])
            dm_cm_plot.append(sparams['dm_cm'])

            ### complile data in an aoa for the csv file.
            if csv_aoa == []:
                csv_aoa.append(["#frequency"]+sparams['frequency'])
                csv_aoa.append(["#RL_node_%d" % tx_node.number]+sparams['s11'])
            csv_aoa.append(["#IL_node_%d" % n.number]+sparams['gain'])

    ################################################################################
    #Write the csv file
    ################################################################################
    if(0):
        with open(csvFile, 'w') as csv:
            csv.write(mpUtil.aoa2csv(mpUtil.transpose(csv_aoa)))

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
    for color_step in np.linspace(0, 0.75, num=len(nodes)):
        (red,green,blue) = colorsys.hsv_to_rgb(color_step,1,1)
        color_array.append('#%02X%02X%02X' % (int(red*255), int(green*255), int(blue*255)))  

    nyquist=Fs/2
    print("nyquist = %.3e" % nyquist)
    xmax=nyquist
    xmax=40e6

    rl_limit = return_loss_limit(frequency[0])
    il_limit = insertion_loss_limit(frequency[0])

    il_plot.plot(frequency[0], il_limit, label="clause 147 limit")  
    il_plot.xaxis.set_major_formatter(EngFormatter(unit = 'Hz'))
    for i,p in enumerate(frequency):
        il_plot.plot(frequency[i], s21_plot[i], label="test", color=color_array[i])  
        cm_plot.plot(frequency[i], dm_cm_plot[i], label="test", color=color_array[i])  

    rl_plot.xaxis.set_major_formatter(EngFormatter(unit = 'Hz'))
    rl_plot.plot(frequency[0], rl_limit, label="clause 147 limit")  
    rl_plot.plot(frequency[0], s11_plot[0], label="test", color='k')  
    rl_plot.set_ylabel('RL (dB)')  
    rl_plot.set_xlim([0,xmax])
    rl_plot.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=2)  # Add a legend.
    if(config['noautoscale']):
        rl_plot.set_ylim([-70,10])

    il_plot.set_ylabel('Rx/Tx (dB)') 
    il_plot.set_xlabel('Frequency') 
    il_plot.set_xlim(   [0,xmax])
    cm_plot.set_xlim(   [0,xmax])
    cm_plot.xaxis.set_major_formatter(EngFormatter(unit = 'Hz'))
    pspec_plot.set_xlim([0,xmax])
    pspec_plot.xaxis.set_major_formatter(EngFormatter(unit = 'Hz'))
    if(config['noautoscale']):
        il_plot.set_ylim([-20,10])

    if(config['noautoscale']):
        pass
        #network_plot.set_xlim([-1,101])
    network_plot.set_ylim([-1,1])
    network_plot.set_xlabel('Attach (m)') 
    network_plot.set_ylabel('Drop (m)')  

    #mixing segment line
    network_plot.plot([0,config['length']],[0,0], color="k")
    color_index = 0
    for node in trunk.attach_points:
        network_plot.plot([node], np.zeros_like([node]), "-o", color=color_array[color_index-1])
        color_index += 1
    network_plot.plot(trunk.attach_points[tx_index-1], np.zeros_like(trunk.attach_points[tx_index-1]),
            "-*",
            color="k",
            markerfacecolor="k",
            markersize=12
            )

    #generate a list with the drop lengths
    plot_drop=[]
    for node in nodes:
        #make every other drop go above/below the trunk line so it is easier to
        #see what is happening
        if(node.number % 2 == 0):
            plot_drop.append(-1 * node.drop_length)
        else:
            plot_drop.append(node.drop_length)

    #add the drop lengths to the plot
    network_plot.vlines(trunk.attach_points, 0, plot_drop, color="tab:red")

    cm_plot.set_ylabel('CM / TX_DM')  # Add an y-label to the axes.
    #cm_plot.set_xlabel('Time')  # Add a y-label to the axes.


    ################################################################################
    # Time domain data / Eye Diagram Generation
    ################################################################################
    print("#Generating Random DME Signal")
    dme_tx = dme_transmitter(ts=1/Fs,ns=Ns,symbol_period=80e-9,n_symbols=prime,amplitude=0.010,zin=sparams['zin'])
    #dme_tx.add_filter("lpf",20e6,5)
    
    if(0):
        config['tx_filter_png'] = os.path.join("data",design_md5,"img",'tx_filter.png') 
        dme_tx.plot_filter(config['tx_filter_png'],title="tx_filter")

    if(0): #used to check / debug sampling data externally
        #dme_tx.output_pwl_to_file()
        #dme_tx.output_sampled_pwl_to_file()
        dme_tx.t_domain_filtered = np.fft.irfft(dme_tx.get_filtered_fft())
        dme_tx.output_t_domain_to_file()
        exit(1)

    #save the plot as a png file incase another script is making a gif
    pspec_plot.set_ylabel('DME Input Spectrum')  # Add an y-label to the axes.
    pspec_plot.plot(dme_tx.fft_freq,
            20*np.log10(np.absolute(dme_tx.get_filtered_fft())),color=color_array[0])
    pspec_plot.plot(dme_tx.fft_freq,
            20*np.log10(np.absolute(dme_tx.fft_value)),color=color_array[1])
    config['plot_png'] = os.path.join("data",design_md5,"img",config['plot_png_filename']) 
    plt.savefig(config['plot_png'])

    print("#Generating Eye Diagrams")
    eye_data_mdi = []
    eye_data_filtered = []
    min_corr_value_list = []
    receivers = []
    #try :
    for z,n in enumerate(nodes):
        #multiply transmit fft by transfer function to node of interest
        fft_out = rf.fft_transfer(
                dme_tx.get_filtered_fft(),
                tx_node.phy_port_voltage(),
                n.phy_port_voltage())

        rx = dme_receiver(n, dme_tx, imgDir)
        receivers.append(rx)

        #rx.add_filter("hpf",500e3,1)
        #rx.add_filter("lpf",15e6,1)
        #rx.add_filter("lpf",30e6,1)
        rx.rx_fft(fft_out)
        rx.output_filter_to_file()
        rx.output_t_domain_to_file()

        #insert new rx object here...
        #run correlations 
        #hold eye data - show more than one eye (one for MDI eye
        #diagram, one for rxfilter eye, another for correlated eye

        ################################################################################
        #these two functions overwrite some object variables that the other one sets
        #like min_corr_value.  
        #right now the order matters, maybe fix this in the future
        #rx.process_mdi_data()
        rx.process_filtered_data()
        ################################################################################

        min_corr_value_list.append(rx.min_corr_value)
        #eye_data_mdi.append(rx.eye_mdi)
        eye_data_filtered.append(rx.eye_filtered)
        rx_filter_png = os.path.join("data",design_md5,"img","rx_filter_%d.png" % rx.node.number) 
        rx.plot_filter(rx_filter_png,title="rx_filter - Node %d" % rx.node.number)

    print("Sampling Period: %.3fns" % (1/Fs*1e9))
    #except Exception as e:
    #    print(e)
    #    print("issues generating eye diagram")

    if(0): #optionally save dme ffts from different nodes (right now set to be the last node, but dont trust comments too much!)
        node_save = -1 #-1 means the last node
        pspec_plot.set_ylabel('DME Output Spectrum')  # Add an y-label to the axes.
        pspec_plot.plot(dme_tx.fft_freq, 20*np.log10(np.absolute(fft_out_list[node_save])),color=color_array[node_save])
        config['plot_png'] = os.path.join("data",design_md5,"img",config['plot_png_filename']) 
        plt.savefig(config['plot_png'])

    #saturation_level is the histogram / heatmap level that makes the heatmap eyediagrams saturate color.
    #Without this, the eye diagram gets normalized to the largest bin. This makes the sparse data hard to see.
    #The level is automatically set to 1/2 the zero crossing bin height of the input dme signal
    #saturation_index = int(eye_data[0].nbins/2)
    #saturation_level = np.amax(eye_data[0].heatmap[int(eye_data[0].nbits/2)][eye_data[0].index1:eye_data[0].index2])/3
    saturation_index = 0
    saturation_level = eye_data_filtered[0].zero_crossing_array[0]/3
    print("Saturation_level (%d): %d" % (saturation_index, saturation_level))

    eye1 = []
    eye2 = []
    cross1 = []
    cross2 = []
    delay = []
    cross_time = []
    cross_time_min  = []
    cross_time_max  = []

    #for e in eye_data_mdi:
    #    e.plot_eye(saturation_level=saturation_level) #plot the 2d histogram
    for e in eye_data_filtered:
        e.plot_eye(saturation_level=saturation_level) #plot the 2d histogram
        #e.plot_slice() #plot the zero crossing slice from the 2d histogram
        eye1.append(e.eye_area_1*1e9)
        eye2.append(e.eye_area_2*1e9)
        cross1.append(e.crossing1_width*1e9)
        cross2.append(e.crossing2_width*1e9)
        delay.append(e.t_offset*1e9)
        cross_time.append(e.crossing_time*1e9)
        cross_time_min.append(e.crossing_time_min*1e9)
        cross_time_max.append(e.crossing_time_max*1e9)

    fig2, eye_plots = plt.subplots(2,2, figsize=(10, 10))  # Create a figure and an axes.
    fig2.canvas.manager.set_window_title(" ".join(sys.argv))
    eps = (eye_plots[0][0], eye_plots[0][1],
           eye_plots[1][0], eye_plots[1][1])

    eps[0].set_xlabel("Attach Point (m)")
    eps[0].set_ylabel("Eye Opening Area (V*ns)")
    eps[0].plot(trunk.attach_points, eye1  , 'o', label="eye1")
    eps[0].plot(trunk.attach_points, eye2  , 'o', label="eye2")
    eps[0].legend()

    eps[1].set_xlabel("Attach Point (m)")
    eps[1].set_ylabel("Zero Cross Widths (ns)")
    eps[1].plot(trunk.attach_points, cross1, 'o')
    eps[1].plot(trunk.attach_points, cross2, 'o')

    eps[2].set_xlabel("Attach Point (m)")
    eps[2].set_ylabel("Min Correlation Value")
    eps[2].set_ylim([0,1])
    eps[2].plot(trunk.attach_points, min_corr_value_list , 'o')
    eps[2].plot([trunk.attach_points[0],trunk.attach_points[-1]], [0.55,0.55] , '-')

    eps[3].set_xlabel("Attach Point (m)")
    eps[3].set_ylabel("Zero Cross Time (ns)")
    eps[3].plot(trunk.attach_points, cross_time_max , 'o', label='max')
    eps[3].plot(trunk.attach_points, cross_time     , 'o', label='mean')
    eps[3].plot(trunk.attach_points, cross_time_min , 'o', label='min')
    eps[3].legend()

    config['corr_png'] = os.path.join("data",design_md5,"img",config['corr_png_filename'])
    plt.savefig(config['corr_png'])

    print("Compiling Gif")
    import imageio.v2 as imageio
    if(0):
        config['eye_gif_mdi'] = 'eye_mdi.gif'
        loop = []
        for e in eye_data_mdi:
            loop.append(e.imgfile)
        for e in reversed(eye_data_mdi):
            loop.append(e.imgfile)

        images = []
        gif_file = os.path.join("data",design_md5,"img",config['eye_gif_mdi'])
        for filename in loop:
            images.append(imageio.imread(filename))
        imageio.mimsave(gif_file, images)

    loop = []
    for e in eye_data_filtered:
        loop.append(e.imgfile)
    for e in reversed(eye_data_filtered):
        loop.append(e.imgfile)

    images = []
    config['eye_gif_filtered'] = 'eye_filtered.gif'
    gif_file = os.path.join("data",design_md5,"img",config['eye_gif_filtered'])
    for filename in loop:
        images.append(imageio.imread(filename))
    imageio.mimsave(gif_file, images)


    ################################################################################
    # End Eye Diagram Generation
    ################################################################################

    ################################################################################
    # Generate HTML output
    ################################################################################
    print("Generating .html report")
    writeHtml(config, eye_data_filtered, np.amin(min_corr_value_list))
    ################################################################################
    # End Eye Diagram Generation
    ################################################################################

    if not config['noplot']:
        #print("#Close plot window to continue")
        #plt.show()
        plt.close()

    fig, rl_plot = plt.subplots(1,1, figsize=(9, 2))  # Create a figure and an axes.
    rl_limit = return_loss_limit(frequency[0])
    il_limit = insertion_loss_limit(frequency[0])
    rl_plot.xaxis.set_major_formatter(EngFormatter(unit = 'Hz'))
    rl_plot.plot(frequency[0], rl_limit, label="clause 147 limit")  
    rl_plot.plot(frequency[0], s11_plot[0], label="test", color='k')  
    rl_plot.set_ylabel('RL (dB)')  
    rl_plot.set_xlim([0,xmax])
    rl_plot.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=2)  # Add a legend.
    if(config['noautoscale']):
        rl_plot.set_ylim([-70,10])

    plt.savefig('rl_plot.png')
    plt.close(fig)

