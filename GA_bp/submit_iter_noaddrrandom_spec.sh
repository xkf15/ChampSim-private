# $1 iteration number
# $2 benchmark number
# $3 trace1
# $4 trace2

# TRACE1=/scratch/gpfs/kaifengx/trace_br_20230925_600.perlbench_s.out
# TRACE2=/scratch/gpfs/kaifengx/trace_br_20230926_195210_600.perlbench_s.out
# sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom_spec.sh 0 600 $TRACE1 $TRACE2

# TRACE1=/scratch/gpfs/kaifengx/trace_br_20230927_172323_602.gcc_s.out
# TRACE2=/scratch/gpfs/kaifengx/trace_br_20230927_223338_602.gcc_s.out
# sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom_spec.sh 0 602 $TRACE1 $TRACE2

TRACE1=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231004_150748_600.perlbench_s.out
TRACE2=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231005_041844_600.perlbench_s.out
sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom_spec.sh 0 600 $TRACE1 $TRACE2

TRACE1=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231005_173529_602.gcc_s.out
TRACE2=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231006_063326_602.gcc_s.out
sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom_spec.sh 0 602 $TRACE1 $TRACE2

TRACE1=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231006_192949_605.mcf_s.out
TRACE2=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231006_235226_605.mcf_s.out
sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom_spec.sh 0 605 $TRACE1 $TRACE2

TRACE1=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231007_041452_620.omnetpp_s.out
TRACE2=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231007_041601_620.omnetpp_s.out
sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom_spec.sh 0 620 $TRACE1 $TRACE2

TRACE1=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231007_041711_623.xalancbmk_s.out
TRACE2=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231007_084237_623.xalancbmk_s.out
sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom_spec.sh 0 623 $TRACE1 $TRACE2

TRACE1=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231007_130846_625.x264_s.out
TRACE2=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231007_213544_625.x264_s.out
sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom_spec.sh 0 625 $TRACE1 $TRACE2

TRACE1=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231008_060319_631.deepsjeng_s.out
TRACE2=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231008_100811_631.deepsjeng_s.out
sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom_spec.sh 0 631 $TRACE1 $TRACE2

TRACE1=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231008_141251_641.leela_s.out
TRACE2=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231008_182305_641.leela_s.out
sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom_spec.sh 0 641 $TRACE1 $TRACE2

TRACE1=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231008_223309_648.exchange2_s.out
TRACE2=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231009_025151_648.exchange2_s.out
sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom_spec.sh 0 648 $TRACE1 $TRACE2

TRACE1=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231009_071052_657.xz_s.out
TRACE2=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231009_153627_657.xz_s.out
sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom_spec.sh 0 657 $TRACE1 $TRACE2

TRACE1=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231010_000239_998.specrand_is.out
TRACE2=/scratch/gpfs/kaifengx/spec_trace/trace_br_20231010_020430_998.specrand_is.out
sbatch champsim-slurm-qemutrace_useronly_iter_noaddrrandom_spec.sh 0 998 $TRACE1 $TRACE2

