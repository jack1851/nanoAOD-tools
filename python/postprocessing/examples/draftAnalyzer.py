#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True


class ExampleAnalysis(Module):
    def __init__(self):
        self.writeHistFile = True

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)
        
        #Defining Histograms
#       self.h_vpt = ROOT.TH1F('sumpt', 'sumpt', 100, 0, 1000)
#       self.addObject(self.h_vpt)

	#Event Weight Histogram
	self.h_eventweight = ROOT.TH1F('EventWeight', 'Event Weight', 200, -100, 100)
        self.addObject(self.h_eventweight)

        #Four Object Mass Histograms
	self.h_fourobjectmass = ROOT.TH1F('FourObjectInvariantMass', 'Four Object Invariant Mass m_{lljj}', 1600, 0, 8000)
        self.addObject(self.h_fourobjectmass)

        #Potential Reweighting Variables
	self.h_leadjetpt = ROOT.TH1F('LeadJetpT', 'Lead jet p_{T}', 200, 0, 1000)
	self.addObject(self.h_leadjetpt)

	self.h_subleadjetpt = ROOT.TH1F('SubleadJetpT', 'Sublead jet p_{T}', 200, 0, 1000)
        self.addObject(self.h_subleadjetpt)

        self.h_dileppt = ROOT.TH1F('DileptonpT', 'Dilepton p_{T}(ll)', 200, 0, 1000)
        self.addObject(self.h_dileppt)

        self.h_ptllOvermll = ROOT.TH1F('PtllOverMll', 'p_{T}^{ll}/m_{ll}', 200, 0, 10)
        self.addObject(self.h_ptllOvermll)

        self.h_dijetpt = ROOT.TH1F('DijetpT', 'Dijet p_{T}(jj)', 200, 0, 1000)
        self.addObject(self.h_dijetpt)

        self.h_dijetmass = ROOT.TH1F('DijetMass', 'Dijet mass m_{jj}', 200, 0, 1000)
        self.addObject(self.h_dijetmass)

        self.h_leadjetZmass = ROOT.TH1F('LeadJetZMass', 'Lead Jet + Z Mass m_{jZ}', 400, 0, 2000)
        self.addObject(self.h_leadjetZmass)

        self.h_subleadjetZmass = ROOT.TH1F('SubleadJetZMass', 'Sublead Jet + Z Mass m_{jZ}', 400, 0, 2000)
        self.addObject(self.h_subleadjetZmass)
 
        self.h_leadleppt = ROOT.TH1F('LeadLeptonpT', 'Lead Lepton p_{T}', 200, 0, 1000)
        self.addObject(self.h_leadleppt)

        self.h_subleadleppt = ROOT.TH1F('SubleadLeptonpT', 'Sublead Lepton p_{T}', 200, 0, 1000)
        self.addObject(self.h_subleadleppt)

       #Sanity Checks
        self.h_dilepmass = ROOT.TH1F('DileptonMass', 'Dilepton Mass m_{ll}', 200, 0, 1000)
        self.addObject(self.h_dilepmass)

	self.h_leadjeteta = ROOT.TH1F('LeadJetEta', 'Lead jet #eta', 100, -3, 3)
        self.addObject(self.h_leadjeteta)

	self.h_subleadjeteta = ROOT.TH1F('SubleadJetEta', 'Sublead jet #eta', 100, -3, 3)
        self.addObject(self.h_subleadjeteta)

        self.h_leadjetphi = ROOT.TH1F('LeadJetPhi', 'Lead jet #phi', 100, -4, 4)
        self.addObject(self.h_leadjetphi)

        self.h_subleadjetphi = ROOT.TH1F('SubleadJetPhi', 'Sublead jet #phi', 100, -4, 4)
        self.addObject(self.h_subleadjetphi)

        self.h_leadlepeta = ROOT.TH1F('LeadLeptonEta', 'Lead Lepton #eta', 100, -3, 3)
        self.addObject(self.h_leadlepeta)

        self.h_subleadlepeta = ROOT.TH1F('SubleadLeptonEta', 'Sublead Lepton #eta', 100, -3, 3)
        self.addObject(self.h_subleadlepeta)

        self.h_leadlepphi = ROOT.TH1F('LeadLeptonPhi', 'Lead Lepton #phi', 100, -4, 4)
        self.addObject(self.h_leadlepphi)

        self.h_subleadlepphi = ROOT.TH1F('SubleadLeptonPhi', 'Sublead Lepton #phi', 100, -4, 4)
        self.addObject(self.h_subleadlepphi)

    def analyze(self, event):
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        genparticles = Collection(event, "GenPart")

	#Two ways of accessing variables
	     #print("Lead jet mass 1: ", (jets[0].p4()).M())
	     #print("Lead jet mass 2: ", (jets[0].mass))
	
