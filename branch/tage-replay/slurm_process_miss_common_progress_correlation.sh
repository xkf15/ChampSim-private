#!/bin/bash
#SBATCH --job-name=Misses_kx      # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=16G         # memory per cpu-core (4G is default)
#SBATCH --time=1-23:59:00        # total run time limit (HH:MM:SS)
#SBATCH --mail-type=FAIL        # send email when job fails
#SBATCH --mail-user=kaifengx@princeton.edu


module add anaconda3/2023.3
python3 process_miss_common_progress_correlation_match_plot.py
