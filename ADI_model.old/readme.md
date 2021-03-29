Consensus Model Readme
This model will reproduce simulation results displayed in SPMD_Potterf_Paul_Consensus_Mixing_Segment_Model_2021-03-24.pdf

run:
python cmodel.py

to simulate the mixing segment
Change pd model in pd.p to reproduce different simulation results
Comment out lpodl in pd.p to remove power coupling inductance
Change Cnode in pd.p to simulate different Cnode values
Controls to sweep parameters of cable length, pd attachment points, drop length, and more will be included in future revisions

Example:
python cmodel.py

Output:
zcable.csv
column 1 is the frequency
columns 4 and 5 are RL/IL respectively
columns 2 and 3 are used for calibration of the model in certain situations, please ignore them
