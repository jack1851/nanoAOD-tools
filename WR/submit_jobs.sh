#!/bin/bash

# Define path for job directories
BASE_PATH=/uscms/home/bjackson/nobackup/WR/DY_NANOAOD/WR_ANALYZE
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

# Create JDL files and job directories
for PROCESS in ${PROCESSES[@]}
do
    python create_job.py $PROCESS $BASE_PATH
done

# Submit jobs
THIS_PWD=$PWD
for PROCESS in ${PROCESSES[@]}
do
    cd $BASE_PATH/$PROCESS
    condor_submit job.jdl
    cd $THIS_PWD
done
