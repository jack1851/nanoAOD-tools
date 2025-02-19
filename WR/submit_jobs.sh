#!/bin/bash

# Define path for job directories
BASE_PATH=/uscms/home/bjackson/nobackup/WR/DY_NANOAOD/WR_ANALYZE
mkdir -p $BASE_PATH

# Full set of processes
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

#Copy the tarball
cd /uscms/home/bjackson/nobackup/WR/DY_NANOAOD
echo "Creating tarball of working directory. Wait approx 30 seconds..."
tar --exclude='CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/WR/reweighting_variables/*' -czvf CMSSW_DYNANO.tar.gz CMSSW_10_6_18
#tar --exclude='CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/WR/reweighting_variables/2Dhistos' --exclude='CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/WR/reweighting_variables/ptjjovermjj' --exclude='CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/WR/reweighting_variables/dijet_pt' --exclude='CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/WR/reweighting_variables/leadjet_pt' --exclude='CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/WR/reweighting_variables/leadlepton_pt' --exclude='CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/WR/reweighting_variables/dilepton_pt' --exclude='CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/WR/reweighting_variables/dijet_mass' --exclude='CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/WR/reweighting_variables/ptllovermll' -czvf CMSSW_DYNANO.tar.gz CMSSW_10_6_18
echo "Tarball created. Submitting scripts."
for PROCESS in ${PROCESSES[@]}
do
    cp CMSSW_DYNANO.tar.gz WR_ANALYZE/$PROCESS/
done
rm CMSSW_DYNANO.tar.gz


# Create JDL files and job directories
cd CMSSW_10_6_18/src/PhysicsTools/NanoAODTools/WR
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
