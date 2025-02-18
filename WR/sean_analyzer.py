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
ROOT.PyConfig.IgnoreCommandLineOptions = True
#script, filename, hist = argv

class ExampleAnalysis(Module):
    def __init__(self):
        self.writeHistFile = True
        self.df = pd.DataFrame()

    def beginJob(self, histFile=None, histDirName=None):
       
        Module.beginJob(self)
        
    def analyze(self, event):
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")

        elept = []
        eleeta = []
        elephi = []
        elep4 = []
      
        mupt = []
        mueta = []
        muphi = []
        mup4 = []

        jetpt = []
        jeteta = []
        jetphi = []
        jetp4 = []

	if (len(electrons) < 2 and len(muons) < 2) or len(jets) < 2:
	    return False

        for ele in electrons:
            if abs(ele.eta) > 2.4 or ele.pt < 50:
                continue
            elept.append(ele.pt)
            eleeta.append(ele.eta)
            elephi.append(ele.phi)
            elep4.append([ele.p4().E(), ele.p4().Px(), ele.p4().Py(), ele.p4().Pz()])
       
        for mu in muons:
            if abs(mu.eta) > 2.4 or mu.pt < 50:
                continue
            mupt.append(mu.pt)
            mueta.append(mu.eta)
            muphi.append(mu.phi)
            mup4.append([mu.p4().E(), mu.p4().Px(), mu.p4().Py(), mu.p4().Pz()])

        for j in jets:
            if j.pt < 40 or abs(j.eta) > 2.4:
                continue
            jetpt.append(j.pt)
            jeteta.append(j.eta)
            jetphi.append(j.phi)
            jetp4.append([j.p4().E(), j.p4().Px(), j.p4().Py(), j.p4().Pz()])

        if (len(elept) + len(mupt)) < 2:
            return False

        print('ELECTRON EVENT DATA:', elept, eleeta, elephi, elep4)
        self.df = self.df.append({'Electron pT': elept, 'Electron Phi': elephi, 'Electron Eta': eleeta, 'Electron 4-vec(E, px, py, pz)': elep4, 
                                  'Muon pT': mupt, 'Muon Phi': muphi, 'Muon Eta': mueta, 'Muon 4-vec(E, px, py, pz)': mup4,
                                  'Jet pT': jetpt, 'Jet Phi': jetphi, 'Jet Eta': jeteta, 'Jet 4-vec(E, px, py, pz)': jetp4,                                                                                                                                                           }, ignore_index=True)
        print(self.df)
        self.df.to_csv("data.csv", index=False)
            
#        print(self.df)
#	
#        if leadLep is None or subleadLep is None:
#            return False
#
#	if abs(leadLep.pdgId) != abs(subleadLep.pdgId):
#	    return False

#	if self.DeltaR(leadLep,subleadLep) < 0.4:
#	    return False
#*******************************************************************************************************	
# Select Jets
#******************************************************************************************************
#	jet_count = 0

#	leadJet = None
#	subleadJet = None

#        for j in jets:
#	    if j.jetId != 6:
#	        continue
#	    if j.pt < 40 or abs(j.eta) > 2.4:
#		continue
#	    else:
#	        if self.DeltaR(j,leadLep) < 0.4 or self.DeltaR(j,subleadLep) < 0.4:
#                    continue
#	        else:
#		    if jet_count == 0:
#		        leadJet = j
#		    else:
#                        subleadJet = j
#		        break
#		    jet_count += 1  
	
#	if leadJet == None or subleadJet == None:
#	    return False 

#        if (leadJet.p4() + subleadJet.p4() + leadLep.p4() + subleadLep.p4()).M() < 2000:
#            return False	
#*************************************************************************************************************  
 # Declare kinematic variables                                                                               *
#*************************************************************************************************************            
#        event.fourObjectInvariantMass = (leadJet.p4() + subleadJet.p4() + leadLep.p4() + subleadLep.p4()).M()
#	event.fourObjectInvariantPt = (leadJet.p4() + subleadJet.p4() + leadLep.p4() + subleadLep.p4()).Pt()
#        event.leadJetZMass = (leadJet.p4() + leadLep.p4() + subleadLep.p4()).M()
#        event.subleadJetZMass = (subleadJet.p4() + leadLep.p4() + subleadLep.p4()).M()
#        event.leadJetPt = leadJet.pt
#        event.subleadJetPt = subleadJet.pt
#        event.diJetMass = (leadJet.p4() + subleadJet.p4()).M()
#        event.diJetPt = (leadJet.p4() + subleadJet.p4()).Pt()
#        event.leadJetEta = leadJet.eta
#        event.subleadJetEta = subleadJet.eta
#        event.leadJetPhi = leadJet.phi
#        event.subleadJetPhi = subleadJet.phi
#        event.leadLepPt = leadLep.pt
#        event.subleadLepPt = subleadLep.pt
#        event.diLepMass = (leadLep.p4() + subleadLep.p4()).M()
#	event.q2Z = (leadLep.p4() + subleadLep.p4()).M2()
#        event.q2in = self.fourMomVec(genparticles).M2()
#	event.qhad = math.sqrt(event.q2in - event.q2Z)	
#        event.diLepPt = (leadLep.p4() + subleadLep.p4()).Pt()
#        event.Zreweights = self.getZweight(event.diLepMass, event.diLepPt)[0] 

