import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class DualPlotViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Dual Folder Data Viewer")
        self.root.geometry("1400x800")
        
        # Main container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left Plot (A+B)
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.create_folder_controls(self.left_frame, ['A', 'B'])
        self.create_plot(self.left_frame, 'AB')
        
        # Right Plot (C+D+E)
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.create_folder_controls(self.right_frame, ['C', 'D', 'E'])
        self.create_plot(self.right_frame, 'CDE')

    def create_folder_controls(self, parent, folders):
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=5)
        
        for folder in folders:
            frame = ttk.Frame(control_frame)
            frame.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(frame, text=f"{folder}:").pack(side=tk.LEFT)
            cb = ttk.Combobox(frame, values=[], width=7)
            cb.pack(side=tk.LEFT, padx=2)
            cb.bind("<<ComboboxSelected>>", lambda e, f=folder: self.update_plot(f))
            
            # Store combobox reference
            setattr(self, f'{folder}_combobox', cb)
            
            # Load initial files
            self.load_folder_files(folder)

    def create_plot(self, parent, plot_id):
        fig = plt.Figure(figsize=(7, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Store plot components
        setattr(self, f'{plot_id}_fig', fig)
        setattr(self, f'{plot_id}_ax', ax)
        
        # Canvas for embedding plot
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        setattr(self, f'{plot_id}_canvas', canvas)
        
        # Initialize plot lines
        colors = {'A': 'blue', 'B': 'red', 'C': 'green', 'D': 'purple', 'E': 'orange'}
        for folder in (['A','B'] if plot_id == 'AB' else ['C','D','E']):
            line, = ax.plot([], [], color=colors[folder], label=folder)
            setattr(self, f'{folder}_line', line)
        
        ax.legend()
        ax.grid(True)
        ax.set_xlabel("Line Number")
        ax.set_ylabel("Value")

    def load_folder_files(self, folder):
        folder_path = os.path.join(os.getcwd(), folder)
        if not os.path.exists(folder_path):
            print(f"Folder {folder} not found!")
            return
            
        files = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')])
        file_nums = ['000'] + [f[1:4] for f in files if f.startswith(folder)]
        getattr(self, f'{folder}_combobox')['values'] = file_nums

    def update_plot(self, folder):
        file_num = getattr(self, f'{folder}_combobox').get()
        if not file_num:
            return
            
        filename = os.path.join(folder, f"{folder}{file_num}.txt")
        if file_num != '000' and not os.path.exists(filename):
            print(f"File {filename} not found!")
            return
        
        if file_num == '000':
            data = []
        else:
            # Read data
            with open(filename, 'r') as f:
                data = [float(line.strip()) for line in f.readlines()]
            
        # Update corresponding plot line
        line = getattr(self, f'{folder}_line')
        line.set_data(range(1, len(data)+1), data)
        
        # Update plot limits
        ax = self.AB_ax if folder in ['A','B'] else self.CDE_ax
        ax.relim()
        ax.autoscale_view()
        
        # Redraw canvas
        canvas = self.AB_canvas if folder in ['A','B'] else self.CDE_canvas
        canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = DualPlotViewer(root)
    root.mainloop()