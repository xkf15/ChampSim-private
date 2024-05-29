#ifndef TAGE_SC_L
#define TAGE_SC_L

#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <inttypes.h>
#include <math.h>
#include <cstdio>
#include <iostream>
//#include "utils.h"
//#include "bt9.h"
//#include "bt9_reader.h"

#include <array>
#include <cstdint>
#include <tuple>

// Changed by Kaifeng Xu
// #include "modules.h"
// #include "msl/bits.h"
// #include "msl/fwcounter.h"
// #include <fmt/core.h>
#include <fstream>
#include "ooo_cpu.h"
#define NUM_STORED_ENTRY 4 // store several entries for insertion
#include <map>
// End of Kaifeng Xu



#define BORNTICK  1024
//To get the predictor storage budget on stderr  uncomment the next line
#define PRINTSIZE
#include <vector>

#define SC                      // 8.2 % if TAGE alone
#define IMLI                    // 0.2 %
#define LOCALH

#ifdef LOCALH                   // 2.7 %
#define LOOPPREDICTOR           //loop predictor enable
#define LOCALS                  //enable the 2nd local history
#define LOCALT                  //enables the 3rd local history

#endif


//The statistical corrector components

#define PERCWIDTH 6             //Statistical corrector  counter width 5 -> 6 : 0.6 %
//The three BIAS tables in the SC component
//We play with the TAGE  confidence here, with the number of the hitting bank
#define LOGBIAS 8
#define INDBIAS (((((PC ^(PC >>2))<<1)  ^  (LowConf &(LongestMatchPred!=alttaken))) <<1) +  pred_inter) & ((1<<LOGBIAS) -1)
#define INDBIASSK (((((PC^(PC>>(LOGBIAS-2)))<<1) ^ (HighConf))<<1) +  pred_inter) & ((1<<LOGBIAS) -1)


#define INDBIASBANK (pred_inter + (((HitBank+1)/4)<<4) + (HighConf<<1) + (LowConf <<2) +((AltBank!=0)<<3)+ ((PC^(PC>>2))<<7)) & ((1<<LOGBIAS) -1)



//In all th GEHL components, the two tables with the shortest history lengths have only half of the entries.




// playing with putting more weights (x2)  on some of the SC components
// playing on using different update thresholds on SC
//update threshold for the statistical corrector
#define VARTHRES
#define WIDTHRES 12
#define WIDTHRESP 8
#ifdef VARTHRES
#define LOGSIZEUP 6             //not worth increasing
#else
#define LOGSIZEUP 0
#endif
#define LOGSIZEUPS  (LOGSIZEUP/2)
#define INDUPD (PC ^ (PC >>2)) & ((1 << LOGSIZEUP) - 1)
#define INDUPDS ((PC ^ (PC >>2)) & ((1 << (LOGSIZEUPS)) - 1))
#define EWIDTH 6



#define CONFWIDTH 7             //for the counters in the choser
#define HISTBUFFERLENGTH 4096   // we use a 4K entries history buffer to store the branch history (this allows us to explore using history length up to 4K)

enum OpType{
  OPTYPE_RET_UNCOND,
  OPTYPE_JMP_INDIRECT_UNCOND,
  OPTYPE_JMP_INDIRECT_COND,
  OPTYPE_CALL_INDIRECT_UNCOND,
  OPTYPE_CALL_INDIRECT_COND,
  OPTYPE_RET_COND,
  OPTYPE_JMP_DIRECT_COND,
  OPTYPE_CALL_DIRECT_COND,
  OPTYPE_JMP_DIRECT_UNCOND,
  OPTYPE_CALL_DIRECT_UNCOND
};




// utility class for index computation
// this is the cyclic shift register for folding 
// a long global history into a smaller number of bits; see P. Michaud's PPM-like predictor at CBP-1
class folded_history
{
public:


  unsigned comp;
  int CLENGTH;
  int OLENGTH;
  int OUTPOINT;

    folded_history ()
  {
  }


  void init (int original_length, int compressed_length)
  {
    comp = 0;
    OLENGTH = original_length;
    CLENGTH = compressed_length;
    OUTPOINT = OLENGTH % CLENGTH;

  }

  void update (uint8_t * h, int PT)
  {
    comp = (comp << 1) ^ h[PT & (HISTBUFFERLENGTH - 1)];
    comp ^= h[(PT + OLENGTH) & (HISTBUFFERLENGTH - 1)] << OUTPOINT;
    comp ^= (comp >> CLENGTH);
    comp = (comp) & ((1 << CLENGTH) - 1);
  }

};




class bentry                    // TAGE bimodal table entry  
{
public:
  int8_t hyst;
  int8_t pred;


    bentry ()
  {
    pred = 0;

    hyst = 1;
  }

};
class gentry                    // TAGE global table entry
{
public:
  int8_t ctr;
  uint tag;
  int8_t u;
  // Changed by Kaifeng Xu
  int8_t is_prefetched;
  int8_t is_used;
  // End Kaifeng Xu

    gentry ()
  {
    ctr = 0;
    u = 0;
    tag = 0;
    is_prefetched = 0;
    is_used = 0;

  }
};



#define  POWER
//use geometric history length

#define NHIST 22                // twice the number of different histories

#define NBANKLOW 6              // number of banks in the shared bank-interleaved for the low history lengths
#define NBANKHIGH 10            // number of banks in the shared bank-interleaved for the  history lengths



#define BORN 9                 // below BORN in the table for low history lengths, >= BORN in the table for high history lengths,

// we use 2-way associativity for the medium history lengths
#define BORNINFASSOC 7          //2 -way assoc for those banks 0.4 %
#define BORNSUPASSOC 15

/*in practice 2 bits or 3 bits par branch: around 1200 cond. branchs*/

#define TAGE_SC_L_MINHIST 4             //not optimized so far
#define TAGE_SC_L_MAXHIST 1024


#define LOGG 8                 /* logsize of the  banks in the  tagged TAGE tables */
#define TBITS 8                 //minimum width of the tags  (low history lengths), +4 for high history lengths





#define NNN 0                   // number of extra entries allocated on a TAGE misprediction (1+NNN)
#define HYSTSHIFT 2             // bimodal hysteresis shared by 4 entries
#define LOGB 13                 // log of number of entries in bimodal predictor


#define PHISTWIDTH 27           // width of the path history used in TAGE
#define UWIDTH 1                // u counter width on TAGE (2 bits not worth the effort for a 512 Kbits predictor 0.2 %)
#define CWIDTH 3                // predictor counter width on the TAGE tagged tables


//the counter(s) to chose between longest match and alternate prediction on TAGE when weak counters
#define LOGSIZEUSEALT 4
#define ALTWIDTH 5
#define SIZEUSEALT  (1<<(LOGSIZEUSEALT))
#define INDUSEALT (((((HitBank-1)/8)<<1)+AltConf) % (SIZEUSEALT-1))


#ifdef LOOPPREDICTOR
//parameters of the loop predictor
#define LOGL 5
#define WIDTHNBITERLOOP 10      // we predict only loops with less than 1K iterations
#define LOOPTAG 10              //tag width in the loop predictor

class lentry                    //loop predictor entry
{
public:
  uint16_t NbIter;              //10 bits
  uint8_t confid;               // 4bits
  uint16_t CurrentIter;         // 10 bits

  uint16_t TAG;                 // 10 bits
  uint8_t age;                  // 4 bits
  bool dir;                     // 1 bit

  //39 bits per entry    
    lentry ()
  {
    confid = 0;
    CurrentIter = 0;
    NbIter = 0;
    TAG = 0;
    age = 0;
    dir = false;



  }


};

//variables for the loop predictor

#endif


// Added By Kaifeng Xu
class tage_miss_entry{
public:
    uint64_t local_history;
    bool valid;
    bool taken;
    tage_miss_entry(){
        local_history = 0;
        valid = false;
        taken = true;
    }
};

#define TAGE_MISS_TABLE_ENTRY_NUM 1000 // Number of problem PCs
// #define HOT_MISS_TABLE_SIZE 
class tage_miss_table{
public:
   tage_miss_entry entries[TAGE_MISS_TABLE_ENTRY_NUM];
   tage_miss_table(){
       int i = 0;
       for(i = 0; i < TAGE_MISS_TABLE_ENTRY_NUM; i++){
           entries[i];
       }
   }

};

class local_history_entry{
public:
    uint64_t pc;
    uint64_t local_history;
    local_history_entry(){
        pc = 0;
        local_history = 0;
    }
};

#define PPC_TABLE_ENTRY_NUM 10 // number of problem PCs
// #define PPC_TABLE_ENTRY_SIZE
class ppc_table{
public:
    local_history_entry entries[PPC_TABLE_ENTRY_NUM];
    ppc_table(){
        int i = 0;
        for(i = 0; i < PPC_TABLE_ENTRY_NUM; i++){
            entries[i];
        }
    }
};


// End of Kaifeng Xu

// Kaifeng Xu
bool sortByPC(const array<uint64_t, 5> buf1, const array<uint64_t, 5> buf2){
    if(buf1[0] != buf2[0]){
        return buf1[0] < buf2[0];;
    } else {
        if(buf1[1] != buf2[1]){
            return buf1[1] < buf2[1];
        } else {
            if(buf1[2] != buf2[2]){
                return buf1[2] < buf2[2];
            } else {
                if(buf1[3] != buf2[3]){
                    return buf1[3] < buf2[3];
                } else {
                    if(buf1[4] != buf2[4]){
                        return buf1[4] < buf2[4];
                    }
                }
            }
        }
    }
    return buf1[0] <= buf2[0];
}
// uint64_t compareByPC(const std::vector<std::array<uint64_t, 4>>::iterator it, uint64_t PC){
// uint64_t compareByPC(const <std::array<uint64_t, 4>> it, uint64_t PC){
//     return  it[0][0] > PC;
// }
// End Kaifeng Xu

