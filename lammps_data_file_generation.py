import os
import subprocess
import time
import shutil

# Unfunctionalized CIFs
mof_path = '/Users/gozel/Desktop/Urop_Kulik_Lab/MD_071924/cif_files_updated'
mof_list = ['UiO-66', 'HKUST-1', 'HOWRES', 'NOTT-300', 'QIFLOI']

current_dir = os.getcwd()

for mof in mof_list:

    #cif_path = os.path.join(mof_path, mof)
    cif_path = f'/Users/gozel/Desktop/Urop_Kulik_Lab/MD_071924/cif_files_updated/{mof}_2_func'
    all_cif = os.listdir(cif_path)
    print(all_cif)
    for cif_file in all_cif:
        if cif_file != '!DS_Store':
            if not os.path.exists('/Users/gozel/Desktop/Urop_Kulik_Lab/MD_071924/lammps_data_2'):
                os.makedirs('/Users/gozel/Desktop/Urop_Kulik_Lab/MD_071924/lammps_data_2')
                
            os.chdir('/Users/gozel/Desktop/Urop_Kulik_Lab/MD_071924/lammps_data_2')
            print(os.path.join(cif_path, cif_file))
            command = f'lammps-interface --replication=1,1,1 {os.path.join(cif_path, cif_file)}'
            try:
                process = subprocess.Popen(command, shell=True)
                # input_1 = 'y\n'
                # input_2 = 'y\n'
                # output_1, errors_1 = process.communicate(input=input_1)
                # output_2, errors_2 = process.communicate(input=input_2)
                time.sleep(3)
                print(f'MOF: {mof}')
                os.chdir(current_dir)
            except:
                continue





        
