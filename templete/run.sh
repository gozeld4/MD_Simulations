#!/bin/bash
#SBATCH --job-name=ins_Pd2L4_OTf
#SBATCH -p xeon-p8
#SBATCH -N 1   # node count
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH -t 96:00:00

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

module purge
module load mpi/openmpi-4.1.5

code=/home/gridsan/gdovranova/HJKgroup_shared/AkashBall/packages/lammps-stable_29Sep2021/build/lmp

mpiexec -np 4 $code -in in.cage -l log.lammps > cage.out