class PREDICTOR
{
public:
  // Added by Kaifeng Xu
  int use_SC;
  int insert_taken = -1;
  int tage_sc_l_taken = -1;
  long long insn_count;
  int is_ld_st = 0; // 0 ld, st 1, no_st_ld 2
  int tmp_counter = 0;
  bool continue_prefetch = true;
  int PPCTable_idx; // Store the index of the matched PPCTable enty
  ppc_table PPCTable; // Store Problematic PCs
  tage_miss_table missTable; // Sotre local histories
  std::ofstream f_miss_his;
  std::ifstream f_ld_miss_his;
  bool init_states_files = false; // Test if init finished
  std::map<uint64_t, std::vector< std::array<uint, 6> > > prefetchTable; // Table read from file
  std::vector<std::array<uint64_t, 5>> prefetchBuffer; // real table to use for branch predictor
  int prefetchTable_idx = -1; // for history update
  int prefetchBuffer_idx = -1; // for history update
  int prefetch_useful = 0; // if use this results
  uint64_t bufferPCHead = 0;
  uint64_t bufferHead_ptr = 0;
  uint64_t bufferPCTail = 0;
  uint64_t bufferTail_ptr = 0;
  void load_table(long insn_count){
      return;
  }
  // Each entry 5 + 10 + 8/12 + 1
  void store_table(int bank_idx, int table_idx, uint tag, bool taken){
      if(!init_states_files){
          f_miss_his.open(bp_states_init_fname, std::ofstream::out);
          if (!f_miss_his.is_open()) {
              std::cerr << "Error opening the miss history file: " << bp_states_init_fname  << std::endl;
          }
          init_states_files = true;
      }
      f_miss_his << std::dec << bank_idx << " ";
      f_miss_his << std::dec << table_idx << " ";
      f_miss_his << std::dec << tag << " ";
      f_miss_his << taken << "\n";
      return ;
  }
  void store_insn_breaker(){
      f_miss_his << std::dec << 1450 << "\n"; // some random number
  }
  int tage_insertion(uint64_t PC){
    if(!init_states_files){
        f_ld_miss_his.open(bp_states_init_fname, std::ofstream::in);
        if (!f_ld_miss_his.is_open()) {
            std::cerr << "Error opening the miss history file: " << bp_states_init_fname  << std::endl;
        }
        while(!f_ld_miss_his.eof()){
            uint64_t tmp_pc = 0;
            f_ld_miss_his >> std::hex >> tmp_pc;
            std::array<uint, 6> tmp_value;
            f_ld_miss_his >> std::dec >> tmp_value[0] >> tmp_value[1] >> tmp_value[2] >> tmp_value[3] >> tmp_value[4];
            tmp_value[5] = 3; // usefulness counter
            prefetchTable[tmp_pc].push_back(tmp_value);
            if(tmp_value[0] == NHIST){
                std::array<uint64_t, 5> tmp_buffer;
                tmp_buffer[0] = tmp_pc;
                tmp_buffer[1] = tmp_value[1]; // hash 1
                tmp_buffer[2] = tmp_value[2]; // hash 2
                tmp_buffer[3] = tmp_value[3]; // taken
                tmp_buffer[4] = 3;
                prefetchBuffer.push_back(tmp_buffer);
            }
            // printf("%016llx %u %u %u %u %u\n", tmp_pc, prefetchTable[tmp_pc].back()[0], prefetchTable[tmp_pc].back()[1], prefetchTable[tmp_pc].back()[2], prefetchTable[tmp_pc].back()[3], prefetchTable[tmp_pc].back()[4]);
        }
        printf("Total Prefetch Info Size: %d\n", prefetchBuffer.size());
        fflush(stdout);
        std::sort(prefetchBuffer.begin(), prefetchBuffer.end(), sortByPC);
        for(int i = 0; i < prefetchBuffer.size(); i++){
            printf("%016llx %u %u %u\n", prefetchBuffer[i][0], prefetchBuffer[i][1], prefetchBuffer[i][2], prefetchBuffer[i][3]);
        }
        fflush(stdout);
        f_ld_miss_his.close();
        init_states_files = true;
    }

    // Check if hit in prefetchBuffer
    prefetchBuffer_idx = -1;
    insert_taken = -1; // -1 not decided, 0 not taken, 1 taken
    if((PC >= bufferPCHead) && (PC <= bufferPCTail)){
        for(int i = bufferHead_ptr; i < bufferTail_ptr; i++){
        // for(int i = 0; i < prefetchBuffer.size(); i++){
            // if(PC == prefetchBuffer[i][0]){
                 if((prefetchBuffer[i][0] & 0xff) == (PC & 0xff)){
                    if( (prefetchBuffer[i][1] == GI[NHIST]) && (prefetchBuffer[i][2] == GTAG[NHIST])){
                        insert_taken = prefetchBuffer[i][3];
                        prefetchBuffer_idx = i;
                        prefetch_useful = (prefetchBuffer[i][4] >= 3);
                        break;
                    }
                 }
            // }
        }

    }

    // Update prefetchBuffer
    // if PC is in range(bufferPCHead, bufferPCTail), do not update
    if((PC <= bufferPCHead) || (PC >= bufferPCTail)){
        // prefetchTable.lowerbound(PC);
        // for(auto it = prefetchTable.begin(); it != prefetchTable.end(); ++it){
        //     if(prefetchBuffer.size() < 1024){
        //         std::array<uint, 2> tmp_hash;
        //         prefetchBuffer.push_back(tmp_hash);
        //     }
        // }
        std::vector<std::array<uint64_t, 5>>::iterator newHead;
        std::array<uint64_t, 5> tmp_PCarray;
        tmp_PCarray[0] = PC;
        tmp_PCarray[1] = tmp_PCarray[2] = tmp_PCarray[3] = tmp_PCarray[4] = 0;
        newHead = std::lower_bound(prefetchBuffer.begin(), prefetchBuffer.end(), tmp_PCarray, sortByPC);
        if(newHead != prefetchBuffer.end()){
            bufferPCHead = newHead[0][0];
            bufferHead_ptr = newHead - prefetchBuffer.begin();
            if(bufferHead_ptr <= 128){
                newHead = prefetchBuffer.begin();
                bufferPCHead = newHead[0][0];
                bufferHead_ptr = 0;
            } else {
                newHead -= 128;
                bufferPCHead = newHead[0][0];
                bufferHead_ptr -= 128;
            }
            if((prefetchBuffer.end() - newHead) <= 1024){
                bufferPCTail = (prefetchBuffer.back())[0];
                bufferTail_ptr = prefetchBuffer.size() - 1;
            } else {
                bufferPCTail = (newHead + 1024)[0][0];
                bufferTail_ptr = bufferHead_ptr + 1024;
            }
        } else {
            ; // no change
        }
        printf("bufferHead_ptr: %d bufferTail_ptr: %d\n", bufferHead_ptr, bufferTail_ptr); // buffer Head moved
    }

    // Check if hit in prefetchTable
    // prefetchTable_idx = -1;
    // bool hit_in_prefetchTable = false;
    // if(prefetchTable.find(PC) != prefetchTable.end()){
    //     for( int i = 0; i < prefetchTable[PC].size(); i++ ){
    //         int bank_idx = prefetchTable[PC][i][0];
    //         int table_idx = prefetchTable[PC][i][1];
    //         uint tmp_tag = prefetchTable[PC][i][2];
    //         int tmp_taken = prefetchTable[PC][i][3];
    //         if(bank_idx == NHIST) { // Temporary Implementation
    //             if((table_idx == GI[bank_idx]) && (tmp_tag == GTAG[bank_idx])){
    //                 hit_in_prefetchTable = true;
    //                 insert_taken = prefetchTable[PC][i][3];
    //                 prefetchTable_idx = i;
    //                 prefetch_useful = (prefetchTable[PC][i][5] >= 3);
    //                 break;
    //             }
    //         }
    //     }
    // }
    // if(hit_in_prefetchTable){
    //     printf("bufferPCHead: %llx PC: %llx, bufferPCTail: %llx\n", bufferPCHead, PC, bufferPCTail);
    //     printf("bufferHead_ptr: %d bufferTail_ptr: %d\n", bufferHead_ptr, bufferTail_ptr);
    //     fflush(stdout);
    // }
    return insert_taken;

    //#### insert_taken = -1; // -1 not decided, 0 not taken, 1 taken
    //#### if(prefetchTable.find(PC) != prefetchTable.end()){
    //####     for( int i = 0; i < prefetchTable[PC].size(); i++ ){
    //####         // if((PC == 0xffffffffbb7cb672) && (prefetchTable[PC][i][0] == 22)){
    //####         //     printf("%016llx %u %u %u %u\n", PC, prefetchTable[PC][i][0], prefetchTable[PC][i][1], prefetchTable[PC][i][2], prefetchTable[PC][i][3]);
    //####         // }
    //####         int bank_idx = prefetchTable[PC][i][0];
    //####         int table_idx = prefetchTable[PC][i][1];
    //####         uint tmp_tag = prefetchTable[PC][i][2];
    //####         int tmp_taken = prefetchTable[PC][i][3];
    //####         if(bank_idx == NHIST) { // Temporary Implementation
    //####             if((table_idx == GI[bank_idx]) && (tmp_tag == GTAG[bank_idx])){
    //####                 insert_taken = tmp_taken;
    //####                 // Do the prefetch if and only if index and tag both matched
    //####                 if(tmp_tag == gtable[bank_idx][table_idx].tag){
    //####                     ctrupdate(gtable[bank_idx][table_idx].ctr, tmp_taken, CWIDTH);
    //####                 } else {
    //####                     gtable[bank_idx][table_idx].tag = tmp_tag;
    //####                     gtable[bank_idx][table_idx].ctr = (tmp_taken) ? 0 : -1;
    //####                     gtable[bank_idx][table_idx].is_prefetched = 1;
    //####                     gtable[bank_idx][table_idx].u = 0;
    //####                 }
    //####                 return insert_taken;
    //####             }
    //####         }
    //####     }
    //#### }
    //#### return insert_taken;

    
//     // store old history values
//     int bank_idx[NUM_STORED_ENTRY];
//     int table_idx[NUM_STORED_ENTRY];
//     uint tag[NUM_STORED_ENTRY];
//     bool resolveDir[NUM_STORED_ENTRY];
//     for(int i = 0; i < NUM_STORED_ENTRY; i++) {
//         if(f_ld_miss_his.peek() == EOF) return 0;
//         f_ld_miss_his >> std::dec >> bank_idx[i];
//         // Check Insn breaker
//         // return 0 means not gonna continue
//         if(bank_idx[i] == 1450) {
//             if(i != 0){
//                 std::cerr << "Error, should not find breaker when i != 0!" << std::endl;
//                 std::cerr << bank_idx[i-1] << " " << table_idx[i-1] << " " << tag[i-1] << " " << resolveDir[i-1] << std::endl;
//             }
//             return 0;
//         }
//         if(f_ld_miss_his.peek() == EOF) return 0;
//         f_ld_miss_his >> std::dec >> table_idx[i];
//         f_ld_miss_his >> std::dec >> tag[i];
//         f_ld_miss_his >> resolveDir[i];
//     }
//     // Tage insertion
//     int num_success = 0;// record number of successful insertion
//     int possible_evict_idx = -1;
//     // Always start at the last entry
//     for(int i = NUM_STORED_ENTRY-1 ; i >=0 ; i--){
//         if(tag[i] == gtable[bank_idx[i]][table_idx[i]].tag){
//             ctrupdate(gtable[bank_idx[i]][table_idx[i]].ctr, resolveDir[i], CWIDTH);
//             num_success ++;
//         } else if(gtable[bank_idx[i]][table_idx[i]].u == 0){
//             if(abs( 2 * gtable[bank_idx[i]][table_idx[i]].ctr + 1) <= 3){
//                 gtable[bank_idx[i]][table_idx[i]].tag = tag[i];
//                 gtable[bank_idx[i]][table_idx[i]].ctr = (resolveDir[i]) ? 0 : -1;
//                 gtable[bank_idx[i]][table_idx[i]].u = 0;
//                 num_success ++;
//             }
//             if(possible_evict_idx == -1) possible_evict_idx = i;
//         }
//         if(num_success >= 1) break; // at most insert 2 entries
//     }
//     // If no entry is inserted, at least insert 1 entry
//     // if(num_success == 0){
//     //     if(possible_evict_idx >= 0){
//     //         gtable[bank_idx[possible_evict_idx]][table_idx[possible_evict_idx]].tag = tag[possible_evict_idx];
//     //         gtable[bank_idx[possible_evict_idx]][table_idx[possible_evict_idx]].ctr = (resolveDir[possible_evict_idx]) ? 0 : -1;
//     //         gtable[bank_idx[possible_evict_idx]][table_idx[possible_evict_idx]].u = 0;
//     //     } else { // if all inserting entries are conflict with entires that u > 0
//     //         gtable[bank_idx[NUM_STORED_ENTRY-1]][table_idx[NUM_STORED_ENTRY-1]].tag = tag[NUM_STORED_ENTRY-1];
//     //         gtable[bank_idx[NUM_STORED_ENTRY-1]][table_idx[NUM_STORED_ENTRY-1]].ctr = (resolveDir[NUM_STORED_ENTRY-1]) ? 0 : -1;
//     //         gtable[bank_idx[NUM_STORED_ENTRY-1]][table_idx[NUM_STORED_ENTRY-1]].u = 0;
//     //     }
//     // }
//    return 1;
  }
  // End of Kaifeng Xu
  int THRES;
  bentry *btable;                       //bimodal TAGE table
  lentry *ltable;                       //loop predictor table
  gentry *gtable[NHIST + 1];    // tagged TAGE tables
  int SizeTable[NHIST + 1];
  bool predloop;                        // loop predictor prediction
  int LIB;
  int LI;
  int LHIT;                     //hitting way in the loop predictor
  int LTAG;                     //tag on the loop predictor
  bool LVALID;                  // validity of the loop predictor prediction
  int8_t WITHLOOP;              // counter to monitor whether or not loop prediction is beneficial
                                //
  //For the TAGE predictor
  int m[NHIST + 1];
  int TB[NHIST + 1];
  int logg[NHIST + 1];
 
