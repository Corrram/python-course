import matplotlib.pyplot as plt
import numpy as np


# 1: Sine wave example

x = np.linspace(0, 10, 100)
y = np.sin(x)

# add labels, title, grid and legend
plt.title("Sine Wave")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.grid()
plt.plot(x, y)
plt.legend(["sin(x)"], loc="upper right")
plt.show()

# 2: Multiple plots example

import numpy as np
import matplotlib.pyplot as plt

# Generate some sample data
t = np.linspace(0, 2*np.pi, 100)   # time
signal = np.sin(t)                 # sine wave
noise = np.random.randn(100) * 0.3 # some noise
freq = np.fft.fftfreq(len(t), d=(t[1]-t[0]))  # frequency domain
spectrum = np.abs(np.fft.fft(signal + noise))

# Create a figure with multiple axes
fig, ax = plt.subplots(2, 2, figsize=(8, 6))

# Time series plot
ax[0, 0].plot(t, signal + noise, label='Signal+Noise')
ax[0, 0].set_title('Time Domain')
ax[0, 0].set_xlabel('Time (s)')
ax[0, 0].set_ylabel('Amplitude')
ax[0, 0].legend()

# Frequency spectrum
ax[0, 1].plot(freq, spectrum, 'r-', label='Spectrum')
ax[0, 1].set_title('Frequency Domain')
ax[0, 1].set_xlabel('Frequency (Hz)')
ax[0, 1].set_ylabel('Magnitude')
ax[0, 1].legend()

# Scatter plot of measurements
x_data = np.random.rand(50)
y_data = np.random.rand(50)
ax[1, 0].scatter(x_data, y_data, c='g', alpha=0.6)
ax[1, 0].set_title('Measurements')
ax[1, 0].set_xlabel('X')
ax[1, 0].set_ylabel('Y')

# Empty plot or additional visualization
ax[1, 1].text(0.5, 0.5, 'More Plots Here', ha='center', va='center')
ax[1, 1].set_axis_off()

fig.tight_layout()
plt.show()