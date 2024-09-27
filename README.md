# MD_Simulations

This repository contains data files and code for running Molecular Dynamics (MD) simulations. In these simulations, a simulation box is created with an organic linker positioned at the center, surrounded by water molecules. The workflow begins with CIF files of the linkers, and the LAMMPS interface is used to generate the necessary data files for the simulations. Automation of MD job submissions is managed using `job_manager_diffusion.py` for MIT's Supercloud.

### Contents:

- **job_manager_diffusion.py**: Automates the submission of MD simulation jobs to MIT's Supercloud.
- **lammps_data_file_generation.py**: Generates LAMMPS-compatible data files from CIF files.
- **cif_files_updated/**: A folder containing CIF files for various organic linkers.
- **lammps_data_1/**: Data files generated using LAMMPS from the CIF files.
- **template/**: Contains templates for submitting MD simulation jobs.