#        event.PtllOverMll = event.diLepPt/event.diLepMass
#        event.PtjjOverMjj = event.diJetPt/event.diJetMass
#        event.leadLepEta = leadLep.eta
#        event.subleadLepEta = subleadLep.eta
#        event.leadLepPhi = leadLep.phi
#        event.subleadLepPhi = subleadLep.phi
##***********************************************************************************************************
 # FILLING UNWEIGHTED HISTOGRAMS                                                                           *
#***********************************************************************************************************
#        print "BEGIN EVENT"
#        print "REWEIGHTING FILE: \n\t%r" % self.file_event_weights
#        if 60 < event.diLepMass < 150:
#            self.CR_unweighted_ll.FillHists(event)
#	    if abs(leadLep.pdgId) == 11: 
#	        self.CR_unweighted_ee.FillHists(event)
#	    elif abs(leadLep.pdgId) == 13:
#		self.CR_unweighted_mumu.FillHists(event)
#	elif 150 < event.diLepMass < 250:
#            self.IR_ll.FillHists(event)
#            if abs(leadLep.pdgId) == 11:
#                self.IR_ee.FillHists(event)
#            elif abs(leadLep.pdgId) == 13:
#                self.IR_mumu.FillHists(event)
#	elif event.diLepMass > 250:
# 	    self.SR_unweighted_ll.FillHists(event)
#	    if abs(leadLep.pdgId) == 11:
#                self.SR_unweighted_ee.FillHists(event)
#            elif abs(leadLep.pdgId) == 13:
#                self.SR_unweighted_mumu.FillHists(event)
#	print "EVENT WEIGHTS:"
#        print "\tUnweighted event weight: %r" % event.eventWeight
#***********************************************************************************************************
 # Create control region reweighted DY and fill histograms                                                 *
#***********************************************************************************************************
#        event.eventWeight = event.eventWeight*self.GetEventReshape(event.PtjjOverMjj)
#        print "\tEvent weight after reweighting by ptjjovermjj: %r" % event.eventWeight
#        if 60 < event.diLepMass < 150:
#            self.CR_reweighted_ll.FillHists(event)
#            if abs(leadLep.pdgId) == 11:
#                self.CR_reweighted_ee.FillHists(event)
#            elif abs(leadLep.pdgId) == 13:
#                self.CR_reweighted_mumu.FillHists(event)
#
#        if event.diLepMass > 400:
#            self.SR_reweighted_ll.FillHists(event)
#            if abs(leadLep.pdgId) == 11:
#                self.SR_reweighted_ee.FillHists(event)
#            elif abs(leadLep.pdgId) == 13:
#                self.SR_reweighted_mumu.FillHists(event)

#***********************************************************************************************************
 # Create control region pseudodata and fill histograms                                                    *
#***********************************************************************************************************
#        event.eventWeight = event.genWeight/abs(event.genWeight)
#        if 1000 < event.fourObjectInvariantMass < 1200:
#            event.eventWeight = event.eventWeight*(1/1.02)
#        elif 1200 < event.fourObjectInvariantMass < 1400:
#            event.eventWeight = event.eventWeight*(1/1.05)
#        elif 1400 < event.fourObjectInvariantMass < 1600:
#            event.eventWeight = event.eventWeight*(1/1.06)
#        elif 1600 < event.fourObjectInvariantMass < 2000:
#            event.eventWeight = event.eventWeight*(1/1.08)
#        elif 2000 < event.fourObjectInvariantMass < 2400:
#            event.eventWeight = event.eventWeight*(1/1.15)
#        elif 2400 < event.fourObjectInvariantMass < 2800:
#            event.eventWeight = event.eventWeight*(1/1.20)
#        elif 2800 < event.fourObjectInvariantMass < 3200:
#            event.eventWeight = event.eventWeight*(1/1.35)
#        elif 3200 < event.fourObjectInvariantMass:
#            event.eventWeight = event.eventWeight*(1/1.38)

