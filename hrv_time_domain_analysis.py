#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from hrv import HRV
from ecg_gudb_database import GUDb
import sys

maths_true = []
sitting_true = []

total_subjects = 25
subject = []

do_normalise = True

for i in range(total_subjects):
#for i in range(2):
    print(i)
    sitting_class = GUDb(i, 'sitting')
    sitting_class.filter_data()
    maths_class = GUDb(i, 'maths')
    maths_class.filter_data()

    if sitting_class.anno_cs_exists and maths_class.anno_cs_exists:
        subject.append(i)

        hrv_class = HRV(sitting_class.fs)

        maths_true_rr = maths_class.anno_cs
        maths_true.append(hrv_class.RMSSD(maths_true_rr,normalise = do_normalise))
        
        sitting_true_rr = sitting_class.anno_cs
        sitting_true.append(hrv_class.RMSSD(sitting_true_rr,normalise = do_normalise))


subject = np.array(subject)
width = 0.4

fig, ax = plt.subplots()
rects1 = ax.bar(subject+(0*width), sitting_true, width)
rects2 = ax.bar(subject+(1*width), maths_true, width)

ax.set_ylabel('nRMSSD')
ax.set_xlabel('Subject #')
ax.set_title('HRV for sitting and maths test')
ax.set_xticks(subject + width)
ax.set_xticklabels(subject)
ax.legend((rects1[0], rects2[0]), ('sitting', 'math' ))

avg_maths_true = np.average(maths_true)
sd_maths_true = np.std(maths_true)

avg_sitting_true = np.average(sitting_true)
sd_sitting_true = np.std(sitting_true)

fig = plt.figure()

plt.bar(['sitting','math'],
        [avg_sitting_true,avg_maths_true],
        yerr=[sd_sitting_true,sd_maths_true],
        align='center', alpha=0.5, ecolor='black', capsize=10)
plt.title("Sitting vs math")
plt.ylabel('nRMSSD')

t,p = stats.ttest_rel(maths_true,sitting_true)
print("Math vs sitting: p=",p)


plt.show()
