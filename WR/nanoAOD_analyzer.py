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
ROOT.PyConfig.IgnoreCommandLineOptions = True
script, filename, hist = argv

class ExampleAnalysis(Module):
    def __init__(self):
        self.writeHistFile = True


    def beginJob(self, histFile=None, histDirName=None):
	prevdir = ROOT.gDirectory

#********************************************************************
# Make the mass and flavor directories                              *
#********************************************************************
        histFile.cd()

	self.CR_Directory = histFile.mkdir("60mll150")
	self.CR_Directory.cd()
	self.CR_ll_Dir = self.CR_Directory.mkdir("l_l")
	self.CR_ee_Dir = self.CR_Directory.mkdir("e_e")
        self.CR_mumu_Dir = self.CR_Directory.mkdir("mu_mu")

	prevdir.cd()
        histFile.cd()

	self.SR_Directory = histFile.mkdir("400mll")
        self.SR_Directory.cd()
	self.SR_ll_Dir = self.SR_Directory.mkdir("l_l")
        self.SR_ee_Dir = self.SR_Directory.mkdir("e_e")
        self.SR_mumu_Dir = self.SR_Directory.mkdir("mu_mu")

        prevdir.cd()
        histFile.cd()

        self.IR_Directory = histFile.mkdir("150mll400")
        self.IR_Directory.cd()
        self.IR_ll_Dir = self.IR_Directory.mkdir("l_l")
        self.IR_ee_Dir = self.IR_Directory.mkdir("e_e")
        self.IR_mumu_Dir = self.IR_Directory.mkdir("mu_mu")
	
        prevdir.cd()

#******************************************************************
# Make instances of the eventHistos class                         *
#******************************************************************

        self.CR_ll = eventHistos("60mll150_ll_")
        self.CR_ee = eventHistos("60mll150_ee_")
        self.CR_mumu = eventHistos("60mll150_mumu_")


        self.SR_ll = eventHistos("400mll_ll_")
        self.SR_ee = eventHistos("400mll_ee_")
        self.SR_mumu = eventHistos("400mll_mumu_")
 
        self.IR_ll = eventHistos("150mll400_ll_")
        self.IR_ee = eventHistos("150mll400_ee_")
        self.IR_mumu = eventHistos("150mll400_mumu_")
       
        Module.beginJob(self, histFile, histDirName)

    def analyze(self, event):
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        genparticles = Collection(event, "GenPart")

	event.eventWeight = event.genWeight/abs(event.genWeight)

	self.CR_ll.eventweights(event)
        self.CR_ee.eventweights(event)
        self.CR_mumu.eventweights(event)
	self.IR_ll.eventweights(event)
        self.IR_ee.eventweights(event)
        self.IR_mumu.eventweights(event)
        self.SR_ll.eventweights(event)
        self.SR_ee.eventweights(event)
        self.SR_mumu.eventweights(event)	

#************************************************************************************************************       
# Preliminary cuts
#************************************************************************************************************
	if (len(electrons) < 2 and len(muons) < 2) or len(jets) < 2:
	    return False
#**********************************************************************************************************
# Select leptons
#**********************************************************************************************************		
	ele_count = 0
	mu_count = 0

        leadLep = None
        subleadLep = None

        for ele in electrons:
	    if ele.eta > 2.4 or ele.pt < 53:
	        continue
	    elif ele.cutBased_HEEP == False:
	        continue
	    else:
		if ele_count == 0:
		    leadLep = ele 
		else:
		    subleadLep = ele
		    break
                ele_count += 1
	
	for mu in muons:
	    if abs(mu.eta) > 2.4 or mu.pt < 53:
	        continue
            elif mu.highPtId == False:
		continue
	    elif mu.tkRelIso > 0.1:
		continue   
	    else:
                if mu_count == 0:
                    leadLep = mu
                else:
                    subleadLep = mu
                    break
                mu_count += 1
		
        if leadLep is None or subleadLep is None:
            return False