#        if 60 < event.diLepMass < 150:
#            self.CR_data_ll.FillHists(event)
#            if abs(leadLep.pdgId) == 11:
#                self.CR_data_ee.FillHists(event)
#            elif abs(leadLep.pdgId) == 13:
#                self.CR_data_mumu.FillHists(event)

#        print "\tEvent weight for CR pseudodata: %r" % event.eventWeight
#***********************************************************************************************************
 # Create signal region pseudodata and fill histograms                                                     *
#***********************************************************************************************************

#        event.eventWeight = event.genWeight/abs(event.genWeight)
#        if 1000 < event.fourObjectInvariantMass < 1200:
#            event.eventWeight = event.eventWeight*(1/0.96)
#        elif 1200 < event.fourObjectInvariantMass < 1400:
#            event.eventWeight = event.eventWeight*(1/0.98)
#        elif 1400 < event.fourObjectInvariantMass < 1600:
#            event.eventWeight = event.eventWeight*(1/1.04)
#        elif 1600 < event.fourObjectInvariantMass < 2000:
#            event.eventWeight = event.eventWeight*(1/1.1)
#        elif 2000 < event.fourObjectInvariantMass < 2400:
#            event.eventWeight = event.eventWeight*(1/1.07)
#        elif 2400 < event.fourObjectInvariantMass < 2800:
#            event.eventWeight = event.eventWeight*(1/1.05)
#        elif 2800 < event.fourObjectInvariantMass < 3200:
#            event.eventWeight = event.eventWeight*(1/0.99)
#        elif 3200 < event.fourObjectInvariantMass:
#            event.eventWeight = event.eventWeight*(1/0.96)

#        if event.diLepMass > 400:
#            self.SR_data_ll.FillHists(event)
#            if abs(leadLep.pdgId) == 11:
#                self.SR_data_ee.FillHists(event)
#            elif abs(leadLep.pdgId) == 13:
#                self.SR_data_mumu.FillHists(event)

#        print "\tEvent weight for SR pseudodata: %r" % event.eventWeight
#*********************************************************************************************************
# CHECKING FINAL VARIABLES                                                                               *
#*********************************************************************************************************
#       print("BEGIN EVENT")
#	print event.q2Z
#	print("CHECKING VARIABLES:")

#        print("\tFour Object Invariant Mass: %r GeV") % (event.fourObjectInvariantMass)

#	print("LEADING LEPTON KINEMATICS")
#        print("\tLeading Lepton 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % (leadLep.p4().E(),leadLep.p4().Px(), leadLep.p4().Py(), leadLep.p4().Pz())
#	print("\tLead Lepton Energy: %r GeV") % (leadLep.p4().E())
#	print("\tLead Lepton pT: %r GeV") % (event.leadLepPt)
#        print("\tLead Lepton Eta: %r") % (event.leadLepEta)
#        print("\tLead Lepton Phi: %r") % (event.leadLepPhi)

#        print("SUBLEADING LEPTON KINEMATICS")
#        print("\tSubleading Lepton 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % (subleadLep.p4().E(), subleadLep.p4().Px(), subleadLep.p4().Py(), subleadLep.p4().Pz())
#        print("\tSubleading Lepton Energy: %r GeV") % (subleadLep.p4().E())
#        print("\tSublead Lepton pT: %r GeV") % (event.subleadLepPt)
# 	print("\tSublead Lepton Eta: %r") % (event.subleadLepEta)
#        print("\tSublead Lepton Phi: %r") % (event.subleadLepPhi)

#	print("DILEPTON KINEMATICS")
#	print("\tZ Boson 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % ((leadLep.p4()+subleadLep.p4()).E(), (leadLep.p4()+subleadLep.p4()).Px(), (leadLep.p4()+subleadLep.p4()).Py(), (leadLep.p4()+subleadLep.p4()).Pz())
#	print("\tZ Boson Energy: E_Z = %r") % (leadLep.p4()+subleadLep.p4()).E()
#        print("\tDilepton pT: p^T_{ll} = %r GeV") % (event.diLepPt)
#        print("\tDilepton Mass: m_{ll} = %r GeV") % (event.diLepMass)
#        print("\tp^T_{ll}/m_{ll} = %r") % (event.PtllOverMll)

