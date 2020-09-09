#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from hrv import HRV
from ecgdetectors import Detectors
import scipy.stats as stats
import sys
from ecg_gudb_database import GUDb

# for plotting max hflf ratio
hflfmax = 10

# example subject for the spectra
subj = 1

if len(sys.argv) > 1:
    subj = int(sys.argv[1])

sitting_class = GUDb(subj, 'sitting')
hrv_class = HRV(sitting_class.fs)
lfhf = hrv_class.fAnalysis(sitting_class.anno_cs)
print("Subject sitting: lf/hf=",lfhf)

fig = plt.figure()
fig.suptitle('Subject sitting doing nothing')
# in time
plt.title("Sitting")
plt.subplot(211)
plt.plot(hrv_class.t_hr_linear,hrv_class.hr_linear)
plt.plot(hrv_class.t_hr_discrete,hrv_class.hr_discrete,"x")
plt.xlabel("t/seconds")
plt.ylabel("heartrate/Hz")

# now the Fourier spectrum
plt.subplot(212)
plt.plot(hrv_class.f_hr_axis,hrv_class.f_hr)
plt.ylim([0,0.3])
plt.xlabel("f/Hz")
plt.ylabel("power")


sitting_class = GUDb(subj, 'maths')
hrv_class = HRV(sitting_class.fs)
lfhf = hrv_class.fAnalysis(sitting_class.anno_cs)
print("Subject doing math test: lf/hf=",lfhf)

fig = plt.figure()
fig.suptitle('Subject sitting doing a math test')
# in time
plt.title("Math test")
plt.subplot(211)
plt.plot(hrv_class.t_hr_linear,hrv_class.hr_linear)
plt.plot(hrv_class.t_hr_discrete,hrv_class.hr_discrete,"x")
plt.xlabel("t/seconds")
plt.ylabel("heartrate/Hz")

# now the Fourier spectrum
plt.subplot(212)
plt.plot(hrv_class.f_hr_axis,hrv_class.f_hr)
plt.ylim([0,0.3])
plt.xlabel("f/Hz")
plt.ylabel("power")

plt.show()
