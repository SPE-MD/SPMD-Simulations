#ADI Consensus Model Readme

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

## Display Help
```python cmodel.py --help ```

## Run Model with Multiple Options Specified at Command Line
```python cmodel.py --seed=144704 --nodes=32 --length=100 --separation_min=1 --drop_max=0.10 --cnode=3e-11```

## Output
An HTML file with graphical results will be produced and automatically opened.
