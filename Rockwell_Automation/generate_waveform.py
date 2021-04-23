"""
generate_waveform.py

This module is designed to generate a differential Manchester encoded (DME)
signal from a bit string, which can be either randomly generated or manually
fixed.

The primary output is a pair of text files, posDME.dat and negDME.dat, in a
piece-wise linear format for LTSpice.

.. moduleauthor:: Scott Griffiths <stgriffi@ra.rockwell.com>
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator


def generate_random_bits(num_bits):
    """Returns a numpy array with N random bits."""
    return np.random.randint(2, size=num_bits)


def generate_ones(num_bits):
    """Returns a numpy array with N ones."""
    return np.ones(num_bits, dtype=np.int)


def invert(bits):
    """Returns the logical inversion of a sequence of bits."""
    return -bits + 1


def PRBS7(seed, repeat=False):
    """
    Generates a PRBS-7 pseudo-random binary sequence.
    Seed can be any number between 0x01 and 0x7F. Do not use zero.
    """
    if seed == 0:
        raise ValueError('PRBS seed must not be zero!')
    x = seed
    while True:
        bit = ((x >> 6) ^ (x >> 5)) & 1
        yield (x >> 6) & 1
        x = ((x << 1) | bit) & 0x7F
        if not repeat and x == seed:
            break


def PRBS17(seed):
    """
    Generates a pseudo-random binary sequence based on the polynomial
    x^17 + x^14 + 1 (also used for the 10BASE-T1S scrambler).

    Seed can be any number between 0x01 and 0x3FFF. Do not use zero.
    """
    if seed == 0:
        raise ValueError('PRBS seed must not be zero!')
    x = seed
    while True:
        bit = ((x >> 16) ^ (x >> 13)) & 1
        yield (x >> 16) & 1
        x = ((x << 1) | bit) & 0x3FFFF


class DME_Generator:
    """
    Class to generate differential Manchester encoded (DME) signals which can
    be used as inputs to Spice simulations.
    """
    def __init__(self, data, symbol_rate_MHz=12.5, transition_time_ns=20, tx_voltage=1.0, time_offset_ns=0):
        """
        Constructs a DME_Generator object and computes clock, data, and DME
        signal waveforms.

        The constructor also saves the output data to 'posDME.dat' and
        'negDME.dat', which correspond to the positive/negative differential
        Manchester encoded signals, in LTSpice format.

        Args:
            data               -- a list of bits, i.e., [1, 0, 1, 1]
            symbol_rate_MHz    -- the symbol/clock rate, in MHz (default: 12.5)
            transition_time_ns -- rise/fall time of signal, in ns (default: 20)
            tx_voltage         -- voltage at the transmitter, in V (default: 1)
            time_offset_ns     -- offset start time, in ns (default: 0)
        """
        self.data = data
        self.N = len(data)
        self.symbol_rate_MHz = symbol_rate_MHz
        self.period_ns = 1/(symbol_rate_MHz*1e6)*1e9
        self.transition_time_ns = transition_time_ns
        self.signal_voltage = tx_voltage
        self.time_offset_ns = time_offset_ns

        self.clock_bits = self._compute_clock_bits()
        self.data_bits = self._compute_data_bits()
        self.dme_bits = self._compute_dme_bits()
        self.save()

    def _compute_clock_bits(self):
        """Computes the bits that make up the clock signal."""
        clock = [0] + self.N*[1, 0]
        return np.array(clock)

    def _compute_data_bits(self):
        """Computes the bits that make up the data signal."""
        data_bits = [0] + [self.data[i//2] for i in range(2*self.N)]
        return np.array(data_bits)

    def _compute_dme_bits(self):
        """
        Computes the bits that make up the positive DME signal.

        The DME signal is generated following Clause 147.4.2 of IEEE Std 802.3cg-2019:
        a) A "clock transition" shall always be generated at the start of each bit.
        b) A "data transition" in the middle of a nominal bit period shall be
           generated if the bit to be transmitted is a logical '1'. Otherwise,
           no transition shall be generated until next bit.
        """
        dme_bits = np.ones(2*self.N + 1, dtype=np.int)
        for i in range(self.N):
            dme_bits[2*i+1] = not dme_bits[2*i]
            if self.data[i] == 0:
                dme_bits[2*i+2] = dme_bits[2*i+1]
            else:
                dme_bits[2*i+2] = not dme_bits[2*i+1]
        return dme_bits

    def _compute_waveform(self, bits):
        """
        Turns a set of bits (clock, signal, or DME) into a voltage vs. time
        waveform, which can then be saved or plotted.
        """
        N = len(bits)
        y = [bits[0]] + [bits[i//2] for i in range(2*N)]
        dt = self.period_ns/2
        delta = self.transition_time_ns / 2
        x = [0]
        x.extend([delta, dt])
        x.extend([dt + delta, 2*dt - delta])
        for i in range(2, N-1):
            x.extend([i*dt + delta, (i+1)*dt - delta])
        x.extend([(N-1)*dt + delta, N*dt - delta])
        x.extend([N*dt, (N+1)*dt])
        y.extend([0, 0])
        x = np.array(x)
        x[1:] += self.time_offset_ns
        y = np.array(y)
        y[:3] = 0
        return x, y

    def print_signals(self):
        """Prints the clock, data, and positive DME signals for debugging."""
        print('Data:', self.data)
        print('Clock Bits:', self.clock_bits)
        print('Data Bits: ', self.data_bits)
        print('DME Bits:  ', self.dme_bits)
        print('+DME Waveform:')
        x, y = self._compute_waveform(self.dme_bits)
        print('  ', x)
        print('  ', y)

    def save(self):
        """
        Writes the DME waveforms to file in LTSpice format, where each line of
        the file has the form: <time> <voltage>. For example,
            0n 0.0
            10n 2.4
            70n 2.4
            90n 0.0

        The files are called 'posDME.dat' and 'negDME.dat', and are saved
        in the current working directory.
        """
        tx_plus = self.signal_voltage*self.dme_bits
        tx_minus = self.signal_voltage*invert(self.dme_bits)
        output_names = ['posDME.dat', 'negDME.dat']
        for i, signal in enumerate([tx_plus, tx_minus]):
            x, y = self._compute_waveform(signal)
            with open(output_names[i], 'w') as f:
                for xx, yy in zip(x, y):
                    f.write("%dn %.1f\n" % (xx, yy))

    def dme_differential(self):
        tx_plus = self.signal_voltage*self.dme_bits
        tx_minus = self.signal_voltage*invert(self.dme_bits)
        dme = (tx_plus - tx_minus)/2   # 1/2 comes from termination voltage divider
        x, y = self._compute_waveform(dme)
        return x, y

    def plot(self, show_cells=True):
        """Plots the clock, data, +/-Tx, and DME signals on a single canvas."""
        fig, axes = plt.subplots(nrows=4, ncols=1, sharex=True)
        fig.set_size_inches(w=17, h=11, forward=True)   # ledger/tabloid
        axes[-1].set_xlabel('Time / ns')

        tx_plus = self.signal_voltage*self.dme_bits
        tx_minus = self.signal_voltage*invert(self.dme_bits)
        dme = (tx_plus - tx_minus)/2   # 1/2 comes from termination voltage divider
        signals = [self.clock_bits, self.data_bits, tx_plus, tx_minus, dme]
        signal_names = ['Clock', 'Data', '±Tx / V', 'DME Signal / V']
        dt = self.period_ns/2
        for i, signal in enumerate(signals):
            x, y = self._compute_waveform(signal)
            if i > 2:
                i -= 1   # plot -Tx signal on same canvas as +Tx
            axes[i].plot(x, y)
            axes[i].set_ylabel(signal_names[i])
            axes[i].set_xticks(np.arange(0, 2*(self.N + 1)*dt, dt))
            axes[i].set_xlim(0, 2*(self.N + 1)*dt)
            axes[i].xaxis.set_minor_locator(AutoMinorLocator(4))
        if show_cells:
            for i in range(self.N+1):
                for ax in axes:
                    ax.axvline(2*(i+1/2)*dt, color='black', alpha=0.25)
        plt.tight_layout(h_pad=0.1)
        plt.show()


if __name__ == '__main__':
    # example: fixed bit pattern
    # fixed = [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1]
    # dme = DME_Generator(fixed)

    # example: random bit pattern
    # random_data = generate_random_bits(128)
    # dme = DME_Generator(random_data)

    # example: PRBS-17 bit sequence
    # prbs_seed = 0x1234
    # sequence_length = 128
    # scrambler = PRBS17(prbs_seed)
    # prbs17 = [next(scrambler) for i in range(sequence_length)]
    # dme = DME_Generator(prbs17)

    prbs_seed = 0x7
    dme = DME_Generator(list(PRBS7(prbs_seed)))
    # dme.plot()
