#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.examples.histos import eventHistos
from importlib import import_module
import os
import sys
import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

class ExampleAnalysis(Module):
    def __init__(self):
        self.writeHistFile = True

#    def beginJob(self, histFile=None, histDirName=None, allRegions=None, controlRegion1=None, controlRegion2=None, signalRegion=None, fourObject1=None):
#        Module.beginJob(self, histFile, histDirName, "50mll", "60mll150", "150mll400", "400mll")
    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)
#        histFile.cd()
#	newdir = histFile.mkdir("60mll150")
	instance = eventHistos()

    def analyze(self, event):
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        genparticles = Collection(event, "GenPart")
	
	event.eventWeight = event.genWeight/abs(event.genWeight)
        instance1 = eventHistos()
	instance2 = eventHistos()
	instance1.eventweights(event)
	#Two ways of accessing variables
	     #print("Lead jet mass 1: ", (jets[0].p4()).M())
	     #print("Lead jet mass 2: ", (jets[0].mass))
	
	print "\nBEGIN EVENT"

####################################################################################
# Stuff
####################################################################################
	
	count = 0
	drvalues0 = []
        drvalues1 = []
        leadLep = None
        subleadLep = None


        for i in genparticles:
	    if abs(i.pdgId) == 11 and (self.getMotherId(genparticles, i.genPartIdxMother) == 22 or self.getMotherId(genparticles, i.genPartIdxMother) == 23): #HERE'S A GEN ELECTRON WITH A Z OR PHOTON MOTHER
		if len(electrons) == 2:
		    leadLep = electrons[0]
		    subleadLep = electrons[1]
		elif len(electrons) < 2:
		    return False
                else:
 		    if count == 0: 
                        leadLep = self.getRecoLeptons(i, electrons, drvalues0)
		        count += 1
		    else:
		        subleadLep = self.getRecoLeptons(i, electrons, drvalues1)
		        count += 1
            elif abs(i.pdgId) == 13 and (self.getMotherId(genparticles, i.genPartIdxMother) == 22 or self.getMotherId(genparticles, i.genPartIdxMother) == 23): #HERE'S A MUON
	        if len(muons) == 2:
                    leadLep = muons[0]
                    subleadLep = muons[1]
		elif len(muons) < 2:
		    return False
                else:
                    if count == 0:
                        leadLep = self.getRecoLeptons(i, muons, drvalues0)
                        count += 1
                    else:
                        subleadLep = self.getRecoLeptons(i, muons, drvalues1)
                        count += 1
     
        if leadLep == None or subleadLep == None:
	    return False
     
        if leadLep == subleadLep:
	   return False

        if leadLep.pt < subleadLep.pt:
	    leadLep, subleadLep = subleadLep, leadLep
 
        if leadLep.pt < 60 or subleadLep.pt < 53 or abs(leadLep.eta) > 2.4 or abs(subleadLep.eta) > 2.4:
	    return False
       
#################################################################################################################################
# CHECKING THAT LEADING/SUBLEADING JETS AND LEADING/SUBLEADING LEPTONS ARE WELL SEPARATED (LEAD AND SUBLEAD JETS DECLARED HERE) #
#################################################################################################################################

	hitelseloop = 0
	subleadJet = None
        for j in jets:
	    if j.pt < 30 or abs(j.eta) > 2.4:
		continue
	    else:
	        if self.DeltaR(j,leadLep) < 0.4 or self.DeltaR(j,subleadLep) < 0.4:
                    continue
	        else:
		    if hitelseloop == 0:
		        leadJet = j
		    else:
                        subleadJet = j
		        break
		    hitelseloop += 1  
	
	if subleadJet is None:
	    return False 	


################################################################################################################################################################################################
        # DECLARING KINEMATIC VARIABLES                                                                                          #
################################################################################################################################################################################################

	#Defining jet variables
        event.leadJetPt = leadJet.pt
        event.subleadJetPt = subleadJet.pt
        event.leadJetEta = leadJet.eta
        event.subleadJetEta = subleadJet.eta
        event.leadJetPhi = leadJet.phi
        event.subleadJetPhi = subleadJet.phi
        event.diJetMass = (leadJet.p4() + subleadJet.p4()).M()
        event.diJetPt = (leadJet.p4() + subleadJet.p4()).Pt()
        event.leadLepPt = leadLep.pt
        event.subleadLepPt = subleadLep.pt
        event.leadLepEta = leadLep.eta
        event.subleadLepEta = subleadLep.eta
        event.leadLepPhi = leadLep.phi
        event.subleadLepPhi = subleadLep.phi
        event.diLepMass = (leadLep.p4() + subleadLep.p4()).M()
        event.diLepPt = (leadLep.p4() + subleadLep.p4()).Pt()
        event.PtllOverMll = (leadLep.p4() + subleadLep.p4()).Pt()/(leadLep.p4() + subleadLep.p4()).M()
        event.fourObjectInvariantMass = (leadJet.p4() + subleadJet.p4() + leadLep.p4() + subleadLep.p4()).M()	 
        event.leadJetZMass = (leadJet.p4() + leadLep.p4() + subleadLep.p4()).M()
        event.subleadJetZMass = (subleadJet.p4() + leadLep.p4() + subleadLep.p4()).M()

