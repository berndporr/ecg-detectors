import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from hrv import HRV
from ecgdetectors import Detectors

path_gu_ecg_database = '../dataset_716'

import sys
sys.path.insert(0, path_gu_ecg_database + r'/example_code')
from ecg_gla_database import Ecg


data_path = path_gu_ecg_database + r'/experiment_data'

maths_rr_sd = []
maths_error_rr_sd = []

sitting_rr_sd = []
sitting_error_rr_sd = []

total_subjects = 25
subject = []

for i in range(total_subjects):
#for i in range(3):
    print(i)
    sitting_class = Ecg(data_path, i, 'sitting')
    sitting_class.filter_data()
    maths_class = Ecg(data_path, i, 'maths')
    maths_class.filter_data()

    detectors = Detectors(sitting_class.fs)

    if sitting_class.anno_cs_exists and maths_class.anno_cs_exists:
        subject.append(i)

        hrv_class = HRV(sitting_class.fs)

        r_peaks = detectors.swt_detector(sitting_class.einthoven_II)
        sitting_rr_sd.append(hrv_class.RMSSD(r_peaks))
        r_peaks = detectors.swt_detector(maths_class.einthoven_II)
        maths_rr_sd.append(hrv_class.RMSSD(r_peaks))

        sitting_error_rr = detectors.two_average_detector(sitting_class.einthoven_II)
        sitting_error_rr_sd.append(hrv_class.RMSSD(sitting_error_rr))

        maths_error_rr = detectors.two_average_detector(maths_class.einthoven_II)
        maths_error_rr_sd.append(hrv_class.RMSSD(maths_error_rr))


subject = np.array(subject)
width = 0.2

fig, ax = plt.subplots()
rects1 = ax.bar(subject, sitting_rr_sd, width)
rects2 = ax.bar(subject + width, maths_rr_sd, width)
rects3 = ax.bar(subject+(2*width), sitting_error_rr_sd, width)
rects4 = ax.bar(subject+(3*width), maths_error_rr_sd, width)

ax.set_ylabel('SDNN (s)')
ax.set_xlabel('Subject')
ax.set_title('HRV for sitting and maths test')
ax.set_xticks(subject + width)
ax.set_xticklabels(subject)
ax.legend((rects1[0], rects2[0], rects3[0], rects4[0]), ('sitting (SWT)', 'maths (SWT)', 'sitting (AVG)', 'math (AVG)' ))

plt.figure()

# now let's do stats with no error

avg_sitting_rr_sd = np.average(sitting_rr_sd)
sd_sitting_rr_sd = np.std(sitting_rr_sd)

avg_maths_rr_sd = np.average(maths_rr_sd)
sd_maths_rr_sd = np.std(maths_rr_sd)

plt.bar([0,1],[avg_sitting_rr_sd,avg_maths_rr_sd],yerr=[sd_sitting_rr_sd,sd_maths_rr_sd],align='center', alpha=0.5, ecolor='black', capsize=10)
plt.ylim([0,100])
plt.title("WAVELET")

t,p = stats.ttest_rel(sitting_rr_sd,maths_rr_sd)

print("WAVELET: p=",p," that both distributions are equal.")

plt.figure()

# and stats with error

avg_sitting_error_rr_sd = np.average(sitting_error_rr_sd)
sd_sitting_error_rr_sd = np.std(sitting_error_rr_sd)

avg_maths_error_rr_sd = np.average(maths_error_rr_sd)
sd_maths_error_rr_sd = np.std(maths_error_rr_sd)

plt.bar([0,1],[avg_sitting_error_rr_sd,avg_maths_error_rr_sd],yerr=[sd_sitting_error_rr_sd,sd_maths_error_rr_sd],align='center', alpha=0.5, ecolor='black', capsize=10)
plt.ylim([0,100])
plt.title("TWO AVG DETECTOR")

t,p = stats.ttest_rel(sitting_error_rr_sd,maths_error_rr_sd)

print("TWO AVG DETECTOR: p=",p," that both distributions are equal.")

plt.show()