#*******************************************************************************************************	
# Select Jets
#******************************************************************************************************
	jet_count = 0

	leadJet = None
	subleadJet = None

        for j in jets:
	    if j.jetId != 6:
	        continue
	    if j.pt < 40 or abs(j.eta) > 2.4:
		continue
	    else:
	        if self.DeltaR(j,leadLep) < 0.4 or self.DeltaR(j,subleadLep) < 0.4:
                    continue
	        else:
		    if jet_count == 0:
		        leadJet = j
		    else:
                        subleadJet = j
		        break
		    jet_count += 1  
	
	if leadJet == None or subleadJet == None:
	    return False 	
#*************************************************************************************************************  
 # Declare kinematic variables                                                                               *
#*************************************************************************************************************            
        event.fourObjectInvariantMass = (leadJet.p4() + subleadJet.p4() + leadLep.p4() + subleadLep.p4()).M()
	event.fourObjectInvariantPt = (leadJet.p4() + subleadJet.p4() + leadLep.p4() + subleadLep.p4()).Pt()
        event.leadJetZMass = (leadJet.p4() + leadLep.p4() + subleadLep.p4()).M()
        event.subleadJetZMass = (subleadJet.p4() + leadLep.p4() + subleadLep.p4()).M()
        event.leadJetPt = leadJet.pt
        event.subleadJetPt = subleadJet.pt
        event.diJetMass = (leadJet.p4() + subleadJet.p4()).M()
        event.diJetPt = (leadJet.p4() + subleadJet.p4()).Pt()
        event.leadJetEta = leadJet.eta
        event.subleadJetEta = subleadJet.eta
        event.leadJetPhi = leadJet.phi
        event.subleadJetPhi = subleadJet.phi
        event.leadLepPt = leadLep.pt
        event.subleadLepPt = subleadLep.pt
        event.diLepMass = (leadLep.p4() + subleadLep.p4()).M()
	event.q2Z = (leadLep.p4() + subleadLep.p4()).M2()
        event.q2in = self.fourMomVec(genparticles).M2()
	event.q2diff = event.q2in - event.q2Z	
        event.diLepPt = (leadLep.p4() + subleadLep.p4()).Pt()
        event.PtllOverMll = (leadLep.p4() + subleadLep.p4()).Pt()/(leadLep.p4() + subleadLep.p4()).M()
        event.PtjjOverMjj = (leadJet.p4() + subleadJet.p4()).Pt()/(leadJet.p4() + subleadJet.p4()).M()
        event.leadLepEta = leadLep.eta
        event.subleadLepEta = subleadLep.eta
        event.leadLepPhi = leadLep.phi
        event.subleadLepPhi = subleadLep.phi
#***********************************************************************************************************
 # FILLING HISTOGRAMS                                                                                      *
#***********************************************************************************************************
        if 50 < event.diLepMass < 150:
            self.CR_ll.FillHists(event)
	    if abs(leadLep.pdgId) == 11: 
	        self.CR_ee.FillHists(event)
	    elif abs(leadLep.pdgId) == 13:
		self.CR_mumu.FillHists(event)
	elif 150 < event.diLepMass < 400:
            self.IR_ll.FillHists(event)
            if abs(leadLep.pdgId) == 11:
                self.IR_ee.FillHists(event)
            elif abs(leadLep.pdgId) == 13:
                self.IR_mumu.FillHists(event)
	elif event.diLepMass > 400:
	    self.SR_ll.FillHists(event)
	    if abs(leadLep.pdgId) == 11:
                self.SR_ee.FillHists(event)
            elif abs(leadLep.pdgId) == 13:
                self.SR_mumu.FillHists(event)
#*********************************************************************************************************
# CHECKING FINAL VARIABLES                                                                               *
#*********************************************************************************************************
#       print("BEGIN EVENT")
#	print("\nCHECKING VARIABLES:")
#	print("LEADING LEPTON KINEMATICS")
#        print("Leading Lepton 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % (leadLep.p4().E(),leadLep.p4().Px(), leadLep.p4().Py(), leadLep.p4().Pz())
#	print("Lead Lepton Energy: %r GeV") % (leadLep.p4().E())
#	print("Lead Lepton pT: %r GeV") % (leadLepPt)
#        print("Lead Lepton Eta: %r") % (leadLepEta)
#        print("Lead Lepton Phi: %r") % (leadLepPhi)

