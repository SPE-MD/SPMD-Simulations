from __future__ import print_function
from __future__ import absolute_import

from pprint import pprint

import collections 

from openpyxl import load_workbook

class MultiDropSimulationNodeConfig(object):
    """Contains a single node from a multidrop network"""
    def __init__(self, nodeConfig):
        self.NodeIndex      = nodeConfig["NodeIndex"]
        self.NodeModel      = nodeConfig["NodeModel"]
        self.TeeModel       = nodeConfig["TeeModel"]
        self.StubCableModel = nodeConfig["StubCableModel"]
        self.StubLength     = nodeConfig["StubLength"]
        self.LineCableModel = nodeConfig["LineCableModel"]
        self.LineLength     = nodeConfig["LineLength"]

    def __str__(self):
        returnString =  "\nNodeConfig\n"
        returnString += "NodeIndex:       %d\n" % self.NodeIndex 
        returnString += "NodeModel:       %s\n" % self.NodeModel 
        returnString += "TeeModel:        %s\n" % self.TeeModel 
        returnString += "StubCableModel:  %s\n" % self.StubCableModel 
        returnString += "StubLength:      %f\n" % self.StubLength 
        returnString += "LineCableModel:  %s\n" % self.LineCableModel 
        returnString += "LineLength:      %f\n" % self.LineLength 
        return returnString



class CableSegmentModelConfig(object):
    """Contains a single cable model parameter set for a given base model"""
    def __init__(self, cableSegConfig):
        self.CableBaseModel = cableSegConfig["CableBaseModel"]
        self.CableModelKey  = cableSegConfig["CableModelKey"]
        self.Vendor         = cableSegConfig["Vendor"]
        self.Model          = cableSegConfig["Model"]
        self.Gauge          = cableSegConfig["Gauge"]
        self.SegmentSize    = cableSegConfig["SegmentSize"]
        self.Rcable         = cableSegConfig["Rcable"]
        self.Lcable         = cableSegConfig["Lcable"]
        self.Ccable         = cableSegConfig["Ccable"]
        self.TransferFunc   = cableSegConfig["TransferFunc"]
    
    def __str__(self):
        returnString =  "\nCableModel\n"
        returnString += "CableBaseModel: %s\n" % self.CableBaseModel
        returnString += "CableModelKey:  %s\n" % self.CableModelKey
        returnString += "Vendor:         %s\n" % self.Vendor
        returnString += "Model:          %s\n" % self.Model
        returnString += "Gauge:          %d\n" % self.Gauge
        returnString += "SegmentSize:    %f\n" % self.SegmentSize
        returnString += "Rcable:         %f\n" % self.Rcable
        returnString += "Lcable:         %f\n" % self.Lcable
        returnString += "Ccable:         %f\n" % self.Ccable
        returnString += "TransferFunc:   %s\n" % self.TransferFunc
        return returnString

class MultidropSimulationNetwork(object):
    """Contains an entire multidrop network model consisting of sveral nodes and cable 
    configureations."""
    def __init__(self, excelFileName):
        self.nodeConfigs = []
        self.cableSegConfigs = {}
        wb = load_workbook(excelFileName, data_only=True)

        sheet = wb['Cables']
        cableSegConfigDictList = sheetToListOfDictsKeyedByHeaderRow(sheet, 0)
        for cableSegConfigDict in cableSegConfigDictList:
            self.appendCableModelConfig(CableSegmentModelConfig(cableSegConfigDict))

        sheet = wb['Networks']

        nodeConfigDictList = sheetToListOfDictsKeyedByHeaderRow(sheet, 0)

        for nodeConfig in nodeConfigDictList:
            self.appendNodeConfig(MultiDropSimulationNodeConfig(nodeConfig))
    
    def __str__(self):
        returnString = "MultiDropSimulationNetwork\n"
        returnString += "Node Configs:\n"
        for nodeConfig in self.nodeConfigs:
            returnString += str(nodeConfig)
        
        returnString += "Cable Segment Configs:\n"
        for cableSegConfigKey in self.cableSegConfigs.keys():
            returnString += str(self.cableSegConfigs[cableSegConfigKey])
        return returnString



    def appendNodeConfig(self, nodeConfig):
        """Appends a node config to the list of nodes"""
        self.nodeConfigs.append(nodeConfig)

    def appendCableModelConfig(self, cableSegConfig):
        """Add a cable model to the dict that stores them by their unique CableModelKey"""
        self.cableSegConfigs[cableSegConfig.CableModelKey] = cableSegConfig

    def getStubCableModelForNodeConfig(self, nodeConfig):
        """Retrieve a cable model from  the dict that stores them by their unique CableModelKey for stubs"""
        return self.cableSegConfig[nodeConfig.StubCableModel]

    def getLineCableModelForNodeConfig(self, nodeConfig):
        """Retrieve a cable model from  the dict that stores them by their unique CableModelKey for lines"""
        return self.cableSegConfig[nodeConfig.LineCableModel]


def sheetToListOfDictsKeyedByHeaderRow(sheet, headerRowNumber=0):
    """Creates a list of ordered dicts using the header row of a worksheet as the keys.
    Note header row number is zero-based, thus 0 is the default for top row header."""
    sheetList = []
    rowDict = collections.OrderedDict()

    headerRow = [header.value for header in list(sheet.rows)[headerRowNumber]]
    for row in list(sheet.rows)[headerRowNumber+1:]:
        for (colNumber, cell) in enumerate(row):
            rowDict[headerRow[colNumber]] = cell.value
        sheetList.append(rowDict)
        rowDict = {}

    return sheetList

if __name__ == '__main__':
    
    network = MultidropSimulationNetwork("MultiDropTopologySampleInput.xlsx");
    print(network)