  int GI[NHIST + 1];            // indexes to the different tables are computed only once  
  uint GTAG[NHIST + 1];         // tags for the different tables are computed only once  
  int BI;                               // index of the bimodal table
  bool pred_taken;              // prediction
  bool alttaken;                        // alternate  TAGEprediction
  bool tage_pred;                       // TAGE prediction
  bool LongestMatchPred;
  int HitBank;                  // longest matching bank
  int AltBank;                  // alternate matching bank
  int Seed;                     // for the pseudo-random number generator
  bool pred_inter;

  int TICK;                     // for the reset of the u counter
  uint8_t ghist[HISTBUFFERLENGTH];
  int ptghist;
  long long phist;              //path history
  folded_history ch_i[NHIST + 1];       //utility for computing TAGE indices
  folded_history ch_t[2][NHIST + 1];    //utility for computing TAGE tags

  long long IMLIcount;          // use to monitor the iteration number

  bool NOSKIP[NHIST + 1];               // to manage the associativity for different history lengths
  bool LowConf;
  bool HighConf;

  int8_t use_alt_on_na[SIZEUSEALT];
  //very marginal benefit
  long long GHIST;
  int8_t BIM;

  bool AltConf;                 // Confidence on the alternate prediction
                                //
  // The two counters used to choose between TAGE and SC on Low Conf SC
  int8_t FirstH, SecondH;
  bool MedConf;                 // is the TAGE prediction medium confidence
 
  int updatethreshold;
  int Pupdatethreshold[(1 << LOGSIZEUP)];       //size is fixed by LOGSIZEUP
  
  int8_t WG[(1 << LOGSIZEUPS)];
  int8_t WL[(1 << LOGSIZEUPS)];
  int8_t WS[(1 << LOGSIZEUPS)];
  int8_t WT[(1 << LOGSIZEUPS)];
  int8_t WP[(1 << LOGSIZEUPS)];
  int8_t WI[(1 << LOGSIZEUPS)];
  int8_t WIM[(1 << LOGSIZEUPS)];
  int8_t WB[(1 << LOGSIZEUPS)];
  
  int LSUM;
  
  int8_t Bias[(1 << LOGBIAS)];
  int8_t BiasSK[(1 << LOGBIAS)];
  int8_t BiasBank[(1 << LOGBIAS)];
 
// IMLI-SIC -> Micro 2015  paper: a big disappointment on  CBP2016 traces
#ifdef IMLI
#define LOGINB 8                // 128-entry
#define INB 1
 int Im[INB] = { 8 };
 int8_t IGEHLA[INB][(1 << LOGINB)] = { {0} };

 int8_t *IGEHL[INB];

#define LOGIMNB 9               // 2* 256 -entry
#define IMNB 2

 int IMm[IMNB] = { 10, 4 };
int8_t IMGEHLA[IMNB][(1 << LOGIMNB)] = { {0} };

int8_t *IMGEHL[IMNB];
long long IMHIST[256];

#endif

//global branch GEHL
#define LOGGNB 9               // 1 1K + 2 * 512-entry tables
#define GNB 3
int Gm[GNB] = { 40, 24, 10 };
int8_t GGEHLA[GNB][(1 << LOGGNB)] = { {0} };

int8_t *GGEHL[GNB];
//variation on global branch history
#define PNB 3
#define LOGPNB 8                // 1 1K + 2 * 512-entry tables
int Pm[PNB] = { 25, 16, 9 };
int8_t PGEHLA[PNB][(1 << LOGPNB)] = { {0} };

int8_t *PGEHL[PNB];

//first local history
#define LOGLNB  9              // 1 1K + 2 * 512-entry tables
#define LNB 3
int Lm[LNB] = { 11, 6, 3 };
int8_t LGEHLA[LNB][(1 << LOGLNB)] = { {0} };

int8_t *LGEHL[LNB];
#define  LOGLOCAL 7
#define NLOCAL (1<<LOGLOCAL)
#define INDLOCAL ((PC ^ (PC >>2)) & (NLOCAL-1))
long long L_shist[NLOCAL];      //local histories

// second local history
#define LOGSNB 8                // 1 1K + 2 * 512-entry tables
#define SNB 3
int Sm[SNB] = { 16, 11, 6 };
int8_t SGEHLA[SNB][(1 << LOGSNB)] = { {0} };

int8_t *SGEHL[SNB];
#define LOGSECLOCAL 3
#define NSECLOCAL (1<<LOGSECLOCAL)      //Number of second local histories
#define INDSLOCAL  (((PC ^ (PC >>5))) & (NSECLOCAL-1))
long long S_slhist[NSECLOCAL];

//third local history
#define LOGTNB 9               // 2 * 512-entry tables
#define TNB 2
int Tm[TNB] = { 9, 4 };
int8_t TGEHLA[TNB][(1 << LOGTNB)] = { {0} };

int8_t *TGEHL[TNB];
#define NTLOCAL 16
#define INDTLOCAL  (((PC ^ (PC >>(LOGTNB)))) & (NTLOCAL-1))     // different hash for the history
long long T_slhist[NTLOCAL];



