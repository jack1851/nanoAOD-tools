#!/usr/bin/env python
#from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
#from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
#from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

class eventHistos(object):

    h_eventweight = ROOT.TH1F('EventWeight', 'Event Weight', 200, -100, 100)
    h_fourobjectinvariantmass = ROOT.TH1F('FourObjectInvariantMass', 'Four Object Invariant Mass m_{lljj}', 1600, 0, 8000)
    h_leadjetpt = ROOT.TH1F('LeadJetpT', 'Lead jet p_{T}', 200, 0, 1000)
    h_subleadjetpt = ROOT.TH1F('SubleadJetpT', 'Sublead jet p_{T}', 200, 0, 1000)
    h_dileppt = ROOT.TH1F('DileptonpT', 'Dilepton p_{T}(ll)', 200, 0, 1000)
    h_ptllOvermll = ROOT.TH1F('PtllOverMll', 'p_{T}^{ll}/m_{ll}', 200, 0, 10)
    h_dijetpt = ROOT.TH1F('DijetpT', 'Dijet p_{T}(jj)', 200, 0, 1000)
    h_dijetmass = ROOT.TH1F('DijetMass', 'Dijet mass m_{jj}', 200, 0, 1000)
    h_leadjetZmass = ROOT.TH1F('LeadJetZMass', 'Lead Jet + Z Mass m_{jZ}', 400, 0, 2000)
    h_subleadjetZmass = ROOT.TH1F('SubleadJetZMass', 'Sublead Jet + Z Mass m_{jZ}', 400, 0, 2000)
    h_leadleppt = ROOT.TH1F('LeadLeptonpT', 'Lead Lepton p_{T}', 200, 0, 1000)
    h_subleadleppt = ROOT.TH1F('SubleadLeptonpT', 'Sublead Lepton p_{T}', 200, 0, 1000)
    h_dilepmass = ROOT.TH1F('DileptonMass', 'Dilepton Mass m_{ll}', 200, 0, 1000)
    h_leadjeteta = ROOT.TH1F('LeadJetEta', 'Lead jet #eta', 100, -3, 3)
    h_subleadjeteta = ROOT.TH1F('SubleadJetEta', 'Sublead jet #eta', 100, -3, 3)
    h_leadjetphi = ROOT.TH1F('LeadJetPhi', 'Lead jet #phi', 100, -4, 4)
    h_subleadjetphi = ROOT.TH1F('SubleadJetPhi', 'Sublead jet #phi', 100, -4, 4)
    h_leadlepeta = ROOT.TH1F('LeadLeptonEta', 'Lead Lepton #eta', 100, -3, 3)
    h_subleadlepeta = ROOT.TH1F('SubleadLeptonEta', 'Sublead Lepton #eta', 100, -3, 3)
    h_leadlepphi = ROOT.TH1F('LeadLeptonPhi', 'Lead Lepton #phi', 100, -4, 4)
    h_subleadlepphi = ROOT.TH1F('SubleadLeptonPhi', 'Sublead Lepton #phi', 100, -4, 4)

    def __init__(self, directoryName):
   	self.directoryName = directoryName
 
    def eventweights(self, event):
	self.directoryName.cd()
        self.h_eventweight.Fill(event.eventWeight)
 
    def FillHists(self, event):
	self.directoryName.cd()    
        self.h_fourobjectinvariantmass.Fill(event.fourObjectInvariantMass, event.eventWeight)	
#        self.h_leadjetpt.Fill(event.leadJetPt, event.eventWeight)
#        self.h_subleadjetpt.Fill(event.subleadJetPt, event.eventWeight)
#        self.h_leadjeteta.Fill(event.leadJetEta, event.eventWeight)
#        self.h_subleadjeteta.Fill(event.subleadJetEta, event.eventWeight)
#        self.h_leadjetphi.Fill(event.leadJetPhi, event.eventWeight)
#        self.h_subleadjetphi.Fill(event.subleadJetPhi, event.eventWeight)
#        self.h_dijetmass.Fill(event.diJetMass, event.eventWeight)
#        self.h_dijetpt.Fill(event.diJetPt, event.eventWeight)
#        self.h_leadleppt.Fill(event.leadLepPt, event.eventWeight)
#        self.h_subleadleppt.Fill(event.subleadLepPt, event.eventWeight)
 #       self.h_leadlepeta.Fill(event.leadLepEta, event.eventWeight)
 #       self.h_subleadlepeta.Fill(event.subleadLepEta, event.eventWeight)
 #       self.h_leadlepphi.Fill(event.leadLepPhi, event.eventWeight)
 #       self.h_subleadlepphi.Fill(event.subleadLepPhi, event.eventWeight)
 #       self.h_dilepmass.Fill(event.diLepMass, event.eventWeight)
 #       self.h_dileppt.Fill(event.diLepPt, event.eventWeight)
 #       self.h_ptllOvermll.Fill(event.PtllOverMll, event.eventWeight)
 #       self.h_leadjetZmass.Fill(event.leadJetZMass, event.eventWeight)
 #       self.h_subleadjetZmass.Fill(event.subleadJetZMass, event.eventWeight)

    def WriteHists(self):
	self.directoryName.cd()
        self.h_eventweight.Write()
        self.h_fourobjectinvariantmass.Write()
#        self.h_leadjetpt.Write()
#        self.h_subleadjetpt.Write()
#        self.h_leadjeteta.Write()
#        self.h_subleadjeteta.Write()
#        self.h_leadjetphi.Write()
#        self.h_subleadjetphi.Write()
#        self.h_dijetmass.Write()
#        self.h_dijetpt.Write()
#        self.h_leadleppt.Write()
#        self.h_subleadleppt.Write()
#        self.h_leadlepeta.Write()
#        self.h_subleadlepeta.Write()
#        self.h_leadlepphi.Write()
#        self.h_subleadlepphi.Write()
#        self.h_dilepmass.Write()
#        self.h_dileppt.Write()
#        self.h_ptllOvermll.Write()
#        self.h_leadjetZmass.Write()
       # self.h_subleadjetZmass.Write()
