import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

print("Running...")

# File path to the saved .npz file
filename = "delay_doppler_map_prn_4.npz"  # Replace with your file path

# Load the .npz file
data = np.load(filename)

# Extract data and parameters
delay_doppler_map = data['delay_doppler_map']
delay_range = data['delay_range']
delay_re = data['delay_re']
dopp_range = data['dopp_range']
dopp_re = data['dopp_re']

print(f"Loaded delay-doppler map with shape: {delay_doppler_map.shape}")

# Generate axis labels
delay_axis = np.arange(delay_range[0], delay_range[1], delay_re)

doppler_axis = np.arange(dopp_range[0], dopp_range[1], dopp_re)

# Compute the magnitude in dB
ddm_magnitude_db = 10 * np.log10(np.abs(delay_doppler_map))
ddm_magnitude_db[np.isinf(ddm_magnitude_db)] = -100  # Replace -inf with a low dB floor

# Find the peak in the DDM
peak_index = np.unravel_index(np.argmax(np.abs(delay_doppler_map)), delay_doppler_map.shape)
peak_delay = delay_axis[peak_index[0]]  # Delay corresponding to the peak
peak_doppler = doppler_axis[peak_index[1]]  # Doppler corresponding to the peak
peak_value = ddm_magnitude_db[peak_index]  # Magnitude in dB

print(f"Peak DDM Value: {peak_value:.2f} dB")
print(f"Corresponding Delay: {peak_delay} samples")
print(f"Corresponding Doppler: {peak_doppler} Hz")

# Create the 3D plot (First Window)
fig1 = plt.figure(figsize=(12, 8))
ax1 = fig1.add_subplot(111, projection='3d')
surf = ax1.plot_surface(
    *np.meshgrid(doppler_axis, delay_axis),  # Meshgrid for 3D plot
    ddm_magnitude_db,
    cmap='viridis',
    edgecolor='none'
)

# Customize the 3D plot
ax1.set_title("Delay-Doppler Map (3D View)")
ax1.set_xlabel("Doppler Shift (Hz)")
ax1.set_ylabel("Delay (samples)")
ax1.set_zlabel("Magnitude (dB)")
fig1.colorbar(surf, ax=ax1, label="Correlation Magnitude (dB)")

# Highlight the peak
ax1.scatter(peak_doppler, peak_delay, peak_value, color='red', s=50, label='Peak')
ax1.legend()

# Create the delay and Doppler cut plots (Second Window)
fig2, (ax2, ax3) = plt.subplots(2, 1, figsize=(10, 10))  # Two subplots in one figure

# Delay Cut: Magnitude vs Delay
delay_cut = ddm_magnitude_db[:, peak_index[1]]  # Extract the delay cut for the peak Doppler index
ax2.plot(delay_axis, delay_cut, label=f"Delay Cut at Doppler={peak_doppler:.2f} Hz", color='blue')
ax2.scatter([peak_delay], [peak_value], color='red', label='Peak', zorder=5)  # Highlight peak
ax2.set_title("Delay Cut (2D View)")
ax2.set_xlabel("Delay (samples)")
ax2.set_ylabel("Magnitude (dB)")
ax2.legend()
ax2.grid()

# Doppler Cut: Magnitude vs Doppler
doppler_cut = ddm_magnitude_db[peak_index[0], :]  # Extract the Doppler cut for the peak Delay index
ax3.plot(doppler_axis, doppler_cut, label=f"Doppler Cut at Delay={peak_delay:.2f} samples", color='green')
ax3.scatter([peak_doppler], [peak_value], color='red', label='Peak', zorder=5)  # Highlight peak
ax3.set_title("Doppler Cut (2D View)")
ax3.set_xlabel("Doppler Shift (Hz)")
ax3.set_ylabel("Magnitude (dB)")
ax3.legend()
ax3.grid()

# Adjust layout and show the plots
plt.tight_layout()
plt.show(block=True)  # Ensure the plot windows stay open