#        print("SUBLEADING LEPTON KINEMATICS")
#        print("Subleading Lepton 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % (subleadLep.p4().E(), subleadLep.p4().Px(), subleadLep.p4().Py(), subleadLep.p4().Pz())
#        print("Subleading Lepton Energy: %r GeV") % (subleadLep.p4().E())
#        print("Sublead Lepton pT: %r GeV") % (subleadLepPt)
# 	print("Sublead Lepton Eta: %r") % (subleadLepEta)
#        print("Sublead Lepton Phi: %r") % (subleadLepPhi)

#	print("\nZ KINEMATICS")
#	print("Z Boson 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % ((leadLep.p4()+subleadLep.p4()).E(), (leadLep.p4()+subleadLep.p4()).Px(), (leadLep.p4()+subleadLep.p4()).Py(), (leadLep.p4()+subleadLep.p4()).Pz())
#	print("Z Boson Energy: E_Z = %r") % (leadLep.p4()+subleadLep.p4()).E()
#        print("Dilepton pT: p^T_{ll} = %r GeV") % (diLepPt)
#        print("Dilepton Mass: m_{ll} = %r GeV") % (diLepMass)
#        print("p^T_{ll}/m_{ll} = %r") % (PtllOverMll)
#	print("Lead Jet + Z Mass: %r GeV") % (leadJetZMass)
#        print("Sublead Jet + Z Mass: %r GeV") % (subleadJetZMass)
#        print("Four Object Invariant Mass: %r GeV") % (fourObjectInvariantMass)
#
#        print("\nLEADING JET KINEMATICS")
#        print("Leading Jet 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % (leadJet.p4().E(),leadJet.p4().Px(), leadJet.p4().Py(), leadJet.p4().Pz())
#        print("Lead Jet Energy: %r GeV") % (leadJet.p4().E())
#        print("Lead Jet pT: %r GeV") % (leadJetPt)
#        print("Lead Jet Eta: %r") % (leadJetEta)
#        print("Lead Jet Phi: %r") % (leadJetPhi)

 #       print("\nSUBLEADING JET KINEMATICS")
 #       print("Subleading Jet 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % (subleadJet.p4().E(), subleadJet.p4().Px(), subleadJet.p4().Py(), subleadJet.p4().Pz())
#        print("Sublead Jet Energy: %r GeV") % (subleadJet.p4().E())
#        print("Sublead Jet pT: %r GeV") % (subleadJetPt)
#        print("Sublead Jet Eta: %r") % (subleadJetEta)
#        print("Sublead Jet Phi: %r") % (subleadJetPhi)

#        print("\nDIJET KINEMATICS")
#        print("Dijet pT: %r GeV") % (diJetPt)
#        print("Dijet Mass: %r GeV") % (diJetMass)
#        print("END EVENT\n")

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

    def fourMomVec(self, gen):
	pX = 0
        pY = 0
        pZ = 0
        ene = 0
        for i in gen:
#           print("%r, ID: %r, Mother Index: %r, Mother Id: %r, px: %r, py: %r, pz: %r, e: %r") % (i, i.pdgId, i.genPartIdxMother, self.getMotherId(genparticles, i.genPartIdxMother), round(i.p4().Px(),2), round(i.p4().Py(),2), round(i.p4().Pz(),2), round(i.p4().E(),2))
            if i.genPartIdxMother == 0:
                pX += i.p4().Px()
                pY += i.p4().Py()
                pZ += i.p4().Pz()
                ene += i.p4().E()
        qin = ROOT.TLorentzVector(pX, pY, pZ, ene)
	return qin


#filename = "root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/280000/DF896280-DF2F-D748-ABCB-FC055EE6CC96.root"
p = PostProcessor(".", filename, cut=None, branchsel=None, modules=[
                  ExampleAnalysis()], noOut=True, histFileName="{}.root".format(hist), histDirName="plots")
p.run()
