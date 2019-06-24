# Heartrate variability python example code

These are Python scripts which calculate both
timedomain and frequency domain HRV parameters.
In particular the timedomain paramter here is
normalised RMSSD and the frequency domain paramter
is LF/HF being the most popular ones.

In order to run the script you need to down the open
access database:

http://researchdata.gla.ac.uk/716/

## ECG viewing

To view the ECGs of a single subject run:

```
plot_ecg.py <subject number>
```

## Timedomain stats

Tests if a math tests has less normalised rRMSSD than just sitting
on a chair:

```
hrv_time_domain_analysis.py
```

## Frequency stats

Tests if a math tests has less LF/HF ratio than just sitting
on a chair:

```
hrv_frequency_domain_analysis.py
```
