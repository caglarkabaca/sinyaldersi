"""

Basic Statistics:
    Mean
    Variance
    Standard Deviation
    Signal Energy
    Root Mean Square (RMS)
    Peak-to-Peak Amplitude
    
Frequency Domain Analysis:
    Fast Fourier Transform (FFT)
    Power in different EEG frequency bands:
    Delta (0.5-4 Hz)
    Theta (4-8 Hz)
    Alpha (8-13 Hz)
    Beta (13-30 Hz)
    Gamma (30-100 Hz)

"""

import os
import numpy as np
import pandas as pd
from scipy import signal
from scipy.fft import fft, fftfreq
import glob

def read_file_data(file_path):
    with open(file_path, 'r') as f:
        return np.array([float(line.strip()) for line in f if line.strip()])

def calculate_fft(data, sampling_rate=1000):  # Assuming 1000 Hz sampling rate
    n = len(data)
    fft_result = fft(data)
    freqs = fftfreq(n, 1/sampling_rate)
    magnitude = np.abs(fft_result)
    return freqs[:n//2], magnitude[:n//2]  # Return only positive frequencies

def calculate_band_powers(freqs, magnitude):
    # Define EEG frequency bands
    delta_mask = (freqs >= 0.5) & (freqs <= 4)
    theta_mask = (freqs > 4) & (freqs <= 8)
    alpha_mask = (freqs > 8) & (freqs <= 13)
    beta_mask = (freqs > 13) & (freqs <= 30)
    gamma_mask = (freqs > 30) & (freqs <= 100)
    
    # Calculate power in each band
    delta_power = np.sum(magnitude[delta_mask]**2)
    theta_power = np.sum(magnitude[theta_mask]**2)
    alpha_power = np.sum(magnitude[alpha_mask]**2)
    beta_power = np.sum(magnitude[beta_mask]**2)
    gamma_power = np.sum(magnitude[gamma_mask]**2)
    
    return {
        'delta_power': delta_power,
        'theta_power': theta_power,
        'alpha_power': alpha_power,
        'beta_power': beta_power,
        'gamma_power': gamma_power
    }

def analyze_file(file_path):
    data = read_file_data(file_path)
    
    # Basic statistics
    stats = {
        'mean': np.mean(data),
        'variance': np.var(data),
        'std_dev': np.std(data),
        'signal_energy': np.sum(data**2),
        'rms': np.sqrt(np.mean(data**2)),
        'peak_to_peak': np.max(data) - np.min(data)
    }
    
    # Frequency domain analysis
    freqs, magnitude = calculate_fft(data)
    band_powers = calculate_band_powers(freqs, magnitude)
    
    # Combine all results
    results = {**stats, **band_powers}
    return results

def process_folder(folder_name):
    # Create analysis_results directory if it doesn't exist
    os.makedirs('analysis_results', exist_ok=True)
    
    files = sorted(glob.glob(f"{folder_name}/{folder_name}*.txt"))
    all_results = []
    
    for file_path in files:
        file_name = os.path.basename(file_path)
        results = analyze_file(file_path)
        results['file_name'] = file_name
        all_results.append(results)
    
    # Convert to DataFrame and save
    df = pd.DataFrame(all_results)
    
    # Save detailed results
    df.to_csv(f'analysis_results/{folder_name}_detailed_analysis.csv', index=False)
    
    # Calculate and save summary statistics
    summary = df.describe()
    summary.to_csv(f'analysis_results/{folder_name}_summary_statistics.csv')
    
    # Save band power comparison
    band_powers = df[['delta_power', 'theta_power', 'alpha_power', 'beta_power', 'gamma_power']]
    band_powers.to_csv(f'analysis_results/{folder_name}_band_powers.csv')
    
    print(f"Analysis completed for folder {folder_name}")

def main():
    # Process each condition
    conditions = {
        'A': 'Eyes Open',
        'B': 'Eyes Closed',
        'C': 'Presurgical Diagnosis 1',
        'D': 'Presurgical Diagnosis 2',
        'E': 'Presurgical Diagnosis 3'
    }
    
    for folder, condition in conditions.items():
        print(f"\nProcessing {condition} (Folder {folder})...")
        process_folder(folder)

if __name__ == "__main__":
    main() 