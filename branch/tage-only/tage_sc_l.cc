///////////////////////////////////////////////////////////////////////
////  Copyright 2015 Samsung Austin Semiconductor, LLC.                //
/////////////////////////////////////////////////////////////////////////

#include "tage_sc_l.h"
#include <ooo_cpu.h>

// bool tage_sc_l::predict_branch(uint64_t pc){
//     bool prediction = tage.GetPrediction(pc);
//     return prediction;
// }
// 
// void tage_sc_l::last_branch_result(uint64_t pc, uint64_t branch_target, uint8_t taken, uint8_t branch_type){
//   tage.UpdatePredictor(pc, (OpType)branch_type, taken, taken, branch_target);
// }


PREDICTOR tage_predictor[NUM_CPUS];

void O3_CPU::initialize_branch_predictor()
{
    // tage_predictor[cpu].init();
}

// uint8_t O3_CPU::predict_branch(uint64_t ip)
uint8_t O3_CPU::predict_branch(uint64_t asid, uint64_t ip, uint64_t predicted_target, uint8_t always_taken, uint8_t branch_type)
{
    // return tage_predictor[cpu].predict(ip);
    bool prediction = tage_predictor[cpu].GetPrediction(asid, ip);
    return prediction;
}

void O3_CPU::last_branch_result(uint64_t asid, uint64_t ip, uint64_t branch_target, uint8_t taken, uint8_t branch_type)
{
    // tage_predictor[cpu].update(ip, taken);
    tage_predictor[cpu].UpdatePredictor(asid, ip, (OpType)branch_type, taken, taken, branch_target, true);
}

// void O3_CPU::bp_store_states(long insn_count)
// {
//     // tage_predictor[cpu].store_tables(insn_count);
// }
// 
// void O3_CPU::bp_load_states(long insn_count)
// {
//    tage_predictor[cpu].load_table(insn_count);
// }
// 
// void O3_CPU::print_detailed_misses()
// {
//     // printf("Miss Types: no_avail_space: %ld wrong_pred: %ld conflict_miss: %ld\n", tage_predictor[cpu].no_avail_space, tage_predictor[cpu].wrong_pred, tage_predictor[cpu].conflict_miss);
// }
