import numpy as np
import matplotlib.pyplot as plt
import pathlib
from hrv import HRV
import scipy.stats as stats

path_gu_ecg_database = '../dataset_716'
data_path = path_gu_ecg_database + r'/experiment_data'

import sys
sys.path.insert(0, path_gu_ecg_database + r'/example_code')
from ecg_gla_database import Ecg

# both ways 12.5 samples
jitter = 12.5

# example subject for the spectra
subj = 1

sitting_class = Ecg(data_path, subj, 'sitting')
r_peaks = sitting_class.anno_cs 

hrv_class = HRV(250)
lfhf = hrv_class.fAnalysis(r_peaks)
print("No jitter: lf/hf=",lfhf)

# in time
plt.title("Example for sitting (no error)")
plt.subplot(211)
plt.plot(hrv_class.t_hr_linear,hrv_class.hr_linear)
plt.plot(hrv_class.t_hr_discrete,hrv_class.hr_discrete,"x")

# now the Fourier spectrum
plt.subplot(212)
plt.plot(hrv_class.f_hr_axis,hrv_class.f_hr)
plt.ylim([0,0.3])

r_peaks = sitting_class.anno_cs

r_peaks = hrv_class.add_rr_error(r_peaks,10)

hrv_class = HRV(250)
lfhf = hrv_class.fAnalysis(r_peaks)
print("Jitter: lf/hf=",lfhf)

plt.figure()
# in time
plt.title("Example for sitting (with error)")
plt.subplot(211)
plt.plot(hrv_class.t_hr_linear,hrv_class.hr_linear)
plt.plot(hrv_class.t_hr_discrete,hrv_class.hr_discrete,"x")

# now the Fourier spectrum
plt.subplot(212)
plt.plot(hrv_class.f_hr_axis,hrv_class.f_hr)
plt.ylim([0,0.3])





maths_hf = []
maths_error_hf = []

sitting_hf = []
sitting_error_hf = []

total_subjects = 25
subject = []

for i in range(total_subjects):
#for i in range(3):
    print(i)
    sitting_class = Ecg(data_path, i, 'sitting')
    maths_class = Ecg(data_path, i, 'maths')

    if sitting_class.anno_cs_exists and maths_class.anno_cs_exists:
        subject.append(i)
        
        hrv_class = HRV(250)

        sitting_hf.append(hrv_class.fAnalysis(sitting_class.anno_cs))
        maths_hf.append(hrv_class.fAnalysis(maths_class.anno_cs))

        sitting_error_rr = hrv_class.add_rr_error(sitting_class.anno_cs, jitter)
        sitting_error_hf.append(hrv_class.fAnalysis(sitting_error_rr))

        maths_error_rr = hrv_class.add_rr_error(maths_class.anno_cs, jitter)
        maths_error_hf.append(hrv_class.fAnalysis(maths_error_rr))


subject = np.array(subject)
width = 0.2

fig, ax = plt.subplots()
rects1 = ax.bar(subject, sitting_hf, width)
rects2 = ax.bar(subject + width, maths_hf, width)
rects3 = ax.bar(subject+(2*width), sitting_error_hf, width)
rects4 = ax.bar(subject+(3*width), maths_error_hf, width)

ax.set_ylabel('fAnalysis (s)')
ax.set_xlabel('Subject')
ax.set_title('LF/HF ratio for sitting and maths test')
ax.set_xticks(subject + width)
ax.set_xticklabels(subject)
ax.legend((rects1[0], rects2[0], rects3[0], rects4[0]), ('sitting', 'maths', 'sitting with error', 'math with error' ))

plt.figure()

# now let's do stats with no error

avg_sitting_hf = np.average(sitting_hf)
sd_sitting_hf = np.std(sitting_hf)

avg_maths_hf = np.average(maths_hf)
sd_maths_hf = np.std(maths_hf)

plt.bar([0,1],[avg_sitting_hf,avg_maths_hf],yerr=[sd_sitting_hf,sd_maths_hf],align='center', alpha=0.5, ecolor='black', capsize=10)
plt.ylim([0,10])
plt.title("Without added error")

t,p = stats.ttest_rel(sitting_hf,maths_hf)

print("No error: p=",p," that both distributions are equal.")

plt.figure()

# and stats with error

avg_sitting_error_hf = np.average(sitting_error_hf)
sd_sitting_error_hf = np.std(sitting_error_hf)

avg_maths_error_hf = np.average(maths_error_hf)
sd_maths_error_hf = np.std(maths_error_hf)

plt.bar([0,1],[avg_sitting_error_hf,avg_maths_error_hf],yerr=[sd_sitting_error_hf,sd_maths_error_hf],align='center', alpha=0.5, ecolor='black', capsize=10)
plt.ylim([0,10])
plt.title("With added error of +/-"+str(jitter)+" samples")

t,p = stats.ttest_rel(sitting_error_hf,maths_error_hf)

print("Error: p=",p," that both distributions are equal.")




plt.show()
