# Overview

This folder contains code developed by Rockwell Automation, primarily during the development of IEEE 802.3cg. The results from this code have been published in several IEEE presentations, including:
https://www.ieee802.org/3/cg/public/Mar2018/brandt_cg_01a_0318.pdf
https://www.ieee802.org/3/cg/public/Sept2018/griffiths_3cg_01a_0918.pdf
https://www.ieee802.org/3/cg/public/May2019/griffiths_3cg_01b_0519.pdf

The primary code is in the root Rockwell_Automation directory. It is meant to be run manually using the LTSpice GUI, specifically using the Multidrop_Bus.asc file. The two Python files have the following functions:
* generate_waveform.py - Generates a differential Manchester encoded (DME) input signal – a text file containing time/voltage pairs – to be used as an input to LTSpice.
* eye_diagram.py - Provides time-domain analysis in the form of an eye diagram. It can import either LTSpice tab-separated .txt data or LTSpice .raw files. Nota bene: it expects the traces to be called V(RXn+,RXn-), where n = 1, 2, 3... The V() parentheses mean it is a differential voltage measured between two LTSpice nodes, RXn+ and RXn-, at a single MDI.

Workflow goes as follows:
1. Generate posDME.dat and negDME.dat piece-wise linear (PWL) files using `python generate_waveform.py`. Default is to generate a PRBS-7 bit sequence.
2. Open Multidrop_Bus.asc using LTSpice. Modify the circuit and run parameters and run in the LTSpice GUI. The transceiver (Transceiver.asc) will automatically use the posDME.dat and negDME.dat files. Plotting is already set up using Multidrop_Bus.plt. From the plot window, export data to text (tab-separated) using `File > Export data as text`, keeping the default file name (Multidrop_Bus.txt).
3. Post-process the data using `python eye_diagram.py`; it will automatically look for Multidrop_Bus.txt.
