#!/bin/bash
#SBATCH --job-name=Misses_kx      # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=8G         # memory per cpu-core (4G is default)
#SBATCH --time=0-23:59:00        # total run time limit (HH:MM:SS)
#SBATCH --mail-type=FAIL        # send email when job fails
#SBATCH --mail-user=kaifengx@princeton.edu

# $1 trace name
TRACE_NAME=$1 # nokvm-2023-11-13_-_23-41-55-chameleon.trace
BIN=/tigress/kaifengx/ChampSim_qemu/ChampSim-private/bin/champsim_tage-replay-lessmemory_detailed_misses_st
BP_STATES=/scratch/gpfs/kaifengx/tage-replay_states/${TRACE_NAME}_lessmemory.states
TRACE_DIR=/scratch/gpfs/kaifengx/
TRACE=${TRACE_DIR}${TRACE_NAME}
# OUTPUT_DIR=/tigress/kaifengx/ChampSim_qemu/ChampSim-private/branch/tage-replay/results/
OUTPUT_DIR=/scratch/gpfs/kaifengx/function_bench_results/
WARMUP_INSN=000000000
# use sim_insn as loading point
SIM_INSN=1000000000

$BIN --warmup_instructions ${WARMUP_INSN} --simulation_instructions ${SIM_INSN} -c -s ${BP_STATES} ${TRACE}  > ${OUTPUT_DIR}${TRACE_NAME}_store_states_lessmemory.out
# $BIN --warmup_instructions ${WARMUP_INSN} --simulation_instructions ${SIM_INSN} -c -b ${BP_STATES}insn -n $1 ${TRACE} > ${BP_STATES}useronly_ld_noaddrrandom_detailed_misses_init_ld${SIM_INSN}_${1}.out
# sbatch champsim-slurm-qemutrace_useronly_ld_noaddrrandom.sh ${1}
# sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom.sh $((${1} + 1))
