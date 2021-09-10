from __future__ import print_function
from __future__ import absolute_import

from pprint import pprint

import argparse
import os.path

from MultiDropTopologySpreadsheetImport import MultidropSimulationNetwork
from MultiDropTopologySpreadsheetImport import CableSegmentModelConfig
from MultiDropTopologySpreadsheetImport import MultiDropSimulationNodeConfig

from ConsensusModelSimulator import ConsensusModelSimulationResult


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='802.3da MultiDrop Network Simulation Consensus Model Launcher',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

       
    parser.add_argument('topology_xlsx_file_path', type=str, \
            metavar='path'+os.path.sep+'to'+os.path.sep+'topology_file.xlsx',
            help='Path to Excel (xlsx) file that defines the network topology.\
                  See MultiDropTopologySampleInput.xlsx for the input format.'\
            )
    
    args = parser.parse_args()
    
    if (os.path.exists(args.topology_xlsx_file_path)):
        network = MultidropSimulationNetwork(args.topology_xlsx_file_path);
        print(network)
    else:
        print ("Error: Specified topology xlsx file path %s is invalid\n" % args.topology_xlsx_file_path)
        parser.print_help()
        exit()

    #below is conceptual, implementation ongoing
    sim = ConsensusModelSimulator()
    
    sim.network = network
    
    sim.run()

    simulationResult = sim.getResults()

    plotter = ConsensusModelPlotter()

    plotter.results = simulationResult

    plotter.generatePlots()