    PREDICTOR (void)
  {

    std::cout <<"Calling PREDICTOR" << std::endl;
    reinit ();
#ifdef PRINTSIZE
    predictorsize ();
#endif
  }


  void reinit ()
  {
    // Added by Kaifeng Xu
    PPCTable;
    missTable;
    // TODO: Add prefetch PPCTable here
    // TODO: Add prefetch missTable here
    // End of Kaifeng Xu

    m[1] = TAGE_SC_L_MINHIST;
    m[NHIST / 2] = TAGE_SC_L_MAXHIST;
    for (int i = 2; i <= NHIST / 2; i++)
      {
        m[i] =
          (int) (((double) TAGE_SC_L_MINHIST *
                  pow ((double) (TAGE_SC_L_MAXHIST) / (double) TAGE_SC_L_MINHIST,
                       (double) (i - 1) / (double) (((NHIST / 2) - 1)))) +
                 0.5);
        //      fprintf(stderr, "(%d %d)", m[i],i);
        
      }
    for (int i = 1; i <= NHIST; i++)
      {
        NOSKIP[i] = ((i - 1) & 1)
          || ((i >= BORNINFASSOC) & (i < BORNSUPASSOC));

      }

    // NOSKIP[4] = 0;
    // NOSKIP[NHIST - 2] = 0;
    // NOSKIP[8] = 0;
    // NOSKIP[NHIST - 6] = 0;
    // just eliminate some extra tables (very very marginal)

    for (int i = NHIST; i > 1; i--)
      {
        m[i] = m[(i + 1) / 2];


      }
    for (int i = 1; i <= NHIST; i++)
      {
        TB[i] = TBITS + 4 * (i >= BORN);
        logg[i] = LOGG;

      }


#ifdef LOOPPREDICTOR
    ltable = new lentry[1 << (LOGL)];
#endif


    gtable[1] = new gentry[NBANKLOW * (1 << LOGG)];
    SizeTable[1] = NBANKLOW * (1 << LOGG);

    gtable[BORN] = new gentry[NBANKHIGH * (1 << LOGG)];
    SizeTable[BORN] = NBANKHIGH * (1 << LOGG);

    for (int i = BORN + 1; i <= NHIST; i++)
      gtable[i] = gtable[BORN];
    for (int i = 2; i <= BORN - 1; i++)
      gtable[i] = gtable[1];
    btable = new bentry[1 << LOGB];


    for (int i = 1; i <= NHIST; i++)
      {
        ch_i[i].init (m[i], (logg[i]));
        ch_t[0][i].init (ch_i[i].OLENGTH, TB[i]);
        ch_t[1][i].init (ch_i[i].OLENGTH, TB[i] - 1);

      }
#ifdef LOOPPREDICTOR
    LVALID = false;
    WITHLOOP = -1;
#endif
    Seed = 0;

    TICK = 0;
    phist = 0;
    Seed = 0;

    for (int i = 0; i < HISTBUFFERLENGTH; i++)
      ghist[0] = 0;
    ptghist = 0;
    updatethreshold=35<<3;
    
    for (int i = 0; i < (1 << LOGSIZEUP); i++)
      Pupdatethreshold[i] = 0;
    for (int i = 0; i < GNB; i++)
      GGEHL[i] = &GGEHLA[i][0];
    for (int i = 0; i < LNB; i++)
      LGEHL[i] = &LGEHLA[i][0];

    for (int i = 0; i < GNB; i++)
      for (int j = 0; j < ((1 << LOGGNB) - 1); j++)
        {
          if (!(j & 1))
            {
              GGEHL[i][j] = -1;

            }
        }
    for (int i = 0; i < LNB; i++)
      for (int j = 0; j < ((1 << LOGLNB) - 1); j++)
        {
          if (!(j & 1))
            {
              LGEHL[i][j] = -1;

            }
        }

    for (int i = 0; i < SNB; i++)
      SGEHL[i] = &SGEHLA[i][0];
    for (int i = 0; i < TNB; i++)
      TGEHL[i] = &TGEHLA[i][0];
    for (int i = 0; i < PNB; i++)
      PGEHL[i] = &PGEHLA[i][0];
#ifdef IMLI
#ifdef IMLIOH
    for (int i = 0; i < FNB; i++)
      FGEHL[i] = &FGEHLA[i][0];

    for (int i = 0; i < FNB; i++)
      for (int j = 0; j < ((1 << LOGFNB) - 1); j++)
        {
          if (!(j & 1))
            {
              FGEHL[i][j] = -1;

            }
        }
#endif
    for (int i = 0; i < INB; i++)
      IGEHL[i] = &IGEHLA[i][0];
    for (int i = 0; i < INB; i++)
      for (int j = 0; j < ((1 << LOGINB) - 1); j++)
        {
          if (!(j & 1))
            {
              IGEHL[i][j] = -1;

            }
        }
    for (int i = 0; i < IMNB; i++)
      IMGEHL[i] = &IMGEHLA[i][0];
    for (int i = 0; i < IMNB; i++)
      for (int j = 0; j < ((1 << LOGIMNB) - 1); j++)
        {
          if (!(j & 1))
            {
              IMGEHL[i][j] = -1;

            }
        }

#endif
    for (int i = 0; i < SNB; i++)
      for (int j = 0; j < ((1 << LOGSNB) - 1); j++)
        {
          if (!(j & 1))
            {
              SGEHL[i][j] = -1;

            }
        }
    for (int i = 0; i < TNB; i++)
      for (int j = 0; j < ((1 << LOGTNB) - 1); j++)
        {
          if (!(j & 1))
            {
              TGEHL[i][j] = -1;

            }
        }
    for (int i = 0; i < PNB; i++)
      for (int j = 0; j < ((1 << LOGPNB) - 1); j++)
        {
          if (!(j & 1))
            {
              PGEHL[i][j] = -1;

            }
        }


    for (int i = 0; i < (1 << LOGB); i++)
      {
        btable[i].pred = 0;
        btable[i].hyst = 1;
      }




    for (int j = 0; j < (1 << LOGBIAS); j++)
      {
        switch (j & 3)
          {
          case 0:
            BiasSK[j] = -8;
            break;
          case 1:
            BiasSK[j] = 7;
            break;
          case 2:
            BiasSK[j] = -32;

            break;
          case 3:
            BiasSK[j] = 31;
            break;
          }
      }
    for (int j = 0; j < (1 << LOGBIAS); j++)
      {
        switch (j & 3)
          {
          case 0:
            Bias[j] = -32;

            break;
          case 1:
            Bias[j] = 31;
            break;
          case 2:
            Bias[j] = -1;
            break;
          case 3:
            Bias[j] = 0;
            break;
          }
      }
    for (int j = 0; j < (1 << LOGBIAS); j++)
      {
        switch (j & 3)
          {
          case 0:
            BiasBank[j] = -32;

            break;
          case 1:
            BiasBank[j] = 31;
            break;
          case 2:
            BiasBank[j] = -1;
            break;
          case 3:
            BiasBank[j] = 0;
            break;
          }
      }
    for (int i = 0; i < SIZEUSEALT; i++)
      {
        use_alt_on_na[i] = 0;

      }
    for (int i = 0; i < (1 << LOGSIZEUPS); i++)
      {
        WG[i] = 7;
        WL[i] = 7;
        WS[i] = 7;
        WT[i] = 7;
        WP[i] = 7;
        WI[i] = 7;
        WB[i] = 4;
      }
    TICK = 0;
    for (int i = 0; i < NLOCAL; i++)
      {
        L_shist[i] = 0;
      }
    for (int i = 0; i < NSECLOCAL; i++)
      {
        S_slhist[i] = 0;

      }
    GHIST = 0;
    ptghist = 0;
    phist = 0;

  }




  // index function for the bimodal table

  int bindex (uint64_t PC)
  {
    return ((PC ^ (PC >> LOGB)) & ((1 << (LOGB)) - 1));
  }


// the index functions for the tagged tables uses path history as in the OGEHL predictor
//F serves to mix path history: not very important impact

  int F (long long A, int size, int bank)
  {
    int   A1, A2;
    A = A & ((1 << size) - 1);
    A1 = (A & ((1 << logg[bank]) - 1));
    A2 = (A >> logg[bank]);

    if (bank < logg[bank])
      A2 =
        ((A2 << bank) & ((1 << logg[bank]) - 1)) +
        (A2 >> (logg[bank] - bank));
    A = A1 ^ A2;
    if (bank < logg[bank])
      A =
        ((A << bank) & ((1 << logg[bank]) - 1)) + (A >> (logg[bank] - bank));
    return (A);
  }

// gindex computes a full hash of PC, ghist and phist
  int gindex (unsigned int PC, int bank, long long hist,
              folded_history * ch_i_)
  {
    int index;
    int M = (m[bank] > PHISTWIDTH) ? PHISTWIDTH : m[bank];
    index =
      PC ^ (PC >> (abs (logg[bank] - bank) + 1))
      ^ ch_i_[bank].comp ^ F (hist, M, bank);

    return (index & ((1 << (logg[bank])) - 1));
  }

  //  tag computation
  uint16_t gtag (unsigned int PC, int bank, folded_history * ch0,
                 folded_history * ch1)
  {
    int tag = (PC) ^ ch0[bank].comp ^ (ch1[bank].comp << 1);
    return (tag & ((1 << (TB[bank])) - 1));
  }