#################################################################################################################################################################################################
        #FILLING HISTOGRAMS
##################################################################################################################################################################################################
        instance1.FillHists(event)
         
#################################################################################################################################################################################################
# CHECKING FINAL VARIABLES
#################################################################################################################################################################################################

#	print("\nCHECKING VARIABLES:")
#	print("LEADING LEPTON KINEMATICS")
#       print("Leading Lepton 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % (leadLep.p4().E(),leadLep.p4().Px(), leadLep.p4().Py(), leadLep.p4().Pz())
#	print("Lead Lepton Energy: %r GeV") % (leadLep.p4().E())
#	print("Lead Lepton pT: %r GeV") % (leadLepPt)
#       print("Lead Lepton Eta: %r") % (leadLepEta)
#       print("Lead Lepton Phi: %r") % (leadLepPhi)

#       print("SUBLEADING LEPTON KINEMATICS")
#       print("Subleading Lepton 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % (subleadLep.p4().E(), subleadLep.p4().Px(), subleadLep.p4().Py(), subleadLep.p4().Pz())
#       print("Subleading Lepton Energy: %r GeV") % (subleadLep.p4().E())
#       print("Sublead Lepton pT: %r GeV") % (subleadLepPt)
#	print("Sublead Lepton Eta: %r") % (subleadLepEta)
#       print("Sublead Lepton Phi: %r") % (subleadLepPhi)

#	print("\nZ KINEMATICS")
#	print("Z Boson 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % ((leadLep.p4()+subleadLep.p4()).E(), (leadLep.p4()+subleadLep.p4()).Px(), (leadLep.p4()+subleadLep.p4()).Py(), (leadLep.p4()+subleadLep.p4()).Pz())
#	print("Z Boson Energy: E_Z = %r") % (leadLep.p4()+subleadLep.p4()).E()
#       print("Dilepton pT: p^T_{ll} = %r GeV") % (diLepPt)
#       print("Dilepton Mass: m_{ll} = %r GeV") % (diLepMass)
#       print("p^T_{ll}/m_{ll} = %r") % (PtllOverMll)
#	print("Lead Jet + Z Mass: %r GeV") % (leadJetZMass)
#       print("Sublead Jet + Z Mass: %r GeV") % (subleadJetZMass)
#       print("Four Object Invariant Mass: %r GeV") % (fourObjectInvariantMass)

#       print("\nLEADING JET KINEMATICS")
#       print("Leading Jet 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % (leadJet.p4().E(),leadJet.p4().Px(), leadJet.p4().Py(), leadJet.p4().Pz())
#       print("Lead Jet Energy: %r GeV") % (leadJet.p4().E())
#       print("Lead Jet pT: %r GeV") % (leadJetPt)
#       print("Lead Jet Eta: %r") % (leadJetEta)
#       print("Lead Jet Phi: %r") % (leadJetPhi)

#       print("\nSUBLEADING JET KINEMATICS")
#       print("Subleading Jet 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % (subleadJet.p4().E(), subleadJet.p4().Px(), subleadJet.p4().Py(), subleadJet.p4().Pz())
#       print("Sublead Jet Energy: %r GeV") % (subleadJet.p4().E())
#       print("Sublead Jet pT: %r GeV") % (subleadJetPt)
#       print("Sublead Jet Eta: %r") % (subleadJetEta)
#       print("Sublead Jet Phi: %r") % (subleadJetPhi)

#       print("\nDIJET KINEMATICS")
#       print("Dijet pT: %r GeV") % (diJetPt)
#       print("Dijet Mass: %r GeV") % (diJetMass)


        print("END EVENT\n")

        return True

    def DeltaR(self, lepton1, lepton2):
        deta = abs(lepton1.eta - lepton2.eta)
        dphi = abs(lepton1.phi - lepton2.phi)
        while dphi > math.pi:
            dphi = abs(dphi - 2 * math.pi)
        return math.sqrt(dphi**2 + deta**2)
	
    def getMotherId(self, GenPart, index):
	if index == -1:
	    return
	else:
	    return GenPart[index].pdgId

    def getRecoLeptons(self, genpar, leptons, dRvals):
	leadLepton = None
	subleadLepton = None
        for lep in leptons:
            dRvals.append(self.DeltaR(genpar,lep))
        idx1 = self.getLeptons(dRvals, len(leptons))
        leadLepton = leptons[idx1]
        return leadLepton

    def getLeptons(self, dR_Values, length):
	smallest_value = dR_Values[0]
	index = 0
	index1 = 0
	for value in dR_Values:
	    if value <= smallest_value:
		smallest_value = value
		index1 = index
		if index < length-1:
		    index += 1
		else:
		    index = 0
	    else:
	    	if index < length-1:
                    index += 1
                else:
                    index = 0
        return index1

preselection = "(nElectron.size() >= 2 || nMuon.size() >=2) && (nGenPart >= 2) && (nJet.size() >=2)"

files = [" root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/280000/DF896280-DF2F-D748-ABCB-FC055EE6CC96.root"]
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[
                  ExampleAnalysis()], noOut=True, histFileName="nanoAOD_WED.root", histDirName = "histograms")
p.run()
