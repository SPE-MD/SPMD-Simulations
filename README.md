# SPMD-Simulations
Repository to support simulations of mixing segments for single pair multi-drop networks to facilitate the selection of the proper mixing segment limits for IEEE 802.3da.

## Goals

The goal of these simulations is to provide a model which combines the best traits of each of the existing SPMD mixing segment models into one consensus model. This allows the broader group to do what-if experiments on a wider variety of network topologies.

### Desired Simulation Engine Features
* Simple Time/Frequency Domain Simulation (Done)
* Frequency Domain Simulation with Skin Effect (Done)
* Time/Frequency Domain Simulation with Skin Effect (In Progress)
* Fully Differential Time/Frequency Domain Simulation with Skin Effect (Planned)

### Desired Input Parameter Features
* Random topology generation (Done)
* Multiple topology batch execution framework (In Progress)
* Cable model variation capability (In Progress)
* PSE and PD modeling capability (Needs Planning)
* Connector modeling capability (Needs Planning)
* Stochastic connector and segment variation to reflect real-world systems (Planned)
* Dynamic segment length scaling (Planned)

### Desired Output Features
* Raw data export to csv (Done)
* Graph export with network topology visualization (Done)
* Overlayed results from batch analysis (Planned)
* Worst/Best case outcome extraction (Planned)

### Desired Configurations to Test
* Unloaded stubs
* Measure RL/IL from station to station (currently term to term)
* Dissimilar cables in trunk and in drop

## Simulation Tools

Front end automation is via Python 3. Some packaged are required:
* matplotlib
* numpy
* openpyxl (for future xlsx spreadsheet I/O features)

Most models here are based on LTSpice, which can be downloaded for free and carries a permissive license.
https://www.analog.com/en/design-center/design-tools-and-calculators/ltspice-simulator.html

