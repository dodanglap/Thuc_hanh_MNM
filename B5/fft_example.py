import numpy as np
import matplotlib.pyplot as plotter
import tkinter as tk
from tkinter import Label, Entry, Button

# Function to plot the signals based on user input
def plot_signals():
    # Get user input from the entry fields
    signal1Frequency = float(entry_signal1.get())
    signal2Frequency = float(entry_signal2.get())
    filterFrequency = float(entry_filter.get())  # Frequency to keep
    
    # How many time points are needed, i.e., Sampling Frequency
    samplingFrequency = 100
    samplingInterval = 1 / samplingFrequency

    # Begin and end time period of the signals
    beginTime = 0
    endTime = 10

    # Time points
    time = np.arange(beginTime, endTime, samplingInterval)

    # Create two sine waves
    amplitude1 = np.sin(2 * np.pi * signal1Frequency * time)
    amplitude2 = np.sin(2 * np.pi * signal2Frequency * time)

    # Sum of both sine waves
    amplitude = amplitude1 + amplitude2

    # Create subplot
    figure, axis = plotter.subplots(4, 1)
    plotter.subplots_adjust(hspace=1)

    # Time domain representation for sine waves
    axis[0].set_title(f'Sine wave with a frequency of {signal1Frequency} Hz')
    axis[0].plot(time, amplitude1)
    axis[0].set_xlabel('Time')
    axis[0].set_ylabel('Amplitude')

    axis[1].set_title(f'Sine wave with a frequency of {signal2Frequency} Hz')
    axis[1].plot(time, amplitude2)
    axis[1].set_xlabel('Time')
    axis[1].set_ylabel('Amplitude')

    # Combined sine wave (time domain)
    axis[2].set_title(f'Sine wave with multiple frequencies ({signal1Frequency} Hz + {signal2Frequency} Hz)')
    axis[2].plot(time, amplitude)
    axis[2].set_xlabel('Time')
    axis[2].set_ylabel('Amplitude')

    # Frequency domain (Fourier Transform)
    fourierTransform = np.fft.fft(amplitude) / len(amplitude)  # Normalize amplitude
    frequencies = np.fft.fftfreq(len(amplitude), d=samplingInterval)

    # Band-pass filter: Keep only the frequency specified by the user
    tolerance = 0.1  # Allow for a slight range around the target frequency
    fourierTransform[np.abs(frequencies - filterFrequency) > tolerance] = 0

    # Inverse FFT to get filtered signal back in time domain
    filtered_amplitude = np.fft.ifft(fourierTransform * len(amplitude))

    # Plot frequency domain after applying filter
    axis[3].set_title(f'Filtered Fourier transform (keeping {filterFrequency} Hz only)')
    axis[3].plot(frequencies[:len(frequencies)//2], np.abs(fourierTransform[:len(fourierTransform)//2]))
    axis[3].set_xlabel('Frequency')
    axis[3].set_ylabel('Amplitude')

    # Show the plot
    plotter.show()

# Create the main window
window = tk.Tk()
window.title("Signal Plotter")

# Add labels and entry fields for Signal 1 Frequency
Label(window, text="Enter frequency for Signal 1 (Hz):").grid(row=0, column=0)
entry_signal1 = Entry(window)
entry_signal1.grid(row=0, column=1)

# Add labels and entry fields for Signal 2 Frequency
Label(window, text="Enter frequency for Signal 2 (Hz):").grid(row=1, column=0)
entry_signal2 = Entry(window)
entry_signal2.grid(row=1, column=1)

# Add labels and entry fields for Filtering Frequency
Label(window, text="Enter the frequency to filter out (Hz):").grid(row=2, column=0)
entry_filter = Entry(window)
entry_filter.grid(row=2, column=1)

# Add a button to trigger the plotting function
Button(window, text="Plot Signals", command=plot_signals).grid(row=3, column=1)

# Start the Tkinter event loop
window.mainloop()
