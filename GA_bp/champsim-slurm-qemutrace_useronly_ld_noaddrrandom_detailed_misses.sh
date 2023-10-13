#!/bin/bash
#SBATCH --job-name=Misses_kx      # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=8G         # memory per cpu-core (4G is default)
#SBATCH --time=0-23:59:00        # total run time limit (HH:MM:SS)
#SBATCH --mail-type=ALL        # send email when job fails
#SBATCH --mail-user=kaifengx@princeton.edu

# $1 version
# $2 load insn point
BIN=/tigress/kaifengx/ChampSim/bin/champsim_branchonly_user_ld_noaddrrandom_detailed_misses
# cd /tigress/kaifengx/ChampSim
BP_STATES=/tigress/kaifengx/ChampSim/branch/tage/states_useronly_noaddrrandom/
TRACE=/scratch/gpfs/kaifengx/trace_br_20230918_imageprocessing_2.out
WARMUP_INSN=90000000
# use sim_insn as loading point
SIM_INSN=$2

$BIN --warmup_instructions ${WARMUP_INSN} --simulation_instructions ${SIM_INSN} -c -b ${BP_STATES}insn -n $1 ${TRACE} > /scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_2_ld${SIM_INSN}_v${1}.out
# $BIN --warmup_instructions ${WARMUP_INSN} --simulation_instructions ${SIM_INSN} -c -b ${BP_STATES}insn -n $1 ${TRACE} > ${BP_STATES}useronly_ld_noaddrrandom_detailed_misses_init_ld${SIM_INSN}_${1}.out
# sbatch champsim-slurm-qemutrace_useronly_ld_noaddrrandom.sh ${1}
# sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom.sh $((${1} + 1))
