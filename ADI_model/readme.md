Consensus Model Readme
This model will reproduce simulation results displayed in SPMD_Potterf_Paul_Consensus_Mixing_Segment_Model_2021-03-24.pdf

run:
python cmodel.py [options]
to simulate the mixing segment

run:
python --help 
for a list of options 

Example:
python cmodel.py --seed=144704 --nodes=32 --length=100 --separation_min=1 --drop_max=0.10 --cnode=3e-11

Output:
A graph window will pop up

CSV File Output:
zcable.csv
column 1 is the frequency
columns 4 and 5 are RL/IL respectively
columns 2 and 3 are used for calibration of the model in certain situations, please ignore them
