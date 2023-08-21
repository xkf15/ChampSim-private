for i in $(seq 101 500)
do
    insn=$(($i * 10000000))
    fname=/tigress/kaifengx/ChampSim/branch/tage/states/insn$insn
    sbatch champsim-slurm-qemutrace.sh $fname
done

