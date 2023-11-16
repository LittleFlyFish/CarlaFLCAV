import pandas as pd
import numpy as np
from scipy.signal import coherence
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from scipy.fftpack import dct



def PlotFour(data_2d, data_3d):
    # Get column names
    columns = data_2d.columns
    # Create a grid of subplots
    fig, axs = plt.subplots(len(columns), 1, figsize=(10, len(columns) * 5))

    # Create a subplot for each column
    for i, column in enumerate(columns):
        axs[i].plot(data_2d[column], color='blue', label='2d data')
        axs[i].plot(data_3d[column], color='orange', label='3d data')
        axs[i].set_title(column)
        axs[i].legend()

    # Display the figure
    plt.tight_layout()
    plt.show()

def Calculation(A, B):
    # Compute the correlation
    correlation = A.corr(B)

    print(f"The correlation between A and B for {column} is {correlation}")
    # Get the time series
    A_cos = A.values.reshape(1, -1)
    B_cos = B.values.reshape(1, -1)

    # Compute the cosine similarity
    cos_sim = cosine_similarity(A_cos, B_cos)[0, 0]

    print(f"The cosine similarity between A and B for {column} is {cos_sim}")

    # Compute the FFT
    A_fft = np.fft.fft(A)
    B_fft = np.fft.fft(B)

    # Compute the phases
    A_phase = np.angle(A_fft)
    B_phase = np.angle(B_fft)

    # Compute the correlation of the phases
    correlation = np.corrcoef(A_phase, B_phase)[0, 1]

    print(f"The correlation between phases of A and B for {column} is {correlation}")

    # Get the time series
    A_cos = A_phase.reshape(1, -1)
    B_cos = B_phase.reshape(1, -1)

    # Compute the cosine similarity
    cos_sim = cosine_similarity(A_cos, B_cos)[0, 0]
    print(f"The cosine similarity between the phase of A and B for {column} is {cos_sim}")
    # Compute the amplitude spectrum
    A_amp = np.abs(A_fft)
    B_amp = np.abs(B_fft)

    # Compute the cosine similarity
    cos_sim = cosine_similarity([A_amp], [B_amp])[0, 0]
    print(f"The cosine similarity between the amplitude spectra of A and B for {column} is {cos_sim}")
    A_dct = dct(A.values)
    B_dct = dct(B.values)
    correlation = np.corrcoef(A_dct, B_dct)[0, 1]

    print(f"The correlation between DCT A and DCT B for {column} is {correlation}")
    # Get the time series
    A_cos = A_dct.reshape(1, -1)
    B_cos = B_dct.reshape(1, -1)

    # Compute the cosine similarity
    cos_sim = cosine_similarity(A_cos, B_cos)[0, 0]

    print(f"The cosine similarity between DCT A and DCT B for {column} is {cos_sim}")



    return 0


# Load first five lines of data
data_2d = pd.read_csv("2d.txt", delim_whitespace=True, nrows=151)
data_3d = pd.read_csv("3d.txt", delim_whitespace=True, nrows=151)

PlotFour(data_2d, data_3d)



for i in range(4):
    # Choose a column to analyze
    column = data_2d.columns[i]
    # Get the time series
    A = data_2d[column]
    B = data_3d[column]
    Calculation(A, B)