  // up-down saturating counter
  void ctrupdate (int8_t & ctr, bool taken, int nbits)
  {
    if (taken)
      {
        if (ctr < ((1 << (nbits - 1)) - 1))
          ctr++;
      }
    else
      {
        if (ctr > -(1 << (nbits - 1)))
          ctr--;
      }
  }


  bool getbim ()
  {
    BIM = (btable[BI].pred << 1) + (btable[BI >> HYSTSHIFT].hyst);
    HighConf = (BIM == 0) || (BIM == 3);
    LowConf = !HighConf;
    AltConf = HighConf;
    MedConf = false;
    return (btable[BI].pred > 0);
  }

  void baseupdate (bool Taken)
  {
    int inter = BIM;
    if (Taken)
      {
        if (inter < 3)
          inter += 1;
      }
    else if (inter > 0)
      inter--;
    btable[BI].pred = inter >> 1;
    btable[BI >> HYSTSHIFT].hyst = (inter & 1);
  };

//just a simple pseudo random number generator: use available information
// to allocate entries  in the loop predictor
  int MYRANDOM ()
  {
    Seed++;
    Seed ^= phist;
    Seed = (Seed >> 21) + (Seed << 11);
    Seed ^= ptghist;
    Seed = (Seed >> 10) + (Seed << 22);
    return (Seed);
  };


  //  TAGE PREDICTION: same code at fetch or retire time but the index and tags must recomputed
  void Tagepred (uint64_t PC)
  {
    HitBank = 0;
    AltBank = 0;
    for (int i = 1; i <= NHIST; i += 2)
      {
        GI[i] = gindex (PC, i, phist, ch_i);
        GTAG[i] = gtag (PC, i, ch_t[0], ch_t[1]);
        GTAG[i + 1] = GTAG[i];
        GI[i + 1] = GI[i] ^ (GTAG[i] & ((1 << LOGG) - 1));
      }
int T = (PC ^ (phist & ((1 << m[BORN]) - 1))) % NBANKHIGH;
//int T = (PC ^ phist) % NBANKHIGH;
    for (int i = BORN; i <= NHIST; i++)
      if (NOSKIP[i])
        {
          GI[i] += (T << LOGG);
          T++;
          T = T % NBANKHIGH;

        }
    T = (PC ^ (phist & ((1 << m[1]) - 1))) % NBANKLOW;

    for (int i = 1; i <= BORN - 1; i++)
      if (NOSKIP[i])
        {
          GI[i] += (T << LOGG);
          T++;
          T = T % NBANKLOW;

        }
    // Added by Kaifeng Xu
    if(is_ld_st == 0){
        tage_insertion(PC);
    }
    // End by Kaifeng Xu
//just do not forget most address are aligned on 4 bytes
    BI = (PC ^ (PC >> 2)) & ((1 << LOGB) - 1);

    {
      alttaken = getbim ();
      tage_pred = alttaken;
      LongestMatchPred = alttaken;
    }

//Look for the bank with longest matching history
    for (int i = NHIST; i > 0; i--)
      {
        if (NOSKIP[i])
          if (gtable[i][GI[i]].tag == GTAG[i])
            {
              HitBank = i;
              LongestMatchPred = (gtable[HitBank][GI[HitBank]].ctr >= 0);
              break;
            }
      }

//Look for the alternate bank
    for (int i = HitBank - 1; i > 0; i--)
      {
        if (NOSKIP[i])
          if (gtable[i][GI[i]].tag == GTAG[i])
            {

              AltBank = i;
              break;
            }
      }
//computes the prediction and the alternate prediction

    if (HitBank > 0)
      {
        if (AltBank > 0)
          {
            alttaken = (gtable[AltBank][GI[AltBank]].ctr >= 0);
            AltConf = (abs (2 * gtable[AltBank][GI[AltBank]].ctr + 1) > 1);

          }
        else
          alttaken = getbim ();

//if the entry is recognized as a newly allocated entry and 
//USE_ALT_ON_NA is positive  use the alternate prediction

        bool Huse_alt_on_na = (use_alt_on_na[INDUSEALT] >= 0);
        if ((!Huse_alt_on_na)
            || (abs (2 * gtable[HitBank][GI[HitBank]].ctr + 1) > 1))
          tage_pred = LongestMatchPred;
        else
          tage_pred = alttaken;

        HighConf =
          (abs (2 * gtable[HitBank][GI[HitBank]].ctr + 1) >=
           (1 << CWIDTH) - 1);
        LowConf = (abs (2 * gtable[HitBank][GI[HitBank]].ctr + 1) == 1);
        MedConf = (abs (2 * gtable[HitBank][GI[HitBank]].ctr + 1) == 5);

      }
  }


//compute the prediction
  bool GetPrediction (uint64_t PC)
  {
// computes the TAGE table addresses and the partial tags
//
    // Added by Kaifeng Xu
    use_SC = 0;
    // End Kaifeng XU

    Tagepred (PC);
    pred_taken = tage_pred;
#ifndef SC
    return (tage_pred);
#endif

#ifdef LOOPPREDICTOR
    predloop = getloop (PC);    // loop prediction
    pred_taken = ((WITHLOOP >= 0) && (LVALID)) ? predloop : pred_taken;
#endif
    pred_inter = pred_taken;

//Compute the SC prediction

    LSUM = 0;

//integrate BIAS prediction   
    int8_t ctr = Bias[INDBIAS];

    LSUM += (2 * ctr + 1);
    ctr = BiasSK[INDBIASSK];
    LSUM += (2 * ctr + 1);
    ctr = BiasBank[INDBIASBANK];
    LSUM += (2 * ctr + 1);
#ifdef VARTHRES
    LSUM = (1 + (WB[INDUPDS] >= 0)) * LSUM;
#endif
//integrate the GEHL predictions
    LSUM +=
      Gpredict ((PC << 1) + pred_inter, GHIST, Gm, GGEHL, GNB, LOGGNB, WG);
    LSUM += Gpredict (PC, phist, Pm, PGEHL, PNB, LOGPNB, WP);
#ifdef LOCALH
    LSUM += Gpredict (PC, L_shist[INDLOCAL], Lm, LGEHL, LNB, LOGLNB, WL);
#ifdef LOCALS
    LSUM += Gpredict (PC, S_slhist[INDSLOCAL], Sm, SGEHL, SNB, LOGSNB, WS);
#endif
#ifdef LOCALT
    LSUM += Gpredict (PC, T_slhist[INDTLOCAL], Tm, TGEHL, TNB, LOGTNB, WT);
#endif
#endif

#ifdef IMLI
    LSUM +=
      Gpredict (PC, IMHIST[(IMLIcount)], IMm, IMGEHL, IMNB, LOGIMNB, WIM);
    LSUM += Gpredict (PC, IMLIcount, Im, IGEHL, INB, LOGINB, WI);
#endif
    bool SCPRED = (LSUM >= 0);
//just  an heuristic if the respective contribution of component groups can be multiplied by 2 or not
    THRES = (updatethreshold>>3)+Pupdatethreshold[INDUPD]
#ifdef VARTHRES
      + 12 * ((WB[INDUPDS] >= 0) + (WP[INDUPDS] >= 0)
#ifdef LOCALH
              + (WS[INDUPDS] >= 0) + (WT[INDUPDS] >= 0) + (WL[INDUPDS] >= 0)
#endif
              + (WG[INDUPDS] >= 0)
#ifdef IMLI
              + (WI[INDUPDS] >= 0)
#endif
      )
#endif
      ;

    //Minimal benefit in trying to avoid accuracy loss on low confidence SC prediction and  high/medium confidence on TAGE
    // but just uses 2 counters 0.3 % MPKI reduction
    if (pred_inter != SCPRED)
      {
//Choser uses TAGE confidence and |LSUM|
        pred_taken = SCPRED;
        use_SC = 1;
        if (HighConf)
          {
            if ((abs (LSUM) < THRES / 4))
              {
                pred_taken = pred_inter;
                use_SC = 0;
              }

            else if ((abs (LSUM) < THRES / 2)){
              pred_taken = (SecondH < 0) ? SCPRED : pred_inter;
              use_SC = (SecondH < 0);
            }
          }

        if (MedConf)
          if ((abs (LSUM) < THRES / 4))
            {
              pred_taken = (FirstH < 0) ? SCPRED : pred_inter;
              use_SC = (FirstH < 0);
            }

      }

    // Added By Kaifeng Xu
    // if(HitBank >= NHIST - 1){
    //     if(gtable[HitBank][GI[HitBank]].is_prefetched){
    //         pred_taken = tage_pred;
    //         use_SC = 2;
    //     }
    // }
    tage_sc_l_taken = pred_taken; // Sotre tage_sc_l prediction, may use TAGE prefetched prediction
    if((insert_taken >= 0) && (prefetch_useful > 0)){
        pred_taken = insert_taken;
        use_SC = 2;
    }
    // Add local history lookup
    // for(int i = 0; i < PPC_TABLE_ENTRY_NUM; i++){
    //     if(PPCTable.entries[i].pc == PC){
    //         PPCTable_idx = i;
    //         for(int j = 0; j < TAGE_MISS_TABLE_ENTRY_NUM; j++){
    //             if(missTable.entries[i].valid && (PPCTable.entries[i].local_history == missTable.entries[i].local_history)){
    //                 // Hit in missTable, use local history to decide
    //                 pred_taken = missTable.entries[i].taken;
    //             }
    //         }
    //     } else {
    //         PPCTable_idx = -1; // Set an invalid number 
    //     }

    // }
    // End of Kaifeng Xu

    return pred_taken;
  }

