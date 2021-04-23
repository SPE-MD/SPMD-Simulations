"""
eye_diagram.py

This module imports time-domain waveform data from LTSpice, either from .raw
files or as tab-separated text.

A sub-interval of the DME waveform (usually 1 bit in, from both the start and
stop) is then fitted to identify zero crossings. The waveform is then folded
with a fixed 80 ns period to generate eye diagrams.

Two types of eye diagrams are generated: one for each node, and a "composite"
eye diagram that is the sum of the individual eye diagrams from all nodes.
The latter is used to quickly identify a "worst-case" eye opening.

The eye opening is also automatically computed at the mid-point (40 ns).

.. moduleauthor:: Scott Griffiths <stgriffi@ra.rockwell.com>
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from scipy.optimize import brentq, minimize
from scipy.interpolate import interp1d, UnivariateSpline
import sys
import os
import re


def import_tab_data(fname):
    """
    Imports tab-separated data exported directly from LTSpice.
    These data files are formatted as follows:

    time	V(RX1+,RX1-)	V(RX2+,RX2-)
    0.000000000000000e+000	0.000000e+000	0.000000e+000
    3.000000000000000e-008	0.000000e+000	0.000000e+000
    3.000078890637637e-008	-1.136868e-013	0.000000e+000
    """
    df = pd.read_table(fname)
    df['time'] *= 1e9   # convert to ns
    df = df.set_index('time')

    rename_dict = {}
    ncolumns = len(df.columns) + 1
    for i in range(1, ncolumns):
        rename_dict['V(RX{0}+,RX{0}-)'.format(i)] = 'Node {0}'.format(i)
    df.rename(columns=rename_dict, inplace=True)
    return df


def import_raw_data(fname):
    """Imports LTSpice .raw files containing n-column voltage data."""
    header = 1
    columns = []
    regex = re.compile('V\((rx.+)\)')
    with open(fname, 'r') as f:
        for line in f:
            if 'Values:' in line:
                break
            match = regex.search(line)
            if match:
                columns.append(match.group(1))
            header += 1
    df = pd.read_table(fname, skiprows=header, names=['Index', 'V', 'Time'])
    stride = int(len(df)/len(df['Index'].dropna()))
    assert stride == len(columns) + 1

    table = [df.iloc[::stride]['Time']]
    for i in range(len(columns)):
        table.append(df.iloc[(i+1)::stride]['V'])
    table = np.transpose(table)
    df = pd.DataFrame(table, columns=(['time'] + columns))
    for i in range(int(len(columns)/2)):
        dV = 'V(RX{0}+, RX{0}-)'.format(i + 1)
        Vp = 'rx{0}+'.format(i + 1)
        Vm = 'rx{0}-'.format(i + 1)
        df[dV] = df[Vp] - df[Vm]
        df.drop([Vp, Vm], axis=1, inplace=True)
    rename_dict = {}
    ncolumns = len(df.columns) + 1
    for i in range(1, ncolumns):
        rename_dict['V(RX{0}+, RX{0}-)'.format(i)] = 'Node {0}'.format(i)
    df.rename(columns=rename_dict, inplace=True)
    df['time'] *= 1e9   # convert to ns
    df.set_index('time', inplace=True)
    return df


def node_id_from_name(node_name):
    """Extracts integer node ID from a string formatted as V(RX{0}+, RX{0}-)."""
    regex = re.compile('(\d+)')
    match = regex.search(node_name)
    if match:
        return int(match.group(1))
    else:
        raise ValueError('Node name %s does not match regex' % node_name)


def derivative(x, y, order=1):
    """Returns the n-th order derivative of (x, y) data."""
    dy = y.copy()
    for n in range(order):
        dy[:-1] = np.diff(y) / np.diff(x)
        dy[-1] = (y[-1] - y[-2])/(x[-1] - x[-2])
        y = dy.copy()
    return dy


def find_start(x, y):
    """
    Old algorithm for computing folding window; not very sophisticated.

    Attempts to find the first falling edge of the waveform and fit a line
    to this edge. The x-intercept is interpreted as the start point for folding.

    This algorithm does not take into account information regarding the positions
    of the other zeros in the waveform; consequently, it produces an inferior fit.
    Moreover, it does not compute the stopping point; the folding algorithm thus
    relies on a rather crude calculation of the stop point in _compute_start_stop.
    However, it is simple and relatively robust.
    """
    # find first falling edge
    falling_edges = np.where(np.diff(y) < 0)[0]
    first_falling = []
    amplitude = (max(y) - min(y))/2
    for i in range(len(falling_edges) - 1):
        if falling_edges[i+1] - falling_edges[i] == 1:
            first_falling.append(falling_edges[i])
        else:
            # check if we have captured the first edge
            accept1 = len(first_falling) > 20
            accept2 = (max(y[first_falling]) - min(y[first_falling])) > amplitude/2
            if accept1 or accept2:
                break
            else:                         # we have captured a wiggle, retry
                first_falling = []

    # find points within 10% and 90% of falling edge
    y_falling = np.array(y[first_falling])
    amp = np.min(y_falling)   # use min because signal is negative
    idx = np.where((y_falling < 0.1*amp) & (y_falling > 0.9*amp))[0]
    if idx.size:
        first_falling = np.array(first_falling)[idx]
    else:
        print(first_falling)
        plt.plot(x, y, marker='o')
        plt.plot(x[falling_edges], y[falling_edges], 'ko')
        plt.show()
        first_falling = np.array(first_falling)

    # fit line to falling edge to find x-intercept, x0
    m, b = np.polyfit(x[first_falling], y[first_falling], 1)
    x0 = -b/m
    return x0


class Eye_Diagram:
    """
    Class to compute Eye Diagrams, which are generated by folding a voltage vs.
    time waveform by the symbol period.

    This class can create two types of eye diagrams:
    1) A "multi" plot containing eye diagrams for each individual node.
    2) A "combined" plot containing the overlaid eye diagrams for all nodes.

    The simulation parameters are set as class parameters and should be adjusted
    before using this class.
    """
    # simulation parameters
    symbol_rate_MHz = 12.5
    period_ns = 1/(symbol_rate_MHz*1e6)*1e9
    transition_time_ns = 20
    signal_amp_V = 0.5   # NOTE: CHANGE to 1.5 FOR 2.4 V
    num_bits = 16

    def __init__(self, df, plot=True):
        """
        Constructor.
        Expects a Pandas DataFrame from import_tab_data() or import_raw_data().
        """
        self.data = df
        self._compute_start_stop()
        if plot:
            self.plot_folded()

    def _compute_start_stop(self):
        """
        Determine the start and stop locations for the folded eye diagrams.
        This is done by calling _find_fold_region() for each node.

        The results are stored as [start, stop] in self.node_start_stop_dict.
        """
        self.node_start_stop_dict = {}
        for node in self.data.columns:
            x = self.data.index
            y = self.data[node].values
            try:
                start, stop = self._find_fold_region(x, y)
            except ValueError:
                print(" --> %s: value error, using legacy fold region algorithm" % node)
                start, stop = self._find_fold_region_old(x, y, node)
            if stop - start < max(x) / 2:   # noisy data; use old algorithm
                print(" --> %s: range error, using legacy fold region algorithm" % node)
                print("    ", start, stop)
                start, stop = self._find_fold_region_old(x, y, node)
            self.node_start_stop_dict[node] = [start, stop]

    def _find_fold_region_old(self, x, y, node):
        # print(" --> %s: Using legacy fold region algorithm" % node)
        start = find_start(x, y) + self.period_ns + self.transition_time_ns/2
        stop = start + (self.num_bits - 2)*self.period_ns
        return start, stop

    def _find_fold_region(self, x, y):
        """
        Algorithm for finding folding region.

        The algorithm operates as follows:
        1) Use the first derivative to locate regions around zeros (roots).
        2) Convert these regions into intervals around zeros.
        3) Use a root-finding algorithm (brentq) to find zeros.
        4) Remove DME 'ones'; keep only zeros associated with DME zeros.
        5) Use a minimizer to find the optimal window with the known period.
        """
        # use first derivative to locate areas around zeros (roots)
        spl = UnivariateSpline(x, y, k=1, s=1)   # k=1 -> linear interp, s=1 -> slight smoothing
        dfdx = spl.derivative()
        dy = dfdx(x)
        max_dy = max(dy)
        derivative_thresh = max_dy/3
        zero_regions = np.where(abs(dy) > derivative_thresh)[0]

        # compute intervals, each of which should surround a single zero
        min_gap_size = 50
        gaps = np.where(np.diff(zero_regions) > min_gap_size)[0]
        interval_edges = [0] + list(gaps) + list(gaps + 1) + [len(zero_regions)-1]
        interval_edges.sort()
        intervals = list(zip(zero_regions[interval_edges[0::2]],
                             zero_regions[interval_edges[1::2]]))

        # use brentq to compute exact zeros, using calculated intervals
        f = interp1d(x, y)
        zeros = []
        for a,b in intervals:
            try:
                x0 = brentq(f, x[a], x[b])
                zeros.append(x0)
            except ValueError:
                pass   # the interval does not contain a zero

        # remove zeros that are from DME 'ones'
        while True:
            ones = np.where(np.diff(zeros) < 0.75*self.period_ns)[0]
            if ones.size > 1:
                zeros.pop(ones[1])
            elif ones.size == 1:   # last bit is a DME 'one'
                zeros.pop(-1)
            else:
                break

        # cost function to minimize; squared deviation of zeros
        def cost(x0, x):
            sum_squared = 0
            for i in range(len(zeros)):
                # handle zeros near edge of waveform
                if x0 + i*self.period_ns > max(x):
                    break
                sum_squared += f(x0 + i*self.period_ns)**2
            return sum_squared

        # minimize deviation so that period matches data as well as possible
        res = minimize(cost, zeros[0], args=(x))
        x0 = res.x[0]

        limit = 0
        while x0 + limit*self.period_ns <= max(x):
            limit += 1
        fit_zeros = np.array([x0 + i*self.period_ns for i in range(limit)])
        return fit_zeros[0], fit_zeros[-1]

    def plot_unfolded(self, node=1, show_start_stop=True):
        """
        Plot unfolded voltage vs. time waveform for a given node (default=1).

        show_start_stop determines whether vertical red lines are overlaid on
        the plot to indicate the folding region that will be used.
        """
        x = self.data.index
        y = self.data['Node %d' % node].values
        plt.axhline(0, color='black', linestyle='--')
        if show_start_stop:
            start, stop = self.node_start_stop_dict['Node %d' % node]
            plt.axvspan(0, start, color='red', alpha=0.1)
            plt.axvline(start, color='red')
            plt.axvspan(stop, max(x), color='red', alpha=0.1)
            plt.axvline(stop, color='red')
        plt.plot(x, y)
        plt.xlabel('Time / ns')
        plt.ylabel('Receiver Signal / V')
        plt.xlim(0, max(x))
        plt.tight_layout()
        plt.show()

    def plot_derivative(self, node=1, order=1):
        """
        Plots the n-th order derivative of the unfolded data. This is mostly
        useful for development and diagnostic work.

        Note that derivatives with order > 2 will likely be unusable because
        of numerical error; the way the derivative is computed by this function
        is very crude.
        """
        x = self.data.index
        y = self.data['Node %d' % node].values
        dy = derivative(x, y, order)
        plt.plot(x, dy)
        plt.xlabel('Time / ns')
        if order == 1:
            plt.ylabel('$dV/dt$')
        else:
            plt.ylabel('$d^{0}V/dt^{0}$'.format(order))
        plt.xlim(0, max(x))
        plt.tight_layout()
        plt.show()
        y = self.data['Node %d' % node].values
        return x, y, dy

    def fold_data(self, node_name):
        """
        Folds the data for a given node (node_name = a column in self.data).

        Returns a list of traces, which are curves on the interval from zero to
        self.period_ns. During plotting, each of these traces must be plotted
        individually in order to avoid plotting lines connecting the curve at
        the end of the period with the beginning.

        By analogy, this algorithm "lifts the pen off of the paper" when moving
        from the end of the period to the start.
        """
        x = self.data.index
        y = self.data[node_name].values
        start, stop = self.node_start_stop_dict[node_name]
        mask = np.where((x >= start) & (x <= stop))[0]
        x = x[mask]
        y = y[mask]
        x -= start
        x = x % self.period_ns

        trace = []
        trace_list = []
        for i in range(len(x) - 1):
            if i > 0 and x[i] < x[i-1]:
                trace_list.append(trace)
                trace = []
                y0 = np.interp(
                    x=0,
                    xp=[x[i-1] - self.period_ns, x[i]],
                    fp=[y[i-1], y[i]]   # y points
                )
                trace.extend([[0, y0], [x[i], y[i]]])
            if i < len(x) - 2 and x[i] > x[i+1]:
                y0 = np.interp(
                    x=self.period_ns,
                    xp=[x[i], x[i+1] + self.period_ns],
                    fp=[y[i], y[i+1]]   # y points
                )
                trace.extend([[x[i], y[i]], [self.period_ns, y0]])
            else:
                trace.append([x[i], y[i]])
        if trace:   # append any final, leftover trace
            trace_list.append(trace)
        return trace_list

    def plot_folded(self, show_openings=True, save=True):
        """
        Creates three types of plots using folded traces computed by fold_data():
        1) A "combined" plot containing the overlaid eye diagrams for all nodes.
        2) A "multi" plot containing eye diagrams for each individual node.
        3) A "trend" plot showing the eye openings for each node.

        The plots are saved in the current working directory as:
        1) combined_eye_diagram.png
        2) multi_eye_diagram.png
        3) multi_eye_trend.png

        This plot function is combined so that the folded traces only need to be
        computed once (the computation is time consuming).
        """
        node_trace_list = []
        for node_name in self.data.columns:
            node_traces = self.fold_data(node_name)
            node_trace_list.append(node_traces)
        self.plot_combined(node_trace_list, show_openings, save)
        self.plot_multi(node_trace_list, save)
        self.plot_multi_trend(node_trace_list, save)

    def plot_combined(self, node_trace_list, show_openings=True, save=True):
        """
        Creates a "combined" plot containing overlaid eye diagrams for all nodes.
        """
        combined_fig = plt.figure()
        combined_ax = combined_fig.gca()
        for node_traces in node_trace_list:
            for trace in node_traces:
                combined_ax.plot(*np.array(trace).T, color='blue', alpha=0.1)
        if show_openings:
            opening_times = [(1/4)*self.period_ns, (3/4)*self.period_ns]
            y_upper, y_lower = self.compute_eye_opening(node_trace_list, details=True)
            for i in range(2):
                eye_opening = y_upper[i] - y_lower[i]
                combined_ax.annotate(
                    '',
                    xy=(opening_times[i], y_upper[i]),
                    xytext=(opening_times[i], y_lower[i]),
                    arrowprops=dict(arrowstyle='<->', shrinkA=0, shrinkB=0)
                )
                combined_ax.text(
                    x=(opening_times[i] + self.period_ns/100),
                    y=0,
                    s='{:.0f} mV'.format(eye_opening * 1000),
                    verticalalignment='center'
                )
        combined_ax.yaxis.set_minor_locator(AutoMinorLocator(5))
        combined_ax.set_xlabel('Time / ns')
        combined_ax.set_ylabel('Voltage / V')
        combined_ax.set_ylim(-1.5*self.signal_amp_V, 1.5*self.signal_amp_V)
        combined_fig.tight_layout()
        if save:
            combined_fig.savefig('combined_eye_diagram.png', dpi=200)
            plt.close(combined_fig)
        else:
            return combined_fig

    def plot_multi(self, node_trace_list, save=True):
        """
        Creates a "multi" plot containing eye diagrams for each individual node.
        """
        default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        color_cycle = len(default_colors)
        number_of_nodes = node_id_from_name(self.data.columns[-1])
        ncols = 10
        nrows = int(np.ceil(number_of_nodes/ncols))
        multi_fig, axes = plt.subplots(
            nrows=nrows,
            ncols=ncols,
            sharey=True,
            gridspec_kw={'wspace': 0}
        )
        axes = axes.flatten()
        height = 4*nrows + 1
        multi_fig.set_size_inches(w=22, h=height, forward=True)   # ANSI size C

        for node_name, node_traces in zip(self.data.columns, node_trace_list):
            i = node_id_from_name(node_name) - 1
            color = default_colors[i % color_cycle]
            for trace in node_traces:
                axes[i].plot(*np.array(trace).T, color=color, alpha=0.5)
            axes[i].yaxis.set_minor_locator(AutoMinorLocator(5))
            axes[i].set_title('Node {0}'.format(i + 1))
            axes[i].set_xlabel('Time / ns')
            axes[i].set_ylim(-1.5*self.signal_amp_V, 1.5*self.signal_amp_V)
            if i % ncols == 0:
                axes[i].set_ylabel('Voltage / V')
        multi_fig.tight_layout()
        for i in range(nrows*ncols - number_of_nodes + 1):   # fix x-ticks in blank plots
            axes[-i].plot([0, 80], [0, 0], alpha=0)
        if save:
            multi_fig.savefig('multi_eye_diagram.png', dpi=200)
            plt.close(multi_fig)
        else:
            return multi_fig

    def plot_multi_trend(self, node_trace_list, save=True):
        """Creates a "trend" plot containing eye openings vs. node number."""
        x = np.arange(1, node_id_from_name(self.data.columns[-1]) + 1)
        y = len(x)*[0]
        for i, node_name in enumerate(self.data.columns):
            j = node_id_from_name(node_name) - 1
            y[j] = self.compute_eye_opening(node_trace_list, node=i+1)
        fig = plt.figure()
        plt.plot(x, y, 'ko')
        plt.xlabel('Node Number')
        plt.ylabel('Eye Opening [mV]')
        plt.gca().xaxis.set_minor_locator(AutoMinorLocator(5))
        plt.gca().yaxis.set_minor_locator(AutoMinorLocator(5))
        plt.ylim(ymin=0)
        plt.tight_layout()
        if save:
            fig.savefig('multi_eye_trend.png', dpi=200)
            plt.close(fig)
        else:
            return x, y

    def compute_eye_opening(self, node_trace_list=None, node=None, details=False):
        """
        Computes the eye opening using list of traces for a set of nodes.

        node_trace_list is assumed to have the form:
            [[node 1 traces], [node 2 traces], ..., [node n traces]]
        If node=None, then all nodes will be used. If node is an integer, then
        the eye opening for only that node will be computed.

        The eye opening is calculated at 1/4 and 3/4 of self.period_ns.
        The minimum of these two openings is what is normally returned.

        If details=True, then the coordinates of the eye openings are returned
        with the following format:
            ([eye_1/4_upper, eye_3/4_upper], [eye_1/4_lower, eye_3/4_lower])
        """
        opening_times = [(1/4)*self.period_ns, (3/4)*self.period_ns]
        y_upper = np.array([4*self.signal_amp_V, 4*self.signal_amp_V])
        y_lower = np.array([-4*self.signal_amp_V, -4*self.signal_amp_V])
        if not node_trace_list:
            trace_list = []
            for node_name in self.data.columns:
                trace_list += self.fold_data(node_name)
        if node:
            node_trace_list = [node_trace_list[node-1]]
        for node_traces in node_trace_list:
            for trace in node_traces:
                x, y = np.transpose(trace)
                for i, x0 in enumerate(opening_times):
                    y0 = y[np.argmin(abs(x - x0))]
                    if y0 >= 0 and y0 < y_upper[i]:
                        y_upper[i] = y0
                    if y0 <= 0 and y0 > y_lower[i]:
                        y_lower[i] = y0
        if details:
            return y_upper, y_lower
        else:
            eye_opening = min(y_upper - y_lower)
            return eye_opening


if __name__ == '__main__':
    fname = 'Multidrop_Bus.txt'
    if len(sys.argv) == 2:
        fname = sys.argv[1]
    extension = os.path.splitext(fname)[1]
    importer_dict = {'.txt': import_tab_data, '.raw': import_raw_data}
    importer = importer_dict[extension]
    data = importer(fname)
    Eye_Diagram(data)