#	print "\nBEGIN EVENT"

#       print("Number of Jets is: %r") % (len(jets))	
#	for j in jets:
#           print("Jet %r: pt: %r GeV, eta: %r, phi %r") % (j, j.pt, j.eta, j.phi)

#	print("Number of RECO electrons: %r") % (len(electrons))
#	for e in electrons:
#	    print("Electron %r: pt: %r GeV, eta: %r, phi: %r") % (e, e.pt, e.eta, e.phi)

#       print("Number of RECO muons: %r") % (len(muons))	
#	for m in muons:
#	    print("Muon %r: pt: %r GeV, eta: %r, phi: %r, pdgid: %r") % (m, m.pt, m.eta, m.phi, m.pdg)

#	print("Number of GEN particles is: %r ") % (len(genparticles))
	      


####################################################################################
# Stuff
####################################################################################
	
	count = 0
	drvalues0 = []
        drvalues1 = []
        leadLep = None
        subleadLep = None

#	for i in genparticles:
#	    print("%r. pdgID is %r. Index of mother is %r") % (i, i.pdgId, i.genPartIdxMother)

        for i in genparticles:
#	    print i
	    if abs(i.pdgId) == 11 and (self.getMotherId(genparticles, i.genPartIdxMother) == 22 or self.getMotherId(genparticles, i.genPartIdxMother) == 23): #HERE'S A GEN ELECTRON WITH A Z OR PHOTON MOTHER
#	        print("%r is an ELECTRON  that has a mother which is a Z or a photon.") % (i)
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
#		print("%r is a GEN muon that has a mother which is a Z or a photon.") % (i)
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
#	    print("Unable to match RECO leptons to GEN leptons")
	    return False
     
        if leadLep == subleadLep:
	   return False

        if leadLep.pt < subleadLep.pt:
	    leadLep, subleadLep = subleadLep, leadLep
 
#	print("\nOur matched RECO leptons are: %r and %r\n") % (leadLep, subleadLep)

        if leadLep.pt < 60 or subleadLep.pt < 53 or abs(leadLep.eta) > 2.4 or abs(subleadLep.eta) > 2.4:
	    return False
       
#################################################################################################################################
# CHECKING THAT LEADING/SUBLEADING JETS AND LEADING/SUBLEADING LEPTONS ARE WELL SEPARATED (LEAD AND SUBLEAD JETS DECLARED HERE) #
#################################################################################################################################

	hitelseloop = 0
	subleadJet = None
#       print("\nChecking jets:")
        for j in jets:
	    if j.pt < 30 or abs(j.eta) > 2.4:
#		if j.pt < 30:
#	            print("%r pT is less than 30 GeV: pT = %r GeV. Skipping to next jet.") % (j, j.pt)
#		else:
#		    print("%r abs(eta) greater than 2.4: Eta = %r GeV. Skipping to next jet.") % (j, j.eta)
		continue
	    else:
	        if self.DeltaR(j,leadLep) < 0.4 or self.DeltaR(j,subleadLep) < 0.4:
#		    if self.DeltaR(j,leadLep) < 0.4:
#			print("dR between %r and the leading lepton < 0.4: dR = %r. Skipping to next jet.") % (j, self.DeltaR(j,leadLep))
#                    else:
#			print("dR between %r and the subleading lepton < 0.4: dR = %r. Skipping to next jet.") % (j, self.DeltaR(j,subleadLep))
                    continue
	        else:
		    if hitelseloop == 0:
		        leadJet = j
#		        print("The leading jet is %r.") % (leadJet)
		    else:
                        subleadJet = j
#                       print("The subleading jet is %r.") % (subleadJet)
		        break
		    hitelseloop += 1  
	
	if subleadJet is None:
#	    print("Unable to assign subleading jet. Returning false.")
	    return False 	


################################################################################################################################################################################################
        # DECLARING KINEMATIC VARIABLES                                                                                          #
