///////////////////////////////////////////////////////////////////////
////  Copyright 2015 Samsung Austin Semiconductor, LLC.                //
/////////////////////////////////////////////////////////////////////////

#include "tage_sc_l.h"



bool tage_sc_l::predict_branch(uint64_t pc){
    bool prediction = tage.GetPrediction(pc);
    return prediction;
}

void tage_sc_l::last_branch_result(uint64_t pc, uint64_t branch_target, uint8_t taken, uint8_t branch_type){
  tage.UpdatePredictor(pc, (OpType)branch_type, taken, taken, branch_target);
}
