"""
micro_reflections.py
.. moduleauthor:: Scott Griffiths <stgriffi@ra.rockwell.com>

Based on original Matlab code by Ragnar Jonsson found at:
https://www.ieee802.org/3/cy/public/adhoc/jonsson_3cy_01_03_23_21.m

and described in:
https://www.ieee802.org/3/cy/public/adhoc/jonsson_3cy_01_03_23_21.pdf

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


def micro_reflections(f, s11, N_bins, N_seg, N_discard, df_nonstandard=0):
    """
    Evaluates micro-reflections.

    Args:
        f -- a list of frequencies
        s11 -- S11 scattering parameters
        N_bins -- the number of time domain bins used in the calculation
        N_discard -- the number of segments to discard when computing REM and ETM

    The parameter df_nonstandard can be used if the frequency sampling
    of s11 is not according to specification. It defaults to 0.

    Returns:
        REM -- residual echo metric
        ETM -- echo tail metric
        h_echo -- impulse response computed from inverse FFT
        sort_ix -- sorting indicies that can be applied to sort P_k
        P_k -- power in each time bin

    Note: sort_ix will differ from the Matlab code by 1 because Matlab arrays
    are indexed from 1, whereas Python (numpy) arrays are indexed from zero.

    Version 1.1 -- March 23, 2021
    """
    # number of samples to use
    K_N = N_bins * N_seg
    N_samples = 2*K_N   # even number of samples

    # experimental code to convert non-standard frequency sampling to standard
    if df_nonstandard == 0:
        fq = np.array(f)
        sq = np.array(s11)
    else:
        fq = df_nonstandard * np.arange(0, K_N+1)
        sq = cr_spline(f, s11, fq)

    # calculate echo impulse response and power
    h_echo = impulse_response_f2t(sq, fq, N_samples)

    # find power in each time bin
    h2 = h_echo**2
    P_k = np.zeros(N_bins)
    m1 = 0
    for n in range(N_bins):
        m0 = m1 + 1
        m1 = round((n+1)*N_seg)
        P_k[n] = np.mean(h2[(m0-1):m1]) * N_seg

    # find residual echo metric (REM)
    sort_ix = np.argsort(P_k)
    p_sort = P_k[sort_ix]
    sort_ix = sort_ix[::-1]
    p_sum = np.cumsum(p_sort)
    REM = 10*np.log10(p_sum[::-1])

    # find residual echo RE_k
    RE_k = P_k.copy()
    RE_k[sort_ix[:N_discard]] = 0

    # calculate echo tail metric (ETM)
    tmp = np.cumsum(RE_k[::-1])
    ETM = 10*np.log10(tmp[::-1])

    return [REM, ETM, h_echo, sort_ix, P_k]


def impulse_response_f2t(H, f, N):
    """
    Impulse (time) response for a given frequency response.

    Required Args:
        H -- the frequency response given at frequencies f
        f -- list of frequncies
        N -- the number of output samples (must be even)
    """
    H = np.array(H)
    N_H = H.size

    # test arguments
    if not all(np.isfinite(aa).flatten()):
        raise ValueError('Signal has invalid samples')

    nonuniform_spacing = np.sum(np.abs(np.diff(np.abs(np.diff(f)))))
    if abs(nonuniform_spacing) > 1e-6:
        raise ValueError('Spacing of frequency points is not uniform')

    if f[0] != 0:
        raise ValueError('Frequency list does not start at DC (0 Hz)')

    # re-shape arguments
    E_k = H.flatten()
    f = f.flatten()
    assert len(E_k) == len(f)

    # adjust phase of frequency response
    K_N = math.ceil(N/2)

    # SG: commented lines below are not needed for correct execution
    # ang_N = np.angle(E_k[K_N])
    # x0 = ang_N / np.pi
    # xq = np.arange(K_N + 1) / K_N / 2
    # E_k = E_k * np.exp(-1j*2*np.pi*x0*xq)[0]
    # # what original Matlab code does:
    # # E_k = np.outer(E_k, np.exp(-1j*2*np.pi*x0*xq))
    # # E_k = E_k.flatten()

    E_k[0] = np.real(E_k[0])
    H_k = np.concatenate((
        E_k[:K_N],
        [np.real(E_k[K_N])],
        np.conj(E_k[K_N-1:0:-1])
    ))

    # find impulse response from inverse FFT
    h_n = np.real(np.fft.ifft(H_k))
    return h_n


def cr_spline(x, y, xq):
    """
    Catmull-Rom spline: s = cr_ spline(x, y, xq)
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
