#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import pathlib
from hrv import HRV
from ecgdetectors import Detectors
import scipy.stats as stats

path_gu_ecg_database = '../dataset_716'
data_path = path_gu_ecg_database + r'/experiment_data'

import sys
sys.path.insert(0, path_gu_ecg_database + r'/example_code')
from ecg_gla_database import Ecg

# for plotting max hflf ratio
hflfmax = 10

# example subject for the spectra
subj = 1

if len(sys.argv) > 1:
    subj = int(sys.argv[1])

sitting_class = Ecg(data_path, subj, 'sitting')
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


sitting_class = Ecg(data_path, subj, 'maths')
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