  void HistoryUpdate (uint64_t PC, OpType opType, bool taken,
                      uint64_t target, long long &X, int &Y,
                      folded_history * H, folded_history * G,
                      folded_history * J)
  {
    int brtype = 0;

    switch (opType)
      {
      case OPTYPE_RET_UNCOND:
      case OPTYPE_JMP_INDIRECT_UNCOND:
      case OPTYPE_JMP_INDIRECT_COND:
      case OPTYPE_CALL_INDIRECT_UNCOND:
      case OPTYPE_CALL_INDIRECT_COND:
      case OPTYPE_RET_COND:
        brtype = 2;
        break;
      case OPTYPE_JMP_DIRECT_COND:
      case OPTYPE_CALL_DIRECT_COND:
      case OPTYPE_JMP_DIRECT_UNCOND:
      case OPTYPE_CALL_DIRECT_UNCOND:
        brtype = 0;
        break;
      default:
        exit (1);
      }
    switch (opType)
      {
      case OPTYPE_JMP_DIRECT_COND:
      case OPTYPE_CALL_DIRECT_COND:
      case OPTYPE_JMP_INDIRECT_COND:
      case OPTYPE_CALL_INDIRECT_COND:
      case OPTYPE_RET_COND:
        brtype += 1;
        break;

      }


//special treatment for indirect  branchs;
    int maxt = 2;
    if (brtype & 1)
      maxt = 2;
    else if ((brtype & 2) )
      maxt = 3;

#ifdef IMLI
    if (brtype & 1)
      {
#ifdef IMLI
        IMHIST[IMLIcount] = (IMHIST[IMLIcount] << 1) + taken;
#endif
        if (target < PC)

          {
//This branch corresponds to a loop
            if (!taken)
              {
//exit of the "loop"
                IMLIcount = 0;

              }
            if (taken)
              {

                if (IMLIcount < ((1 << Im[0]) - 1))
                  IMLIcount++;
              }
          }
      }


#endif

    if (brtype & 1)
      {
        GHIST = (GHIST << 1) + (taken & (target < PC));
        L_shist[INDLOCAL] = (L_shist[INDLOCAL] << 1) + (taken);
        S_slhist[INDSLOCAL] =
          ((S_slhist[INDSLOCAL] << 1) + taken) ^ (PC & 15);
        T_slhist[INDTLOCAL] = (T_slhist[INDTLOCAL] << 1) + taken;
      }


    int T = ((PC ^ (PC >> 2))) ^ taken;
    int PATH = PC ^ (PC >> 2) ^ (PC >> 4);
    if ((brtype == 3) & taken)
      {
        T = (T ^ (target >> 2));
        PATH = PATH ^ (target >> 2) ^ (target >> 4);
      }

    for (int t = 0; t < maxt; t++)
      {
        bool DIR = (T & 1);
        T >>= 1;
        int PATHBIT = (PATH & 127);
        PATH >>= 1;
//update  history
        Y--;
        ghist[Y & (HISTBUFFERLENGTH - 1)] = DIR;
        X = (X << 1) ^ PATHBIT;


        for (int i = 1; i <= NHIST; i++)
          {

            H[i].update (ghist, Y);
            G[i].update (ghist, Y);
            J[i].update (ghist, Y);


          }
      }

    X = (X & ((1<<PHISTWIDTH)-1));
    
//END UPDATE  HISTORIES
  }

// PREDICTOR UPDATE