#        print("LEADING JET KINEMATICS")
#        print("\tLeading Jet 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % (leadJet.p4().E(),leadJet.p4().Px(), leadJet.p4().Py(), leadJet.p4().Pz())
#        print("\tLead Jet Energy: %r GeV") % (leadJet.p4().E())
#        print("\tLead Jet pT: %r GeV") % (event.leadJetPt)
#        print("\tLead Jet Eta: %r") % (event.leadJetEta)
#        print("\tLead Jet Phi: %r") % (event.leadJetPhi)

#        print("SUBLEADING JET KINEMATICS")
#        print("\tSubleading Jet 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % (subleadJet.p4().E(), subleadJet.p4().Px(), subleadJet.p4().Py(), subleadJet.p4().Pz())
#        print("\tSublead Jet Energy: %r GeV") % (subleadJet.p4().E())
#        print("\tSublead Jet pT: %r GeV") % (event.subleadJetPt)
#        print("\tSublead Jet Eta: %r") % (event.subleadJetEta)
#        print("\tSublead Jet Phi: %r") % (event.subleadJetPhi)

#        print("DIJET KINEMATICS")
#        print("\tDijet pT: %r GeV") % (event.diJetPt)
#        print("\tDijet Mass: %r GeV") % (event.diJetMass)
#        print("\tp^T_{jj}/m_{jj} = %r") % (event.PtjjOverMjj)

#        print("OTHER KINEMATICS")
#        print("\tLead Jet + Z Mass: %r GeV") % (event.leadJetZMass)
#        print("\tSublead Jet + Z Mass: %r GeV") % (event.subleadJetZMass)

#        print("Q SQUARED STATS")
#        print("\tInitial q^{2}: %r GeV^{2}") % (event.q2in)
#        print("\tInitial q: %r GeV") % (math.sqrt(event.q2in))
#        print("\tq^{2} of the Z: %r GeV^{2}") % (event.q2Z)
#        print("\tq of the Z: %r GeV") % (math.sqrt(event.q2Z))
#        print("\tq_{had} = \sqrt{q^{2}_{in} - q^{2}_{Z}}: %r GeV") % (event.qhad)
#        print("END EVENT\n")

        return True

    def DeltaR(self, lepton1, lepton2):
        deta = abs(lepton1.eta - lepton2.eta)
        dphi = abs(lepton1.phi - lepton2.phi)
        while dphi > math.pi:
            dphi = abs(dphi - 2 * math.pi)
        return math.sqrt(dphi**2 + deta**2)
	
    def fourMomVec(self, gen):
        qin = ROOT.TLorentzVector()
        for i in gen:
            if i.genPartIdxMother == 0 or i.genPartIdxMother == 1:
                qin += i.p4()
        return qin
    
    def GetDYReshape(self, jetpt):
        if jetpt >= 2000:
            jetpt = 2000
        
        this_bin = -1
        this_bin = self.hist_DYReshape_Resolved_ratio_AllCh.FindBin(jetpt)
	return self.hist_DYReshape_Resolved_ratio_AllCh.GetBinContent(this_bin)

    def GetEventReshape(self, variable):
        if variable >= 1400:
            variable = 1399

        this_bin = -1
        this_bin = self.hist_reweights.FindBin(variable)
        print "\tTHIS BIN: %r " % (self.hist_reweights.GetBinContent(this_bin))
        return self.hist_reweights.GetBinContent(this_bin)


    def getZweight(self, zm, zpt):
	xbin = self.m_Zweights.GetXaxis().FindBin(zm)
        ybin = self.m_Zweights.GetXaxis().FindBin(zpt)
        if xbin == 0:
            xbin = -1
        elif xbin > self.m_Zweights.GetXaxis().GetNbins():
            xbin -= 1
        elif ybin > self.m_Zweights.GetYaxis().GetNbins():
            ybin = -1

        weight = self.m_Zweights.GetBinContent(xbin, ybin)
        error = self.m_Zweights.GetBinError(xbin, ybin)
        Zweights = []
        Zweights.append(weight)
        Zweights.append(weight+error)
        Zweights.append(weight-error)
        return Zweights

preselection = "(nElectron > 1 || nMuon > 1) && nJet > 1 && Jet_pt[0] > 40" 
filename = "root://cms-xrd-global.cern.ch//store/mc/Run3Winter22NanoAOD/TTTo2L2Nu_CP5_13p6TeV_powheg-pythia8/NANOAODSIM/122X_mcRun3_2021_realistic_v9-v1/40000/b228f31a-ed9c-45e5-b3ca-00a866435b46.root"
p = PostProcessor(".", filename, cut=preselection, branchsel=None, modules=[
                  ExampleAnalysis()], noOut=True, histFileName="{seanHistos}.root", histDirName="plots")
p.run()
