# $1 iteration number
# $2 benchmark number
# $3 trace1
# $4 trace2

# TRACE1=/scratch/gpfs/kaifengx/trace_br_20230925_600.perlbench_s.out
# TRACE2=/scratch/gpfs/kaifengx/trace_br_20230926_195210_600.perlbench_s.out
# sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom_spec.sh 0 600 $TRACE1 $TRACE2

TRACE1=/scratch/gpfs/kaifengx/trace_br_20230927_172323_602.gcc_s.out
TRACE2=/scratch/gpfs/kaifengx/trace_br_20230927_223338_602.gcc_s.out
sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom_spec.sh 0 602 $TRACE1 $TRACE2
