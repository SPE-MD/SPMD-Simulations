# ADI Consensus Model Readme

This model will reproduce simulation results displayed in SPMD_Potterf_Paul_Consensus_Mixing_Segment_Model_2021-03-24.pdf

## Install
After pulling the git repot, go to the ADI_model folder and execute:


```
PS C:\users\username\git\SPMD-Simulations\ADI_model> pipenv install
Pipfile.lock (16c839) out of date, updating to (24b969)...
Locking [dev-packages] dependencies...
Locking [packages] dependencies...
 Locking...Building requirements...
Resolving dependencies...
Success!
Updated Pipfile.lock (24b969)!
Installing dependencies from Pipfile.lock (24b969)...
  ================================ 10/10 - 00:00:17
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.

PS C:\users\username\git\SPMD-Simulations\ADI_model> pipenv shell
Launching subshell in virtual environment...
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows
```

In addition to the Python libraries required by the core script, LTSpice is also reqiured.


## Run Model with Defaults
```
PS C:\Users\username\git\SPMD-Simulations\ADI_model> python cmodel.py
```

## Run Model with Options
```python cmodel.py [options]```

## Run Model with Multiple Options Specified at Command Line
```python cmodel.py --seed=144704 --nodes=32 --length=100 --separation_min=1 --drop_max=0.10 --cnode=3e-11```

## Output
An HTML file with graphical results will be produced and automatically opened.

## Command Line Help
```
python cmodel.py --help
usage: cmodel.py [-h] [--nodes NODES] [--random_attach] [--start_pad START_PAD] [--end_pad END_PAD] [--start_attach START_ATTACH]
                 [--end_attach END_ATTACH] [--length LENGTH] [--segments_per_meter SEGMENTS_PER_METER] [--drop_max DROP_MAX]
                 [--random_drop] [--separation_min SEPARATION_MIN] [--lcomp LCOMP] [--cnode CNODE] [--lpodl LPODL] [--rnode RNODE]
                 [--seed SEED] [--tx_node TX_NODE] [--noplot] [--plot_png_filename PLOT_PNG_FILENAME] [--noautoscale]
                 [--attach_error ATTACH_ERROR] [--fft FFT] [--attach_points ATTACH_POINTS [ATTACH_POINTS ...]] [--json JSON]

802.3da network model generator

optional arguments:
  -h, --help            show this help message and exit
  --nodes NODES         Set the number of nodes in the simulation (default: None)
  --random_attach       When set, nodes will attached at random locations on the mixing segment after nodes specified by
                        --start_attach and --end_attach flags have been added to the mixing segment (if any). Node placements should
                        be reproducible by reusing the seed value from another sim (see the --seed flag) Otherwise, nodes will be
                        evenly distributed across the mixing segment between nodes specified by --start_attach and --end_attach
                        flags (default: False)
  --start_pad START_PAD
                        Specify the distance between start of cable and the 1st node (default: None)
  --end_pad END_PAD     Specify the distance between end of cable and the last node (default: None)
  --start_attach START_ATTACH
                        Specify an number of nodes to be placed at the start of the mixing segment with 'separation_min' spacing
                        (default: None)
  --end_attach END_ATTACH
                        Specify an number of nodes to be placed at the end of the mixing segment with 'separation_min' spacing
                        (default: None)
  --length LENGTH       Mixing segment length in meters, will be rounded to an integer number of segments per meter (default: None)
  --segments_per_meter SEGMENTS_PER_METER
                        Size of finite element cable model segments. Be sure this lines up with lump models (default: None)
  --drop_max DROP_MAX   Drop length between mixing segment and PD attachment in meters. This number will be rounded to an interger
                        number of segments per meter (default: None)
  --random_drop         When set, node drop length will be chosen at random between zero and drop_max. Drop lengths should be
                        reproducible by reusing the seed value from another sim (see the --seed flag) Otherwise, drop lengths will
                        be evenly distributed across the mixing segment (default: False)
  --separation_min SEPARATION_MIN
                        Minimum separation between nodes in meters. This number will be rounded to an integer number of segments per
                        meter (default: None)
  --lcomp LCOMP         Compensation inductance added to tconnector ports (default: None)
  --cnode CNODE         Node capacitance in Farads. All nodes will be assigned this MDI interface capacitance (default: None)
  --lpodl LPODL         Node inducatnce in Henrys. All nodes will be assigned this MDI interface inductance (default: None)
  --rnode RNODE         Node resistance in Ohms. All nodes will be assigned this MDI interface resitance (default: None)
  --seed SEED           Seed value for random number generator (default: None)
  --tx_node TX_NODE     Set the transmitter node. (default: None)
  --noplot              set this flag to prevent plotting (default: False)
  --plot_png_filename PLOT_PNG_FILENAME
                        Filename for plot image output as a .png file. Default is zcable.png (default: None)
  --noautoscale         set this flag to lock the y-axis on IL/RL plots to -80dB/-70dB respectively. The xaxis on the network model
                        will be locked at -1m to 101m (default: False)
  --attach_error ATTACH_ERROR
                        add gaussian error to attachment points. Pass the the sigma value of the attachment error or 0 for no error.
                        Ignored for randomly placed nodes. Ifattach_error is set to a large value, can separation_min be violated?I
                        don't know (default: None)
  --fft FFT             fft of and input signal in text form to be multiplied against the insertion loss then ifft is applied to
                        reconstruct the time domain signal shape (default: None)
  --attach_points ATTACH_POINTS [ATTACH_POINTS ...]
                        specify the mixing segment attachment points with a space separated list --nodes is overridden by the length
                        of this list. Make sure this list is ordered (default: None)
  --json JSON           specify a json file containing a system description (default: None)
```
