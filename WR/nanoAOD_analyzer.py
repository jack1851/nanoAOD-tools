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

	self.file_DYReshape = ROOT.TFile("WR/hists/DYReshapeJetPt_2018.root","READ")
        self.hist_DYReshape_Resolved_ratio_AllCh = self.file_DYReshape.Get("Resolved_ratio_AllCh")

	self.file_Zcorr = ROOT.TFile("WR/hists/Zpt_weights_2018.root", "READ")
	self.m_Zweights = self.file_Zcorr.Get("zptmass_weights")

#        self.file_event_weights = ROOT.TFile("WR/reweighting_variables/ptjjovermjj/ptjjovermjjweights.root", "READ")
#        self.hist_reweights = self.file_event_weights.Get("hnew_ratio")

    def beginJob(self, histFile=None, histDirName=None):
	prevdir = ROOT.gDirectory

#********************************************************************
# Make the mass and flavor directories                              *
#********************************************************************
        histFile.cd()

	self.CR_Directory = histFile.mkdir("60mll150")

	self.CR_Directory.cd()
        self.CR_unweighted_Directory =  self.CR_Directory.mkdir("60mll150_unweighted")
        self.CR_unweighted_Directory.cd()
        self.CR_unweighted_ll_Dir = self.CR_unweighted_Directory.mkdir("l_l")
        self.CR_unweighted_ee_Dir = self.CR_unweighted_Directory.mkdir("e_e")
        self.CR_unweighted_mumu_Dir = self.CR_unweighted_Directory.mkdir("mu_mu")
        
        self.CR_Directory.cd()
        self.CR_data_Directory =  self.CR_Directory.mkdir("60mll150_pseudodata")
        self.CR_data_Directory.cd()
        self.CR_data_ll_Dir = self.CR_data_Directory.mkdir("l_l")
        self.CR_data_ee_Dir = self.CR_data_Directory.mkdir("e_e")
        self.CR_data_mumu_Dir = self.CR_data_Directory.mkdir("mu_mu")

        self.CR_Directory.cd()
        self.CR_reweighted_Directory =  self.CR_Directory.mkdir("60mll150_reweighted")
        self.CR_reweighted_Directory.cd()
        self.CR_reweighted_ll_Dir = self.CR_reweighted_Directory.mkdir("l_l")
        self.CR_reweighted_ee_Dir = self.CR_reweighted_Directory.mkdir("e_e")
        self.CR_reweighted_mumu_Dir = self.CR_reweighted_Directory.mkdir("mu_mu")

	prevdir.cd()
        histFile.cd()

	self.SR_Directory = histFile.mkdir("400mll")

        self.SR_Directory.cd()
        self.SR_unweighted_Directory =  self.SR_Directory.mkdir("400mll_unweighted")
        self.SR_unweighted_Directory.cd()
	self.SR_unweighted_ll_Dir = self.SR_unweighted_Directory.mkdir("l_l")
        self.SR_unweighted_ee_Dir = self.SR_unweighted_Directory.mkdir("e_e")
        self.SR_unweighted_mumu_Dir = self.SR_unweighted_Directory.mkdir("mu_mu")

        self.SR_Directory.cd()
        self.SR_data_Directory =  self.SR_Directory.mkdir("400mll_pseudodata")
        self.SR_data_Directory.cd()
        self.SR_data_ll_Dir = self.SR_data_Directory.mkdir("l_l")
        self.SR_data_ee_Dir = self.SR_data_Directory.mkdir("e_e")
        self.SR_data_mumu_Dir = self.SR_data_Directory.mkdir("mu_mu")

        self.SR_Directory.cd()
        self.SR_reweighted_Directory =  self.SR_Directory.mkdir("400mll_reweighted")
        self.SR_reweighted_Directory.cd()
        self.SR_reweighted_ll_Dir = self.SR_reweighted_Directory.mkdir("l_l")
        self.SR_reweighted_ee_Dir = self.SR_reweighted_Directory.mkdir("e_e")
        self.SR_reweighted_mumu_Dir = self.SR_reweighted_Directory.mkdir("mu_mu")


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

        self.CR_unweighted_ll = eventHistos("60mll150_ll_")
        self.CR_unweighted_ee = eventHistos("60mll150_ee_")
        self.CR_unweighted_mumu = eventHistos("60mll150_mumu_")

        self.CR_data_ll = eventHistos("60mll150_ll_")
        self.CR_data_ee = eventHistos("60mll150_ee_")
        self.CR_data_mumu = eventHistos("60mll150_mumu_")

        self.CR_reweighted_ll = eventHistos("60mll150_ll_")
        self.CR_reweighted_ee = eventHistos("60mll150_ee_")
        self.CR_reweighted_mumu = eventHistos("60mll150_mumu_")

        self.SR_unweighted_ll = eventHistos("400mll_ll_")
        self.SR_unweighted_ee = eventHistos("400mll_ee_")
        self.SR_unweighted_mumu = eventHistos("400mll_mumu_")
 
        self.SR_data_ll = eventHistos("400mll_ll_")
        self.SR_data_ee = eventHistos("400mll_ee_")
        self.SR_data_mumu = eventHistos("400mll_mumu_")

        self.SR_reweighted_ll = eventHistos("400mll_ll_")
        self.SR_reweighted_ee = eventHistos("400mll_ee_")
        self.SR_reweighted_mumu = eventHistos("400mll_mumu_")

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
#        print "TEST: %r" % self.file_DYReshape
#        print self.hist_DYReshape_Resolved_ratio_AllCh
 	self.CR_unweighted_ll.eventweights(event)
        self.CR_unweighted_ee.eventweights(event)
        self.CR_unweighted_mumu.eventweights(event)

        self.CR_data_ll.eventweights(event)
        self.CR_data_ee.eventweights(event)
        self.CR_data_mumu.eventweights(event)

        self.CR_reweighted_ll.eventweights(event)
        self.CR_reweighted_ee.eventweights(event)
        self.CR_reweighted_mumu.eventweights(event)

        self.SR_unweighted_ll.eventweights(event)
        self.SR_unweighted_ee.eventweights(event)
        self.SR_unweighted_mumu.eventweights(event)
	
        self.SR_data_ll.eventweights(event)
        self.SR_data_ee.eventweights(event)
        self.SR_data_mumu.eventweights(event)

        self.SR_reweighted_ll.eventweights(event)
        self.SR_reweighted_ee.eventweights(event)
        self.SR_reweighted_mumu.eventweights(event)

        self.IR_ll.eventweights(event)
        self.IR_ee.eventweights(event)
        self.IR_mumu.eventweights(event)
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
	    if abs(ele.eta) > 2.4 or ele.pt < 53:
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

	if abs(leadLep.pdgId) != abs(subleadLep.pdgId):
	    return False

	if self.DeltaR(leadLep,subleadLep) < 0.4:
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

        if (leadJet.p4() + subleadJet.p4() + leadLep.p4() + subleadLep.p4()).M() < 2000:
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
	event.qhad = math.sqrt(event.q2in - event.q2Z)	
        event.diLepPt = (leadLep.p4() + subleadLep.p4()).Pt()
        event.Zreweights = self.getZweight(event.diLepMass, event.diLepPt)[0] 

        event.PtllOverMll = event.diLepPt/event.diLepMass
        event.PtjjOverMjj = event.diJetPt/event.diJetMass
        event.leadLepEta = leadLep.eta
        event.subleadLepEta = subleadLep.eta
        event.leadLepPhi = leadLep.phi
        event.subleadLepPhi = subleadLep.phi
