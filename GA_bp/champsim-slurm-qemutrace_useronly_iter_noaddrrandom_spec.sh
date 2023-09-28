#!/bin/bash
#SBATCH --job-name=Retrain_bp_kx # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=8G         # memory per cpu-core (4G is default)
#SBATCH --time=0-23:59:00        # total run time limit (HH:MM:SS)
#SBATCH --mail-type=FAIL         # send email when job fails
#SBATCH --mail-user=kaifengx@princeton.edu

# $1 iteration number
# $2 benchmark number
# $3 trace1
# $4 trace2
BIN=/tigress/kaifengx/ChampSim/bin/champsim_branchonly_user_iter_noaddrrandom_spec
# cd /tigress/kaifengx/ChampSim
BP_STATES=/tigress/kaifengx/ChampSim/branch/tage/states_useronly_noaddrrandom_spec_${2}/
TRACE_LD=$3 #/scratch/gpfs/kaifengx/trace_br_20230926_195210_600.perlbench_s.out
# TRACE=/scratch/gpfs/kaifengx/nokvm-2023-06-26_-_19-16-36-imageprocessing_test.trace
WARMUP_INSN=100000000
SIM_INSN=900000000

mkdir ${BP_STATES}
$BIN --warmup_instructions ${WARMUP_INSN} --simulation_instructions ${SIM_INSN} -c -b ${BP_STATES}insn -n $1 ${TRACE_LD} > ${BP_STATES}useronly_iter_noaddrrandom_spec_${2}_${1}.out
sbatch champsim-slurm-qemutrace_useronly_ld_noaddrrandom_spec.sh ${1} ${2} ${4}
sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom_spec.sh $((${1} + 1)) ${2} ${3} ${4}