  void UpdatePredictor (uint64_t PC, OpType opType, bool resolveDir,
                        bool predDir, uint64_t branchTarget, bool is_update_his)
  {

    // Added By Kaifeng Xu
    if (is_update_his) {
        // Decide which component is used, using tage predictor
        char predict_component = 'T';
        if(LVALID && (WITHLOOP >= 0)) predict_component = 'L';
        else if(use_SC == 1) predict_component = 'S';
        else if(use_SC == 2) predict_component = 'P';
        printf("ip %016llx %c %c %d %d ", PC, predict_component, ((resolveDir == pred_taken) ? 'H': 'M'), resolveDir, HitBank);
        printf("%d %016llx %d %u %d %u\n", opType, branchTarget, GI[NHIST-1], GTAG[NHIST-1], GI[NHIST], GTAG[NHIST]);
        // for(int i = 0; i < HISTBUFFERLENGTH ; i +=4 ){
        //     int tmp_ptghist = ptghist - i - 1;
        //     int hex_out = ghist[tmp_ptghist & (HISTBUFFERLENGTH - 1)] << 3;
        //     hex_out ^= ghist[(tmp_ptghist - 1) & (HISTBUFFERLENGTH - 1)] << 2;
        //     hex_out ^= ghist[(tmp_ptghist - 2) & (HISTBUFFERLENGTH - 1)] << 1;
        //     hex_out ^= ghist[(tmp_ptghist - 3) & (HISTBUFFERLENGTH - 1)];
        //     printf("%x", hex_out);
        // }
        // printf("\n");
        // Update usefulness in prefetchBuffer/Table
        if(insert_taken >= 0) {
            if(resolveDir == insert_taken){
                if(prefetchBuffer_idx >= 0) {
                    prefetchBuffer[prefetchBuffer_idx][4] += 1;
                    if(prefetchBuffer[prefetchBuffer_idx][4] >= 6){
                        prefetchBuffer[prefetchBuffer_idx][4] = 6;
                    }
                }
                if(prefetchTable_idx >= 0) {
                    prefetchTable[PC][prefetchTable_idx][5] += 1;
                    if(prefetchTable[PC][prefetchTable_idx][5] >= 6){
                        prefetchTable[PC][prefetchTable_idx][5] = 6;
                    }
                }
            } else {
                if(prefetchBuffer_idx >= 0) {
                    if(prefetchBuffer[prefetchBuffer_idx][4] <= 1){
                        prefetchBuffer[prefetchBuffer_idx][4] = 0;
                    } else {
                        prefetchBuffer[prefetchBuffer_idx][4] -= 1;
                    }
                }
                if(prefetchTable_idx >= 0) {
                    if(prefetchTable[PC][prefetchTable_idx][5] <= 1){
                        prefetchTable[PC][prefetchTable_idx][5] = 0;
                    } else {
                        prefetchTable[PC][prefetchTable_idx][5] -=1;
                    }
                }
            }
        }
        pred_taken = tage_sc_l_taken; // restore tage_sc_l prediction
    } 
    // Tmp vars for storing the misses
    int num_stored = 0;
    int tmp_bank_idx = -1;
    int tmp_table_idx;
    uint tmp_tag;
    // End Kaifeng Xu

#ifdef SC
#ifdef LOOPPREDICTOR
    if (LVALID)
      {
        if (pred_taken != predloop)
          ctrupdate (WITHLOOP, (predloop == resolveDir), 7);
      }
    loopupdate (PC, resolveDir, (pred_taken != resolveDir));
#endif

    bool SCPRED = (LSUM >= 0);
    if (pred_inter != SCPRED)
      {
        if ((abs (LSUM) < THRES))
          if ((HighConf))
            {


              if ((abs (LSUM) < THRES / 2))
                if ((abs (LSUM) >= THRES / 4))
                  ctrupdate (SecondH, (pred_inter == resolveDir), CONFWIDTH);
            }
        if ((MedConf))
          if ((abs (LSUM) < THRES / 4))
            {
              ctrupdate (FirstH, (pred_inter == resolveDir), CONFWIDTH);
            }
      }

    if ((SCPRED != resolveDir) || ((abs (LSUM) < THRES)))
      {
        {
          if (SCPRED != resolveDir)
          {Pupdatethreshold[INDUPD] += 1;updatethreshold+=1;
          }
          
          else
          {Pupdatethreshold[INDUPD] -= 1;updatethreshold -= 1;
          }
          

          if (Pupdatethreshold[INDUPD] >= (1 << (WIDTHRESP - 1)))
            Pupdatethreshold[INDUPD] = (1 << (WIDTHRESP - 1)) - 1;
//Pupdatethreshold[INDUPD] could be negative
          if (Pupdatethreshold[INDUPD] < -(1 << (WIDTHRESP - 1)))
            Pupdatethreshold[INDUPD] = -(1 << (WIDTHRESP - 1));
          if (updatethreshold >= (1 << (WIDTHRES - 1)))
            updatethreshold = (1 << (WIDTHRES - 1)) - 1;
//updatethreshold could be negative
          if (updatethreshold < -(1 << (WIDTHRES - 1)))
            updatethreshold = -(1 << (WIDTHRES - 1));
        }
#ifdef VARTHRES
        {
          int XSUM =
            LSUM - ((WB[INDUPDS] >= 0) * ((2 * Bias[INDBIAS] + 1) +
                                          (2 * BiasSK[INDBIASSK] + 1) +
                                          (2 * BiasBank[INDBIASBANK] + 1)));
          if ((XSUM +
               ((2 * Bias[INDBIAS] + 1) + (2 * BiasSK[INDBIASSK] + 1) +
                (2 * BiasBank[INDBIASBANK] + 1)) >= 0) != (XSUM >= 0))
            ctrupdate (WB[INDUPDS],
                       (((2 * Bias[INDBIAS] + 1) +
                         (2 * BiasSK[INDBIASSK] + 1) +
                         (2 * BiasBank[INDBIASBANK] + 1) >= 0) == resolveDir),
                       EWIDTH);
        }
#endif
        ctrupdate (Bias[INDBIAS], resolveDir, PERCWIDTH);
        ctrupdate (BiasSK[INDBIASSK], resolveDir, PERCWIDTH);
        ctrupdate (BiasBank[INDBIASBANK], resolveDir, PERCWIDTH);
        Gupdate ((PC << 1) + pred_inter, resolveDir,
                 GHIST, Gm, GGEHL, GNB, LOGGNB, WG);
        Gupdate (PC, resolveDir, phist, Pm, PGEHL, PNB, LOGPNB, WP);
#ifdef LOCALH
        Gupdate (PC, resolveDir, L_shist[INDLOCAL], Lm, LGEHL, LNB, LOGLNB,
                 WL);
#ifdef LOCALS
        Gupdate (PC, resolveDir, S_slhist[INDSLOCAL], Sm,
                 SGEHL, SNB, LOGSNB, WS);
#endif
#ifdef LOCALT

        Gupdate (PC, resolveDir, T_slhist[INDTLOCAL], Tm, TGEHL, TNB, LOGTNB,
                 WT);
#endif
#endif


#ifdef IMLI
        Gupdate (PC, resolveDir, IMHIST[(IMLIcount)], IMm, IMGEHL, IMNB,
                 LOGIMNB, WIM);
        Gupdate (PC, resolveDir, IMLIcount, Im, IGEHL, INB, LOGINB, WI);
#endif



      }
#endif

//TAGE UPDATE
    bool ALLOC = ((tage_pred != resolveDir) & (HitBank < NHIST));


    //do not allocate too often if the overall prediction is correct 

    if (HitBank > 0)
      {
// Manage the selection between longest matching and alternate matching
// for "pseudo"-newly allocated longest matching entry
        // this is extremely important for TAGE only, not that important when the overall predictor is implemented 
        bool PseudoNewAlloc =
          (abs (2 * gtable[HitBank][GI[HitBank]].ctr + 1) <= 1);
// an entry is considered as newly allocated if its prediction counter is weak
        if (PseudoNewAlloc)
          {
            if (LongestMatchPred == resolveDir)
              ALLOC = false;
// if it was delivering the correct prediction, no need to allocate a new entry
//even if the overall prediction was false


            if (LongestMatchPred != alttaken)
              {
                ctrupdate (use_alt_on_na[INDUSEALT], (alttaken == resolveDir),
                           ALTWIDTH);
              }



          }


      }

    if (pred_taken == resolveDir)
      if ((MYRANDOM () & 31) != 0)
        ALLOC = false;

    if (ALLOC)
      {

        int T = NNN;

        int A = 1;
        if ((MYRANDOM () & 127) < 32)
          A = 2;
        int Penalty = 0;
        int NA = 0;
        int DEP = ((((HitBank - 1 + 2 * A) & 0xffe)) ^ (MYRANDOM () & 1));
// just a complex formula to chose between X and X+1, when X is odd: sorry

        for (int I = DEP; I < NHIST; I += 2)
          {
            int i = I + 1;
            bool Done = false;
            if (NOSKIP[i])
              {
                if (gtable[i][GI[i]].u == 0)

                  {
#define OPTREMP
// the replacement is optimized with a single u bit: 0.2 %
#ifdef OPTREMP
                    if (abs (2 * gtable[i][GI[i]].ctr + 1) <= 3)
#endif
                      {
                        gtable[i][GI[i]].tag = GTAG[i];
                        gtable[i][GI[i]].ctr = (resolveDir) ? 0 : -1;
                        gtable[i][GI[i]].is_prefetched = 0;
                        if((is_ld_st == 1) && (num_stored < NUM_STORED_ENTRY)){
                            store_table(i, GI[i], GTAG[i], resolveDir);
                            num_stored++;
                            tmp_bank_idx = i;
                            tmp_table_idx = GI[i];
                            tmp_tag = GTAG[i];
                        }
                        NA++;
                        if (T <= 0)
                          {
                            break;
                          }
                        I += 2;
                        Done = true;
                        T -= 1;
                      }
#ifdef OPTREMP
                    else
                      {
                        if (gtable[i][GI[i]].ctr > 0)
                          gtable[i][GI[i]].ctr--;
                        else
                          gtable[i][GI[i]].ctr++;
                      }

#endif

                  }



                else
                  {
                    Penalty++;
                  }
              }

            if (!Done)
              {
                i = (I ^ 1) + 1;
                if (NOSKIP[i])
                  {

                    if (gtable[i][GI[i]].u == 0)
                      {
#ifdef OPTREMP
                        if (abs (2 * gtable[i][GI[i]].ctr + 1) <= 3)
#endif

                          {
                            gtable[i][GI[i]].tag = GTAG[i];
                            gtable[i][GI[i]].ctr = (resolveDir) ? 0 : -1;
                            gtable[i][GI[i]].is_prefetched = 0;
                            if((is_ld_st == 1) && (num_stored < NUM_STORED_ENTRY)){
                                store_table(i, GI[i], GTAG[i], resolveDir);
                                num_stored++;
                                tmp_bank_idx = i;
                                tmp_table_idx = GI[i];
                                tmp_tag = GTAG[i];
                            }
                            NA++;
                            if (T <= 0)
                              {
                                break;
                              }
                            I += 2;
                            T -= 1;
                          }
#ifdef OPTREMP
                        else
                          {
                            if (gtable[i][GI[i]].ctr > 0)
                              gtable[i][GI[i]].ctr--;
                            else
                              gtable[i][GI[i]].ctr++;
                          }

#endif


                      }
                    else
                      {
                        Penalty++;
                      }
                  }

              }

          }
        TICK += (Penalty - 2 * NA);


//just the best formula for the Championship:
        //In practice when one out of two entries are useful
        if (TICK < 0)
          TICK = 0;
        if (TICK >= BORNTICK)
          {

            for (int i = 1; i <= BORN; i += BORN - 1)
              for (int j = 0; j < SizeTable[i]; j++)
                gtable[i][j].u >>= 1;
            TICK = 0;


          }
      }

//update predictions
    if (HitBank > 0)
      {
        if (abs (2 * gtable[HitBank][GI[HitBank]].ctr + 1) == 1)
          if (LongestMatchPred != resolveDir)

            {                   // acts as a protection 
              if (AltBank > 0)
                {
                  ctrupdate (gtable[AltBank][GI[AltBank]].ctr,
                             resolveDir, CWIDTH);
                }
              if (AltBank == 0)
                baseupdate (resolveDir);

            }
        ctrupdate (gtable[HitBank][GI[HitBank]].ctr, resolveDir, CWIDTH);
//sign changes: no way it can have been useful
        if (abs (2 * gtable[HitBank][GI[HitBank]].ctr + 1) == 1)
          gtable[HitBank][GI[HitBank]].u = 0;
        if (alttaken == resolveDir)
          if (AltBank > 0)
            if (abs (2 * gtable[AltBank][GI[AltBank]].ctr + 1) == 7)
              if (gtable[HitBank][GI[HitBank]].u == 1)
                {
                  if (LongestMatchPred == resolveDir)
                    {
                      gtable[HitBank][GI[HitBank]].u = 0;
                    }
                }
      }

    else
      baseupdate (resolveDir);

    if (LongestMatchPred != alttaken)
      if (LongestMatchPred == resolveDir)
        {
          if (gtable[HitBank][GI[HitBank]].u < (1 << UWIDTH) - 1)
            gtable[HitBank][GI[HitBank]].u++;
        }
//END TAGE UPDATE


    if (is_update_his){
        HistoryUpdate (PC, opType, resolveDir, branchTarget,
                       phist, ptghist, ch_i, ch_t[0], ch_t[1]);
    }

//     // Start of Kaifeng Xu
//     // Store/Load Entries
//     if ((tage_pred != resolveDir) && is_update_his && (is_ld_st == 1)) {
//         if(num_stored < NUM_STORED_ENTRY) {
//             // No entry stored, then randomly store
//             int start_bank = (num_stored == 0) ? (NHIST/2 + 1) : (tmp_bank_idx + 1);
//             for(int I = start_bank; I < NHIST; I += 2 ){
//                 int i = I + MYRANDOM() % 2;
//                 if(NOSKIP[i]) {
//                     // store_table(tmp_bank_idx, tmp_table_idx, tmp_tag, resolveDir);
//                     store_table(i, GI[i], GTAG[i], resolveDir);
//                     num_stored ++;
//                 }
//                 if(num_stored >= NUM_STORED_ENTRY) break;
//             }
//             for(; num_stored < NUM_STORED_ENTRY; num_stored++){
//                 int i = NHIST;
//                 store_table(i, GI[i], GTAG[i], resolveDir);
//             }
//         }
//     }
//     if(num_stored != 0 && num_stored != NUM_STORED_ENTRY){
//         std::cerr << "Invalid Number of stored entries:"<< num_stored << "ALLOC: " << ALLOC << endl;
//     }
//     // tmp counter
//     if (is_update_his && continue_prefetch){
//         if(is_ld_st == 0) {
//             for( ; continue_prefetch ; ){
//                 continue_prefetch = tage_insertion();
//             }
//         }
//     }
//     if (is_update_his) tmp_counter ++;
//     if (tmp_counter % 1000 == 0){
//         continue_prefetch = true;
//         if((is_ld_st == 1) && (tmp_counter >= 10000)) store_insn_breaker();
//     }
//     // End of Kaifeng Xu

//END PREDICTOR UPDATE


  }
#define GINDEX (((long long) PC) ^ bhist ^ (bhist >> (8 - i)) ^ (bhist >> (16 - 2 * i)) ^ (bhist >> (24 - 3 * i)) ^ (bhist >> (32 - 3 * i)) ^ (bhist >> (40 - 4 * i))) & ((1 << (logs - (i >= (NBR - 2)))) - 1)
  int Gpredict (uint64_t PC, long long BHIST, int *length,
                int8_t ** tab, int NBR, int logs, int8_t * W)
  {
    int PERCSUM = 0;
    for (int i = 0; i < NBR; i++)
      {
        long long bhist = BHIST & ((long long) ((1 << length[i]) - 1));
        long long index = GINDEX;

        int8_t ctr = tab[i][index];

        PERCSUM += (2 * ctr + 1);


      }
#ifdef VARTHRES
    PERCSUM = (1 + (W[INDUPDS] >= 0)) * PERCSUM;
#endif
    return ((PERCSUM));
  }
  void Gupdate (uint64_t PC, bool taken, long long BHIST, int *length,
                int8_t ** tab, int NBR, int logs, int8_t * W)
  {

    int PERCSUM = 0;

    for (int i = 0; i < NBR; i++)
      {
        long long bhist = BHIST & ((long long) ((1 << length[i]) - 1));
        long long index = GINDEX;

        PERCSUM += (2 * tab[i][index] + 1);
        ctrupdate (tab[i][index], taken, PERCWIDTH);
      }
#ifdef VARTHRES
    {
      int XSUM = LSUM - ((W[INDUPDS] >= 0)) * PERCSUM;
      if ((XSUM + PERCSUM >= 0) != (XSUM >= 0))
        ctrupdate (W[INDUPDS], ((PERCSUM >= 0) == taken), EWIDTH);
    }
#endif
  }


