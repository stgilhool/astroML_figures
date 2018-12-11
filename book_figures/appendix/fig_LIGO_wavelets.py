"""
LIGO wavelet transform
----------------------
"""
# Author: Jake VanderPlas
# License: BSD
#   The figure produced by this code is published in the textbook
#   "Statistics, Data Mining, and Machine Learning in Astronomy" (2013)
#   For more information, see http://astroML.github.com
#   To report a bug or issue, use the following forum:
#    https://groups.google.com/forum/#!forum/astroml-general
import numpy as np
from matplotlib import pyplot as plt

from astroML.datasets import fetch_LIGO_bigdog
from astroML.fourier import FT_continuous, IFT_continuous

#----------------------------------------------------------------------
# This function adjusts matplotlib settings for a uniform feel in the textbook.
# Note that with usetex=True, fonts are rendered with LaTeX.  This may
# result in an error if LaTeX is not installed on your system.  In that case,
# you can set usetex to False.
if "setup_text_plots" not in globals():
    from astroML.plotting import setup_text_plots
setup_text_plots(fontsize=8, usetex=True)


def wavelet(t, t0, f0, Q):
    return (np.exp(-(f0 * (t - t0) / Q) ** 2)
            * np.exp(2j * np.pi * f0 * (t - t0)))


def wavelet_FT(f, t0, f0, Q):
    # this is its fourier transform using
    # H(f) = integral[ h(t) exp(-2pi i f t) dt]
    return (np.sqrt(np.pi) * Q / f0
            * np.exp(-2j * np.pi * f * t0)
            * np.exp(-(np.pi * (f - f0) * Q / f0) ** 2))


def check_funcs(t0=1, f0=2, Q=3):
    t = np.linspace(-10, 10, 10000)
    h = wavelet(t, t0, f0, Q)

    f, H = FT_continuous(t, h)
    assert np.allclose(H, wavelet_FT(f, t0, f0, Q))

X = fetch_LIGO_bigdog()
t = X['t']
h = X['Hanford']

dt = t[1] - t[0]

Q = np.sqrt(22)
f0 = 1

f0 = 2 ** np.linspace(5, 8, 50)

f, H = FT_continuous(t, h)
W = np.conj(wavelet_FT(f, 0, f0[:, None], Q))

t, HW = IFT_continuous(f, H * W)

t = t[::100]
HW = HW[:, ::100]

fig = plt.figure(figsize=(5, 3.75))
plt.imshow(abs(HW), origin='lower', aspect='auto',
           extent=[t[0], t[-1], np.log2(f0[0]), np.log2(f0[-1])])
plt.colorbar()
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(1))
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, *args:
                                                      "%i" % (2 ** x)))
plt.show()
