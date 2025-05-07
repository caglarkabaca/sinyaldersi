import os
import numpy as np
import matplotlib.pyplot as plt
import glob

def read_file_data(file_path):
    with open(file_path, 'r') as f:
        return [float(line.strip()) for line in f if line.strip()]

def process_folder(folder_name):
    # Create raw_charts directory if it doesn't exist
    os.makedirs('raw_charts', exist_ok=True)
    
    files = sorted(glob.glob(f"{folder_name}/{folder_name}*.txt"))
    plt.figure(figsize=(20, 10))  # Horizontal layout
    for file_path in files:
        data = read_file_data(file_path)
        x = range(len(data))
        plt.plot(x, data, alpha=0.5, label=os.path.basename(file_path))
    plt.title(f'Data from {folder_name} folder')
    plt.xlabel('Line Index')
    plt.ylabel('Value')
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    
    # Save the plot in raw_charts folder
    plt.savefig(f'raw_charts/{folder_name}_plot.png', bbox_inches='tight', dpi=300)
    plt.close()

def main():
    for folder in ['A', 'B', 'C', 'D', 'E']:
        process_folder(folder)
        print(f"Created plot for folder {folder} in raw_charts directory")

if __name__ == "__main__":
    main() 