  void TrackOtherInst (uint64_t PC, OpType opType, bool taken,
                       uint64_t branchTarget)
  {


    HistoryUpdate (PC, opType, taken, branchTarget, phist,
                   ptghist, ch_i, ch_t[0], ch_t[1]);



  }

#ifdef LOOPPREDICTOR
  int lindex (uint64_t PC)
  {
    return (((PC ^ (PC >> 2)) & ((1 << (LOGL - 2)) - 1)) << 2);
  }


//loop prediction: only used if high confidence
//skewed associative 4-way
//At fetch time: speculative
#define CONFLOOP 15
  bool getloop (uint64_t PC)
  {
    LHIT = -1;

    LI = lindex (PC);
    LIB = ((PC >> (LOGL - 2)) & ((1 << (LOGL - 2)) - 1));
    LTAG = (PC >> (LOGL - 2)) & ((1 << 2 * LOOPTAG) - 1);
    LTAG ^= (LTAG >> LOOPTAG);
    LTAG = (LTAG & ((1 << LOOPTAG) - 1));

    for (int i = 0; i < 4; i++)
      {
        int index = (LI ^ ((LIB >> i) << 2)) + i;

        if (ltable[index].TAG == LTAG)
          {
            LHIT = i;
            LVALID = ((ltable[index].confid == CONFLOOP)
                      || (ltable[index].confid * ltable[index].NbIter > 128));


            if (ltable[index].CurrentIter + 1 == ltable[index].NbIter)
              return (!(ltable[index].dir));
            return ((ltable[index].dir));

          }
      }

    LVALID = false;
    return (false);

  }



  void loopupdate (uint64_t PC, bool Taken, bool ALLOC)
  {
    if (LHIT >= 0)
      {
        int index = (LI ^ ((LIB >> LHIT) << 2)) + LHIT;
//already a hit 
        if (LVALID)
          {
            if (Taken != predloop)
              {
// free the entry
                ltable[index].NbIter = 0;
                ltable[index].age = 0;
                ltable[index].confid = 0;
                ltable[index].CurrentIter = 0;
                return;

              }
            else if ((predloop != tage_pred) || ((MYRANDOM () & 7) == 0))
              if (ltable[index].age < CONFLOOP)
                ltable[index].age++;
          }

        ltable[index].CurrentIter++;
        ltable[index].CurrentIter &= ((1 << WIDTHNBITERLOOP) - 1);
        //loop with more than 2** WIDTHNBITERLOOP iterations are not treated correctly; but who cares :-)
        if (ltable[index].CurrentIter > ltable[index].NbIter)
          {
            ltable[index].confid = 0;
            ltable[index].NbIter = 0;
//treat like the 1st encounter of the loop 
          }
        if (Taken != ltable[index].dir)
          {
            if (ltable[index].CurrentIter == ltable[index].NbIter)
              {
                if (ltable[index].confid < CONFLOOP)
                  ltable[index].confid++;
                if (ltable[index].NbIter < 3)
                  //just do not predict when the loop count is 1 or 2     
                  {
// free the entry
                    ltable[index].dir = Taken;
                    ltable[index].NbIter = 0;
                    ltable[index].age = 0;
                    ltable[index].confid = 0;
                  }
              }
            else
              {
                if (ltable[index].NbIter == 0)
                  {
// first complete nest;
                    ltable[index].confid = 0;
                    ltable[index].NbIter = ltable[index].CurrentIter;
                  }
                else
                  {
//not the same number of iterations as last time: free the entry
                    ltable[index].NbIter = 0;
                    ltable[index].confid = 0;
                  }
              }
            ltable[index].CurrentIter = 0;
          }

      }
    else if (ALLOC)

      {
        uint64_t X = MYRANDOM () & 3;

        if ((MYRANDOM () & 3) == 0)
          for (int i = 0; i < 4; i++)
            {
              int LHIT_ = (X + i) & 3;
              int index = (LI ^ ((LIB >> LHIT_) << 2)) + LHIT_;
              if (ltable[index].age == 0)
                {
                  ltable[index].dir = !Taken;
// most of mispredictions are on last iterations
                  ltable[index].TAG = LTAG;
                  ltable[index].NbIter = 0;
                  ltable[index].age = 7;
                  ltable[index].confid = 0;
                  ltable[index].CurrentIter = 0;
                  break;

                }
              else
                ltable[index].age--;
              break;
            }
      }
  }
#endif
  int
  predictorsize ()
  {
    int STORAGESIZE = 0;
    int inter = 0;
  
  
    STORAGESIZE +=
      NBANKHIGH * (1 << (logg[BORN])) * (CWIDTH + UWIDTH + TB[BORN]);
    STORAGESIZE += NBANKLOW * (1 << (logg[1])) * (CWIDTH + UWIDTH + TB[1]);
  
    STORAGESIZE += (SIZEUSEALT) * ALTWIDTH;
    STORAGESIZE += (1 << LOGB) + (1 << (LOGB - HYSTSHIFT));
    STORAGESIZE += m[NHIST];
    STORAGESIZE += PHISTWIDTH;
    STORAGESIZE += 10;          //the TICK counter
  
    fprintf (stderr, " (TAGE %d) ", STORAGESIZE);
  #ifdef SC
  #ifdef LOOPPREDICTOR
  
    inter = (1 << LOGL) * (2 * WIDTHNBITERLOOP + LOOPTAG + 4 + 4 + 1);
    fprintf (stderr, " (LOOP %d) ", inter);
    STORAGESIZE += inter;
  
  #endif
  
    inter += WIDTHRES;
    inter = WIDTHRESP * ((1 << LOGSIZEUP));     //the update threshold counters
    inter += 3 * EWIDTH * (1 << LOGSIZEUPS);    // the extra weight of the partial sums
    inter += (PERCWIDTH) * 3 * (1 << (LOGBIAS));
  
    inter +=
      (GNB - 2) * (1 << (LOGGNB)) * (PERCWIDTH) +
      (1 << (LOGGNB - 1)) * (2 * PERCWIDTH);
    inter += Gm[0];             //global histories for SC
    inter += (PNB - 2) * (1 << (LOGPNB)) * (PERCWIDTH) +
      (1 << (LOGPNB - 1)) * (2 * PERCWIDTH);
  //we use phist already counted for these tables
  
  #ifdef LOCALH
    inter +=
      (LNB - 2) * (1 << (LOGLNB)) * (PERCWIDTH) +
      (1 << (LOGLNB - 1)) * (2 * PERCWIDTH);
    inter += NLOCAL * Lm[0];
    inter += EWIDTH * (1 << LOGSIZEUPS);
  #ifdef LOCALS
    inter +=
      (SNB - 2) * (1 << (LOGSNB)) * (PERCWIDTH) +
      (1 << (LOGSNB - 1)) * (2 * PERCWIDTH);
    inter += NSECLOCAL * (Sm[0]);
    inter += EWIDTH * (1 << LOGSIZEUPS);
  
  #endif
  #ifdef LOCALT
    inter +=
      (TNB - 2) * (1 << (LOGTNB)) * (PERCWIDTH) +
      (1 << (LOGTNB - 1)) * (2 * PERCWIDTH);
    inter += NTLOCAL * Tm[0];
    inter += EWIDTH * (1 << LOGSIZEUPS);
  #endif
  
  
  
  
  
  
  
  
  
  #endif
  
  
  
  #ifdef IMLI
  
    inter += (1 << (LOGINB - 1)) * PERCWIDTH;
    inter += Im[0];
  
    inter += IMNB * (1 << (LOGIMNB - 1)) * PERCWIDTH;
    inter += 2 * EWIDTH * (1 << LOGSIZEUPS);    // the extra weight of the partial sums
    inter += 256 * IMm[0];
  #endif
    inter += 2 * CONFWIDTH;     //the 2 counters in the choser
    STORAGESIZE += inter;
  
  
    fprintf (stderr, " (SC %d) ", inter);
  #endif
  #ifdef PRINTSIZE
    fprintf (stderr, " (TOTAL %d bits %d Kbits) ", STORAGESIZE,
           STORAGESIZE / 1024);
    fprintf (stdout, " (TOTAL %d bits %d Kbits) ", STORAGESIZE,
           STORAGESIZE / 1024);
  #endif
  
  
    return (STORAGESIZE);
  
  
  }
};



// struct tage_sc_l : champsim::modules::branch_predictor {
//   using branch_predictor::branch_predictor;
//   bool predict_branch(uint64_t pc);
//   void last_branch_result(uint64_t pc, uint64_t branch_target, uint8_t taken, uint8_t branch_type);
//   PREDICTOR tage;
// 
// };




#endif
