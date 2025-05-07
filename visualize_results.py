import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def load_analysis_data():
    # Create visualization directory
    os.makedirs('visualization_results', exist_ok=True)
    
    # Load all analysis results
    data = {}
    conditions = {
        'A': 'Eyes Open',
        'B': 'Eyes Closed',
        'C': 'Presurgical Diagnosis 1',
        'D': 'Presurgical Diagnosis 2',
        'E': 'Presurgical Diagnosis 3'
    }
    
    for folder, condition in conditions.items():
        detailed_file = f'analysis_results/{folder}_detailed_analysis.csv'
        if os.path.exists(detailed_file):
            data[condition] = pd.read_csv(detailed_file)
    
    return data

def plot_band_powers_comparison(data):
    plt.figure(figsize=(15, 8))
    
    # Prepare data for plotting
    band_powers = []
    for condition, df in data.items():
        for band in ['delta', 'theta', 'alpha', 'beta', 'gamma']:
            band_powers.append({
                'Condition': condition,
                'Band': band,
                'Power': df[f'{band}_power'].mean()
            })
    
    band_df = pd.DataFrame(band_powers)
    
    # Create grouped bar plot
    sns.barplot(data=band_df, x='Band', y='Power', hue='Condition')
    plt.title('Average Power in Different Frequency Bands Across Conditions')
    plt.xlabel('Frequency Band')
    plt.ylabel('Power')
    plt.xticks(rotation=45)
    plt.legend(title='Condition', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('visualization_results/band_powers_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_basic_stats_comparison(data):
    stats = ['mean', 'variance', 'std_dev', 'signal_energy', 'rms', 'peak_to_peak']
    
    for stat in stats:
        plt.figure(figsize=(12, 6))
        
        # Prepare data
        stat_data = []
        for condition, df in data.items():
            stat_data.append({
                'Condition': condition,
                'Value': df[stat].mean()
            })
        
        stat_df = pd.DataFrame(stat_data)
        
        # Create bar plot
        sns.barplot(data=stat_df, x='Condition', y='Value')
        plt.title(f'Average {stat.replace("_", " ").title()} Across Conditions')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'visualization_results/{stat}_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()

def plot_condition_distributions(data):
    stats = ['mean', 'variance', 'std_dev', 'signal_energy', 'rms', 'peak_to_peak']
    
    for stat in stats:
        plt.figure(figsize=(12, 6))
        
        # Prepare data
        stat_data = []
        for condition, df in data.items():
            for value in df[stat]:
                stat_data.append({
                    'Condition': condition,
                    'Value': value
                })
        
        stat_df = pd.DataFrame(stat_data)
        
        # Create violin plot
        sns.violinplot(data=stat_df, x='Condition', y='Value')
        plt.title(f'Distribution of {stat.replace("_", " ").title()} Across Conditions')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'visualization_results/{stat}_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()

def plot_correlation_heatmap(data):
    for condition, df in data.items():
        plt.figure(figsize=(12, 10))
        
        # Select numerical columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numeric_cols].corr()
        
        # Create heatmap
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
        plt.title(f'Correlation Matrix - {condition}')
        plt.tight_layout()
        plt.savefig(f'visualization_results/{condition}_correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()

def main():
    print("Loading analysis data...")
    data = load_analysis_data()
    
    print("Creating band powers comparison plot...")
    plot_band_powers_comparison(data)
    
    print("Creating basic statistics comparison plots...")
    plot_basic_stats_comparison(data)
    
    print("Creating distribution plots...")
    plot_condition_distributions(data)
    
    print("Creating correlation heatmaps...")
    plot_correlation_heatmap(data)
    
    print("\nAll visualizations have been saved in the 'visualization_results' folder.")

if __name__ == "__main__":
    main() 