#***********************************************************************************************************
 # FILLING UNWEIGHTED HISTOGRAMS                                                                           *
#***********************************************************************************************************
        print "BEGIN EVENT"
#        print "REWEIGHTING FILE: \n\t%r" % self.file_event_weights
        if 60 < event.diLepMass < 150:
            self.CR_unweighted_ll.FillHists(event)
	    if abs(leadLep.pdgId) == 11: 
	        self.CR_unweighted_ee.FillHists(event)
	    elif abs(leadLep.pdgId) == 13:
		self.CR_unweighted_mumu.FillHists(event)
	elif 150 < event.diLepMass < 250:
            self.IR_ll.FillHists(event)
            if abs(leadLep.pdgId) == 11:
                self.IR_ee.FillHists(event)
            elif abs(leadLep.pdgId) == 13:
                self.IR_mumu.FillHists(event)
	elif event.diLepMass > 250:
 	    self.SR_unweighted_ll.FillHists(event)
	    if abs(leadLep.pdgId) == 11:
                self.SR_unweighted_ee.FillHists(event)
            elif abs(leadLep.pdgId) == 13:
                self.SR_unweighted_mumu.FillHists(event)
	print "EVENT WEIGHTS:"
        print "\tUnweighted event weight: %r" % event.eventWeight
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
	print("CHECKING VARIABLES:")

        print("\tFour Object Invariant Mass: %r GeV") % (event.fourObjectInvariantMass)

	print("LEADING LEPTON KINEMATICS")
        print("\tLeading Lepton 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % (leadLep.p4().E(),leadLep.p4().Px(), leadLep.p4().Py(), leadLep.p4().Pz())
	print("\tLead Lepton Energy: %r GeV") % (leadLep.p4().E())
	print("\tLead Lepton pT: %r GeV") % (event.leadLepPt)
        print("\tLead Lepton Eta: %r") % (event.leadLepEta)
        print("\tLead Lepton Phi: %r") % (event.leadLepPhi)

        print("SUBLEADING LEPTON KINEMATICS")
        print("\tSubleading Lepton 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % (subleadLep.p4().E(), subleadLep.p4().Px(), subleadLep.p4().Py(), subleadLep.p4().Pz())
        print("\tSubleading Lepton Energy: %r GeV") % (subleadLep.p4().E())
        print("\tSublead Lepton pT: %r GeV") % (event.subleadLepPt)
 	print("\tSublead Lepton Eta: %r") % (event.subleadLepEta)
        print("\tSublead Lepton Phi: %r") % (event.subleadLepPhi)

	print("DILEPTON KINEMATICS")
	print("\tZ Boson 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % ((leadLep.p4()+subleadLep.p4()).E(), (leadLep.p4()+subleadLep.p4()).Px(), (leadLep.p4()+subleadLep.p4()).Py(), (leadLep.p4()+subleadLep.p4()).Pz())
	print("\tZ Boson Energy: E_Z = %r") % (leadLep.p4()+subleadLep.p4()).E()
        print("\tDilepton pT: p^T_{ll} = %r GeV") % (event.diLepPt)
        print("\tDilepton Mass: m_{ll} = %r GeV") % (event.diLepMass)
        print("\tp^T_{ll}/m_{ll} = %r") % (event.PtllOverMll)

        print("LEADING JET KINEMATICS")
        print("\tLeading Jet 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % (leadJet.p4().E(),leadJet.p4().Px(), leadJet.p4().Py(), leadJet.p4().Pz())
        print("\tLead Jet Energy: %r GeV") % (leadJet.p4().E())
        print("\tLead Jet pT: %r GeV") % (event.leadJetPt)
        print("\tLead Jet Eta: %r") % (event.leadJetEta)
        print("\tLead Jet Phi: %r") % (event.leadJetPhi)

        print("SUBLEADING JET KINEMATICS")
        print("\tSubleading Jet 4-vector (E, px, py, pz): (%r GeV, %r GeV, %r GeV, %r GeV)") % (subleadJet.p4().E(), subleadJet.p4().Px(), subleadJet.p4().Py(), subleadJet.p4().Pz())
        print("\tSublead Jet Energy: %r GeV") % (subleadJet.p4().E())
        print("\tSublead Jet pT: %r GeV") % (event.subleadJetPt)
        print("\tSublead Jet Eta: %r") % (event.subleadJetEta)
        print("\tSublead Jet Phi: %r") % (event.subleadJetPhi)

        print("DIJET KINEMATICS")
        print("\tDijet pT: %r GeV") % (event.diJetPt)
        print("\tDijet Mass: %r GeV") % (event.diJetMass)
        print("\tp^T_{jj}/m_{jj} = %r") % (event.PtjjOverMjj)

        print("OTHER KINEMATICS")
        print("\tLead Jet + Z Mass: %r GeV") % (event.leadJetZMass)
        print("\tSublead Jet + Z Mass: %r GeV") % (event.subleadJetZMass)

        print("Q SQUARED STATS")
        print("\tInitial q^{2}: %r GeV^{2}") % (event.q2in)
        print("\tInitial q: %r GeV") % (math.sqrt(event.q2in))
        print("\tq^{2} of the Z: %r GeV^{2}") % (event.q2Z)
        print("\tq of the Z: %r GeV") % (math.sqrt(event.q2Z))
        print("\tq_{had} = \sqrt{q^{2}_{in} - q^{2}_{Z}}: %r GeV") % (event.qhad)
        print("END EVENT\n")

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
 
#filename = "root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/280000/DF896280-DF2F-D748-ABCB-FC055EE6CC96.root"
p = PostProcessor(".", filename, cut=None, branchsel=None, modules=[
                  ExampleAnalysis()], noOut=True, histFileName="{}.root".format(hist), histDirName="plots")
p.run()
