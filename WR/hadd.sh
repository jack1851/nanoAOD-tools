#!/bin/bash

# Define path for job directories
BASE_PATH=/uscms/home/bjackson/nobackup/WR/DY_NANOAOD/WR_ANALYZE
NEW_PATH=/uscms/home/bjackson/nobackup/WR/DY_NANOAOD/CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/WR/hists
mkdir -p $BASE_PATH

# Set processes
PROCESSES=( \
    DYJetsToLL_M-50_HT-70to100 \
    DYJetsToLL_M-50_HT-100to200 \
    DYJetsToLL_M-50_HT-200to400 \
    DYJetsToLL_M-50_HT-400to600 \
    DYJetsToLL_M-50_HT-600to800 \
    DYJetsToLL_M-50_HT-800to1200 \
    DYJetsToLL_M-50_HT-1200to2500 \
    DYJetsToLL_M-50_HT-2500toinf \
    )

# Submit jobs
THIS_PWD=$PWD
for PROCESS in ${PROCESSES[@]}
do
    cd $NEW_PATH
    rm ${PROCESS}.root
    echo "${PROCESS}.root removed."
    cd $BASE_PATH/$PROCESS
    hadd -fk ${PROCESS}.root *.root    
    mv ${PROCESS}.root $NEW_PATH
    cd $THIS_PWD
done