################################################################################################################################################################################################

	#Defining jet variables
        leadJetPt = leadJet.pt
        subleadJetPt = subleadJet.pt

        leadJetEta = leadJet.eta
        subleadJetEta = subleadJet.eta

        leadJetPhi = leadJet.phi
        subleadJetPhi = subleadJet.phi

        diJetMass = (leadJet.p4() + subleadJet.p4()).M()
        diJetPt = (leadJet.p4() + subleadJet.p4()).Pt()

        #Defining lepton variables
        leadLepPt = leadLep.pt
        subleadLepPt = subleadLep.pt

        leadLepEta = leadLep.eta
        subleadLepEta = subleadLep.eta

        leadLepPhi = leadLep.phi
        subleadLepPhi = subleadLep.phi
        
        diLepMass = (leadLep.p4() + subleadLep.p4()).M()
        diLepPt = (leadLep.p4() + subleadLep.p4()).Pt()
   
        PtllOverMll = (leadLep.p4() + subleadLep.p4()).Pt()/(leadLep.p4() + subleadLep.p4()).M()

	#Lepton and Jet Variables
        fourObjectInvariantMass = (leadJet.p4() + subleadJet.p4() + leadLep.p4() + subleadLep.p4()).M()	 
        leadJetZMass = (leadJet.p4() + leadLep.p4() + subleadLep.p4()).M()
        subleadJetZMass = (subleadJet.p4() + leadLep.p4() + subleadLep.p4()).M()

#################################################################################################################################################################################################
        #FILLING HISTOGRAMS
#################################################################################################################################################################################################

        self.h_fourobjectmass.Fill(fourObjectInvariantMass)
        self.h_leadjetZmass.Fill(leadJetZMass)
        self.h_subleadjetZmass.Fill(subleadJetZMass)
        
        self.h_leadjetpt.Fill(leadJetPt)
        self.h_subleadjetpt.Fill(subleadJetPt)
        self.h_dijetmass.Fill(diJetMass)
        self.h_dijetpt.Fill(diJetPt)

        self.h_leadjeteta.Fill(leadJetEta)
        self.h_subleadjeteta.Fill(subleadJetEta)
        self.h_leadjetphi.Fill(leadJetPhi)
        self.h_subleadjetphi.Fill(subleadJetPhi)

        self.h_leadleppt.Fill(leadLepPt)
        self.h_subleadleppt.Fill(subleadLepPt)
        self.h_dilepmass.Fill(diLepMass)
        self.h_dileppt.Fill(diLepPt)
        self.h_ptllOvermll.Fill(PtllOverMll)

        self.h_leadlepeta.Fill(leadLepEta)
        self.h_subleadlepeta.Fill(subleadLepEta)
        self.h_leadlepphi.Fill(leadLepPhi)
        self.h_subleadlepphi.Fill(subleadLepPhi)


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

        # select events with at least 2 muons
#        if len(muons) >= 2:
#            for lep in muons:  # loop on muons
#                eventSum += lep.p4()
#            for lep in electrons:  # loop on electrons
#                eventSum += lep.p4()
#            for j in jets:  # loop on jets
#                eventSum += j.p4()
#           self.h_vpt.Fill(eventSum.Pt())  # fill histogram

#       print("END EVENT\n")

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
#       print("dR between %r and %r: dR = %r") % (i, j, self.DeltaR(i,j)) #Computes the dR bewteen the GEN lepton and every RECO lepton
            dRvals.append(self.DeltaR(genpar,lep))
#       print("The dR values of %r are: %r") % (genpar, dRvals)
        idx1 = self.getLeptons(dRvals, len(leptons))
        leadLepton = leptons[idx1]
        return leadLepton

    def getLeptons(self, dR_Values, length):
	smallest_value = dR_Values[0]
	index = 0
	index1 = 0
#	print("Assuming the minimum is %r at index %r") %(smallest_value, index)
#	print("Entering for loop:")
	for value in dR_Values:
#	    print("Looking at the value %r at index %r") % (value, index)
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
#           print("Now the minimum is %r at index %r") % (smallest_value, index1)
#       print("The correct dR value is  %r at index %r") % (smallest_value, index1)
        return index1

preselection = "(nElectron.size() >= 2 || nMuon.size() >=2) && (nGenPart >= 2) && (nJet.size() >=2)"

files = [" root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/280000/DF896280-DF2F-D748-ABCB-FC055EE6CC96.root"]
#files = [" root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_HT-70to100_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/270000/088661DE-FACE-A94C-925A-54AAEF6F3DCF.root", " root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/280000/C5FC268A-8CB9-CD4B-A2B2-6BA6C3682C54.root", " root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/130000/2D91D1A8-9AA4-9342-8FF4-831D18A023E2.root", " root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/70000/EC850326-C715-634C-A49A-C5A3E6836794.root", " root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/270000/AF40878C-BED6-0B41-8F21-9F2F661DEC65.root", " root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/280000/535D7D65-C9BB-FB40-9BB9-6CCFEB9B5356.root", " root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/280000/50E410D5-1103-4648-BE10-12BA80354B31.root", " root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/260000/0132FCFD-2353-2249-B586-77BB49034EF6.root"]
#files = open("files.txt", "r") 
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[
                  ExampleAnalysis()], noOut=True, histFileName="DY_nanoAOD_Hists.root", histDirName="plots")
p.run()
