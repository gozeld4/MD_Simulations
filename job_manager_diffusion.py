import os
import shutil
import subprocess
import pandas as pd
import time

def submit_job(filename, data_files_path):
    try:
        current_dir = os.getcwd()
        filename_wo_data = filename.replace('data.', '')
        filename_parts = filename_wo_data.split('_')
        func_group = filename_parts[1]
        num_func = filename_parts[2]
        mofname = filename_parts[0]
        
        # if len(filename_parts[1:-2]) > 1:
        #     mofname = ''
        #     for element in filename_parts[1:-2]:
        #         mofname += element +'_'
        #     mofname = mofname[:-1]
        # else:
        #     mofname = filename_parts[1]
        
        diffusion_dir = f'./nvt_results_func/{mofname}/{num_func}_func/{func_group}/' #???
        if not os.path.exists(diffusion_dir):
            os.makedirs(diffusion_dir)
        
        input_path = os.path.join(diffusion_dir, 'in.cage')
        run_path = os.path.join(diffusion_dir, 'run.sh')
        water_path = os.path.join(diffusion_dir, 'water.tip4p')
        datafile_path = os.path.join(diffusion_dir, filename)

        shutil.copyfile('./template/in.cage', input_path) 
        shutil.copyfile('./template/run.sh', run_path)
        shutil.copyfile('./template/water.tip4p', water_path)
        shutil.copyfile(os.path.join(data_files_path, filename), datafile_path)


        with open(datafile_path, 'r') as lammps_data_file:
            for i, line in enumerate(lammps_data_file):
                if i == 8:
                    line_parts = line.split(' ')
                    line_parts_wo_space = [x for x in line_parts if x != '']
                    atom_type = line_parts_wo_space[0]
                elif i == 9:
                    line_parts = line.split(' ')
                    line_parts_wo_space = [x for x in line_parts if x != '']
                    bond_type = line_parts_wo_space[0]
                elif i == 10:
                    line_parts = line.split(' ')
                    line_parts_wo_space = [x for x in line_parts if x != '']
                    angle_type = line_parts_wo_space[0]
                elif i == 11:
                    line_parts = line.split(' ')
                    line_parts_wo_space = [x for x in line_parts if x != '']
                    dihedral_type = line_parts_wo_space[0]
                elif i == 12:
                    line_parts = line.split(' ')
                    line_parts_wo_space = [x for x in line_parts if x != '']
                    improper_type = line_parts_wo_space[0]
                    break
                else:
                    continue

        with open(input_path, 'r') as input_file:
            input_template = input_file.read()
        input_template = input_template.replace('datafile_name', filename)
        atom_type_int = int(atom_type)
        mofgroup = 'linker type '

        for i in range(1, atom_type_int+1):
            mofgroup = mofgroup + ' ' + str(i)
        watergroup = f'tip4p type {atom_type_int+1} {atom_type_int+2} {atom_type_int+3}'

        input_template = input_template.replace('mofgroup', mofgroup)
        input_template = input_template.replace('watergroup', watergroup)
        input_template = input_template.replace('atom bond angle dihedral improper', f'{atom_type} {bond_type} {angle_type} {dihedral_type} {improper_type}')
        input_template = input_template.replace('O_type', f'{atom_type_int+1}')
        input_template = input_template.replace('H_type', f'{atom_type_int+2}')
        input_template = input_template.replace('M_type', f'{atom_type_int+3}')
        

        input_template = input_template.replace('O-H', f'{int(bond_type)+1}')
        input_template = input_template.replace('O-M', f'{int(bond_type)+2}')
        input_template = input_template.replace('<HOH', f'{int(angle_type)+1}')

        with open(input_path, 'w') as file:
            file.write(input_template)

        os.chdir(diffusion_dir)
        command = 'sbatch run_p8.sh'
        subprocess.Popen(command, shell=True)
        print(f'Submitted: {mofname}, {func_group}, {num_func}')
        os.chdir(current_dir)
    except:
        print(f'Failed: {mofname}, {func_group}, {num_func}')

def get_running_jobs_count():
    command1 = f"squeue -u gdovranova | grep 'xeon-p8' | wc -l"
    result1 = subprocess.run(command1, shell=True, stdout=subprocess.PIPE, text=True)
    return int(result1.stdout.strip())

def main():
    job_limit = 90
    total_jobs = 70
    job_submitted = 0

    data_files_path = './lammps_data_1/'
    data_files = os.listdir(data_files_path)
    #data_files = ['data.functionalized_ADABUE_COOH_1']

    while True:
        running_jobs = get_running_jobs_count()
        print(running_jobs)
        if running_jobs < job_limit:
            submit_job(data_files[job_submitted], data_files_path)
            job_submitted += 1

        if job_submitted == total_jobs:
            break
        if running_jobs < job_limit:
            time.sleep(5)
        else:
            time.sleep(600)

if __name__ == "__main__":
    main()
    
