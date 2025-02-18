#!/bin/bash

# Exit on error
set -e

#echo "### Begin of job"
#echo "Starting job on " `date` #Date/time of start of job
#echo "Running on: `uname -a`" #Condor job is running on this node
#echo "System software: `cat /etc/redhat-release`" #Operating System on that node
ID=$1
#echo "ID:" $ID
PROCESS=$2
#echo "Process:" $PROCESS
FILE=$3
#echo "File:" $FILE
#echo "In the directory with the current contents:"
#echo "pwd: $(pwd)"
#echo "ls: $(ls -lrt)"
#echo "Unzipping tarbell: CMSSW_DYNANO.tar.gz"
tar -xzf CMSSW_DYNANO.tar.gz
#echo "Unzipped."
cd CMSSW_10_6_18
#echo "In the directory with the current contents:"
#echo "pwd: $(pwd)"
#echo "ls: $(ls -lrt)"
#echo "Running environment setup script:"
source /cvmfs/cms.cern.ch/cmsset_default.sh
#echo "Running cmsenv:"
cmsenv
#echo "Scram b Project rename"
scramv1 b ProjectRename
#echo "Running cmsenv again:"
cmsenv
#echo "pwd: $(pwd)"
#echo "Finding python path"
PYTHONPATH=$PWD/python
export PYTHONPATH
#echo $PYTHONPATH
#echo "Changing directory"
cd src/PhysicsTools/NanoAODTools
#echo "pwd: $(pwd)"
#echo "ls: $(ls -lrt)"
#echo "Submitting analyzer"
python WR/nanoAOD_analyzer.py $3 $2_$1
#echo "Now the contents of the directory is:"
#echo "ls: $(ls -lrt)"
#echo "### End of job"
