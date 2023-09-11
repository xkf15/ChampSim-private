#!/bin/bash
#SBATCH --job-name=GA_bp_kx      # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=8G         # memory per cpu-core (4G is default)
#SBATCH --time=0-23:59:00        # total run time limit (HH:MM:SS)
#SBATCH --mail-type=ALL        # send email when job fails
#SBATCH --mail-user=kaifengx@princeton.edu

# $1 binary name
# $2 folder name
# $3 trace name
# $4 warmup instruction number
# $5 sim instruction number
BIN=/tigress/kaifengx/ChampSim/bin/champsim_branchonly_ld_for_diff_traces
# cd /tigress/kaifengx/ChampSim
BP_STATES=/tigress/kaifengx/ChampSim/branch/tage/states/
# TRACE=/scratch/gpfs/kaifengx/nokvm-2023-06-26_-_19-16-36-imageprocessing_test.trace
TRACE=/scratch/gpfs/kaifengx/nokvm-2023-07-18_-_15-23-51-imageprocessing_test_2nd.trace
WARMUP_INSN=1000000000
SIM_INSN=9000000000

$BIN --warmup_instructions ${WARMUP_INSN} --simulation_instructions ${SIM_INSN} -c -b ${BP_STATES}insn -n $1 ${TRACE} > ${BP_STATES}_ld_diff_traces_${1}_times.out
# sbatch champsim-slurm-qemutrace_retrain.sh $((${1} + 1))
