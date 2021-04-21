Description of gif files and how to recreate them

git repository:
	https://github.com/SPE-MD/SPMD-Simulations/

gif generation is done in the gifmaker folder in the git repository
python scripts in the gifmaker repository call cmodel.py in a loop, then compile the output into a gif


drop_length.gif
Description:
	50m mixing segment, 16 nodes, vary drop length between 0 and 0.5m
Command:
	python drop_length.py


vary_l_16n.gif
Description:
	100m mixing segment, 16 nodes, vary trunk length between 16m and 100m
Command:
	python vary_l_16n.py


vary_l_32n.gif
Description:
	100m mixing segment, 32 nodes, vary trunk length between 16m and 100m
Command:
	python vary_l_32n.py


vary_cap.gif
Description:
    50m mixing segment, 16 nodes, mdi capcatitance (cnode) varying between 1pF and 30pF
Command:
    python vary_cap.py


vary_nodes.gif
Description:
    50m mixing segment, vary the number of nodes between 2 and 32
Command:
    python vary_nodes.py


tx_position.gif
Description:
    50m mixing segment, 16 nodes, vary the transmitter position between node 1 thru node 16
Command:
    python tx_position.py


gauss_attach.gif
Description:
    50m mixing segment, 16 nodes, vary the exact position of nodes with gaussian distribution
    sigma=10cm
Command:
    python gauss_16.py


random_16n_50m.gif
Description:
    50m mixing segment, 16 nodes, trunk attachment and transmitter positions are random
Command:
    python random_16n_50m.py


random_32n_50m.gif
Description:
    100m mixing segment, 32 nodes, trunk attachment and transmitter positions are random
Command:
    python random_32n_50m.py

