#!/usr/bin/env python3
#coding=utf8
import matplotlib.pyplot as plt
import numpy as np

#x = np.linspace(0, 2, 100)
#
## Note that even in the OO-style, we use `.pyplot.figure` to create the figure.
#fig, ax = plt.subplots()  # Create a figure and an axes.
#ax.plot(x, x, label='linear')  # Plot some data on the axes.
#ax.plot(x, x**2, label='quadratic')  # Plot more data on the axes...
#ax.plot(x, x**3, label='cubic')  # ... and some more.
#ax.set_xlabel('x label')  # Add an x-label to the axes.
#ax.set_ylabel('y label')  # Add a y-label to the axes.
#ax.set_title("Simple Plot")  # Add a title to the axes.
#ax.legend()  # Add a legend.


x = np.linspace(0, 2, 100)

plt.plot(x, x, label='linear')  # Plot some data on the (implicit) axes.
plt.plot(x, x**2, label='quadratic')  # etc.
plt.plot(x, x**3, label='cubic')
plt.xlabel('x label')
plt.ylabel('y label')
plt.title("Simple Plot")
plt.legend()
plt.show()
