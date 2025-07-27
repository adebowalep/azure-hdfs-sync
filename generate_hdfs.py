import os
import numpy as np
import h5py

# ====== Configuration ======
base_path = "mock_hdf5_runs"  
num_runs = 3                  # Number of simulation runs
files_per_run = 2             # Files per run
rows, cols = 100, 100         # Shape of dataset in each HDF5 file
dataset_name = "sim_data"     # Name of dataset inside each file

# ====== Generate Folders & Files ======
os.makedirs(base_path, exist_ok=True)

# Create the base directory if it doesn't exist
for run in range(1, num_runs + 1):
    run_folder = os.path.join(base_path, f"run_{run:02}")
    os.makedirs(run_folder, exist_ok=True)
    
    # Create HDF5 files in the run folder
    for f in range(1, files_per_run + 1):
        file_path = os.path.join(run_folder, f"sample_{f:02}.h5")
        with h5py.File(file_path, "w") as h5file:
            h5file.create_dataset(dataset_name, data=np.random.rand(rows, cols))

        print(f"Created: {file_path}")