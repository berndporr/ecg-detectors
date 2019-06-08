import numpy as np
import matplotlib.pyplot as plt
import pathlib
from ecgdetectors import Detectors
import random

current_dir = pathlib.Path(__file__).resolve()

unfiltered_ecg_dat = np.loadtxt("example_data/k2.tsv") 
unfiltered_ecg = unfiltered_ecg_dat[:, 2]
fs = 250
e = 0

detectors = Detectors(fs)

r_peaks = detectors.two_average_detector(unfiltered_ecg)
#r_peaks = detectors.matched_filter_detector(unfiltered_ecg)
#r_peaks = detectors.swt_detector(unfiltered_ecg)
#r_peaks = detectors.engzee_detector(unfiltered_ecg)
#r_peaks = detectors.christov_detector(unfiltered_ecg)
#r_peaks = detectors.hamilton_detector(unfiltered_ecg)
#r_peaks = detectors.pan_tompkins_detector(unfiltered_ecg)

for i in range(len(r_peaks)):
    r_peaks[i] = r_peaks[i] + (random.random()-0.5)*e

hr = [(j-i)*(1.0/fs)*60 for i, j in zip(r_peaks[:], r_peaks[1:])]

plt.subplot(211)
plt.plot(hr)

plt.subplot(212)

f = np.fft.fft(hr)
f = np.abs(f)
f[0] = 0
plt.plot(f)

plt.show()
