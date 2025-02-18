#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.histos import eventHistos
from importlib import import_module
import os
import sys
from sys import argv
import ROOT
import math
import uproot
import pandas as pd
import csv
import inspect
ROOT.PyConfig.IgnoreCommandLineOptions = True
#script, filename, hist = argv

class ExampleAnalysis(Module):
    def __init__(self):
        self.writeHistFile = True
        self.file_header_written = False
    def beginJob(self, histFile=None, histDirName=None):
       
        Module.beginJob(self)
        
    def analyze(self, event):
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        elep4 = []
        eleid = []
        mup4 = []
        mutight = []
        muid2 = []
        muid3 = []
        jetp4 = []
        jetid = []
#        print("event:", event)
        print("event type:", type(event))
        print(inspect.getmembers(event)) 
        for ele in electrons:
            elep4.append([ele.p4().E(), ele.p4().Px(), ele.p4().Py(), ele.p4().Pz()])
            eleid.append(ele.cutBased_HEEP)
        for mu in muons:
            mup4.append([mu.p4().E(), mu.p4().Px(), mu.p4().Py(), mu.p4().Pz()])
            mutight.append(mu.tightId)
            muid2.append(mu.highPtId)
            muid3.append(mu.pfRelIso03_all)
        for j in jets:
            jetp4.append([j.p4().E(), j.p4().Px(), j.p4().Py(), j.p4().Pz()])
            jetid.append(j.jetId)

        with open("full_unprocessed_ttbar_data.csv", mode='a') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'electrons(E,px,py,pz)',
                'muons(E,px,py,pz)',
                'jets(E,px,py,pz)',
                'electronId',
                'muonTightId',
                'muonHighpTId',
                'muonRelIso',
                'jetId',
            ])  
            if not self.file_header_written: 
                writer.writeheader()
                self.file_header_written = True
            writer.writerow({
                'electrons(E,px,py,pz)': elep4,
                'muons(E,px,py,pz)': mup4,
                'jets(E,px,py,pz)': jetp4,
                'electronId': eleid,
                'muonTightId': mutight,
                'muonHighpTId': muid2,
                'muonRelIso': muid3,
                'jetId': jetid,
            })          
        return True

preselection = None 
filename = "root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/102X_upgrade2018_realistic_v15-v1/120000/45141C8F-A79E-4A41-A1A8-25C8EE261EDD.root"
p = PostProcessor(".", filename, cut=preselection, branchsel=None, modules=[
                  ExampleAnalysis()], noOut=True, histFileName="{seanHistos}.root", histDirName="plots")
p.run()
