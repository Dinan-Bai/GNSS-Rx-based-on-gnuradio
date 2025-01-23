from scipy.signal import firwin
import numpy as np

# Parameters
fs = 16367600          # Input sampling rate (Hz)
decimation_factor = 4
output_fs = fs / decimation_factor
cutoff = fs/4       # Cutoff frequency (Hz)
transition_width = 200e3  # Transition band (Hz)
num_taps = 101       # Number of filter taps (adjust as needed)

# Normalized cutoff frequency (as a fraction of Nyquist frequency)
nyquist_rate = fs / 2
normalized_cutoff = cutoff / nyquist_rate

# Design the FIR low-pass filter
taps = firwin(num_taps, normalized_cutoff, window="hamming")

# Print or save the taps
print("Filter Taps:", taps)
