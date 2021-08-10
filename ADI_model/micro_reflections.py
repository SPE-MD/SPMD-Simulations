"""
micro_reflections.py
.. moduleauthor:: Scott Griffiths <stgriffi@ra.rockwell.com>

Based on original Matlab code by Ragnar Jonsson found at:
https://www.ieee802.org/3/cy/public/mar21/jonsson_3cy_01_03_16_21.m

and described in:
https://www.ieee802.org/3/cy/public/mar21/jonsson_3cy_01_03_16_21.pdf

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import numpy as np
import math


def ureflections_test_1(f, s11, f_s=14062500000, N_bins=512, L_bin=4, N_discard=12):
    """
    Evaluates micro-reflections.
    Args:
        f -- a list of frequencies
        s11 -- S11 scattering parameters
        N_bins -- the number of bins (default: 512)
        L_bin (default: 4)
        N_discard (default: 12)

    The function returns the metric value, residual, and h_echo.
    This function does not do any plotting.
    """
    # sampling interval and bin size
    T = 1/f_s    # sampling interval
    t_bin = L_bin * T
    t_max = N_bins * L_bin * T

    # number of samples and time vector
    N_samples = round(N_bins * L_bin) * 2   # even number of samples
    t = np.arange(N_samples) * T

    # calculate echo impulse response and power
    h_echo = cy_f2t(s11, f, T, N_samples)

    # find power in each time bin
    h2 = h_echo**2
    p_bin = np.zeros(N_bins)
    m1 = 0
    for n in range(N_bins):
        m0 = m1 + 1
        m1 = round((n+1)*L_bin)
        p_bin[n] = np.mean(h2[(m0-1):m1]) * L_bin

    # calculate effect of increasing number of bins
    p_sort = sorted(p_bin)
    p_sum = np.cumsum(p_sort)
    p_residual = p_sum[::-1]

    # convert to dB
    REM = 10*np.log10(p_residual[N_discard-1])
    return [REM, p_residual, h_echo]


def cy_f2t(H, f=None, T=1, N=256):
    """
    Impulse (time) response for a given frequency response.

    Required Args:
        H -- the frequency response given at frequencies f

    Keyword Args:
        f -- list of frequncies
        T -- the sampling interval
        N -- the number of output samples (must be even)
    """
    # find size
    H = np.array(H)
    NN = H.size

    # provide default frequency list, from 0 to pi
    if f is None:
        f = np.linspace(0, np.pi, num=NN)

    N2 = math.ceil(N/2)

    H = H.transpose().flatten()
    f = f.transpose().flatten()
    assert len(H) == len(f)

    # interpolate frequency response
    xq = np.linspace(0, 0.5, num=(N2 + 1))
    Hs1 = cr_spline(f*T, H, xq)
    ang_N = np.angle(Hs1[N2])
    x0 = ang_N / np.pi
    Hs1 = Hs1 * np.exp(-1j*2*np.pi*x0*xq)
    Hs = np.concatenate((
        [np.real(Hs1[0])],
        Hs1[1:N2],
        [np.real(Hs1[N2])],
        np.conj(Hs1[N2-1:0:-1])
    ))

    # find impulse response from inverse FFT
    h = np.real(np.fft.ifft(Hs))
    return np.roll(h, -1)


def cr_spline(x, y, xq):
    """
    Catmull-Rom spline
        s = cr_ spline(f*T,H,[0:N2]/N2/2)
    See more at https://en.wikipedia.org/wiki/Cubic_Hermite_spline
    """
    # initialize
    N_x = len(x)
    M_xq, N_xq = (1, len(xq))

    # reshape arguments
    x = x.transpose().flatten()
    y = y.transpose().flatten()
    xq = xq.transpose().flatten()

    # Catmull-Rom spline coefficients
    cr0 = np.array([0, 0, 1, 0])
    cr1 = np.array([0, 1, 0, -1])/2
    cr2 = np.array([-1, 4, -5, 2])/2
    cr3 = np.array([1, -3, 3, -1])/2

    # find closest points for x-values
    xm = (x[0:-1] + x[1:len(x)] - 1e-10)/2   # midpoints in interval
    reshape_xm = np.hstack([xm[:, np.newaxis] for i in range(len(xq))])
    reshape_xq = np.vstack([xq for i in range(len(xm))])
    m = np.argmin(abs(reshape_xm - reshape_xq), axis=0)
    u = (xq - x[m]) / (x[m+1] - x[m])

    # Use Farrow Structure to implement spline
    y0 = np.convolve(y, cr0)
    y1 = np.convolve(y, cr1)
    y2 = np.convolve(y, cr2)
    y3 = np.convolve(y, cr3)

    s = y3[m+2]*u**3 + y2[m+2]*u**2 + y1[m+2]*u + y0[m+2]
    return s
