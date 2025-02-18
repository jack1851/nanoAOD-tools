#!/usr/bin/env python
from importlib import import_module
import os
import sys
import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

class eventHistos:
    def __init__(self, directoryName):
   	self.directoryName = directoryName
	self.h_eventcount = ROOT.TH1F('EventCount', 'Event Count', 1, 0, 1)
        self.h_eventweight = ROOT.TH1F('EventWeight', 'Event Weight', 200, -100, 100)
        self.h_fourobjectinvariantmass = ROOT.TH1F('FourObjectInvariantMass', 'Four Object Invariant Mass m_{lljj}', 1600, 0, 8000)
	self.h_q2input = ROOT.TH1F('Q2In', 'Initial q^{2}', 1000, 0, 100000000)
        self.h_q2ZBoson = ROOT.TH1F('Q2Z', 'q^{2}_{Z}', 50000, 0, 25000000)
	self.h_qdifference = ROOT.TH1F('Qhad', '\sqrt{q^{2}_{in} - q^{2}_{Z}} ', 1000, 0, 10000)
        self.h_fourobjectinvariantpt = ROOT.TH1F('FourObjectInvariantpT', 'Four Object pT p_{T}(lljj)', 200, 0, 1000)
        self.h_leadjetpt = ROOT.TH1F('LeadJetpT', 'Lead jet p_{T}', 400, 0, 2000)
        self.h_subleadjetpt = ROOT.TH1F('SubleadJetpT', 'Sublead jet p_{T}', 200, 0, 1000)
        self.h_dileppt = ROOT.TH1F('DileptonpT', 'Dilepton p_{T}(ll)', 200, 0, 1000)
        self.h_ptllOvermll = ROOT.TH1F('PtllOverMll', 'p_{T}^{ll}/m_{ll}', 2000, 0, 100)
        self.h_dijetpt = ROOT.TH1F('DijetpT', 'Dijet p_{T}(jj)', 1600, 0, 8000)
        self.h_dijetmass = ROOT.TH1F('DijetMass', 'Dijet mass m_{jj}', 1600, 0, 8000)
	self.h_ptjjOvermjj = ROOT.TH1F('PtjjOverMjj', 'p_{T}^{jj}/m_{jj}', 2000, 0, 100)
        self.h_leadjetZmass = ROOT.TH1F('LeadJetZMass', 'Lead Jet + Z Mass m_{jZ}', 1600, 0, 8000)
        self.h_subleadjetZmass = ROOT.TH1F('SubleadJetZMass', 'Sublead Jet + Z Mass m_{jZ}', 1600, 0, 8000)
        self.h_leadleppt = ROOT.TH1F('LeadLeptonpT', 'Lead Lepton p_{T}', 400, 0, 2000)
        self.h_subleadleppt = ROOT.TH1F('SubleadLeptonpT', 'Sublead Lepton p_{T}', 400, 0, 2000)
        self.h_dilepmass = ROOT.TH1F('DileptonMass', 'Dilepton Mass m_{ll}', 1000, 0, 5000)
        self.h_leadjeteta = ROOT.TH1F('LeadJetEta', 'Lead jet #eta', 600, -3, 3)
        self.h_subleadjeteta = ROOT.TH1F('SubleadJetEta', 'Sublead jet #eta', 600, -3, 3)
        self.h_leadjetphi = ROOT.TH1F('LeadJetPhi', 'Lead jet #phi', 800, -4, 4)
        self.h_subleadjetphi = ROOT.TH1F('SubleadJetPhi', 'Sublead jet #phi', 800, -4, 4)
        self.h_leadlepeta = ROOT.TH1F('LeadLeptonEta', 'Lead Lepton #eta', 600, -3, 3)
        self.h_subleadlepeta = ROOT.TH1F('SubleadLeptonEta', 'Sublead Lepton #eta', 600, -3, 3)
        self.h_leadlepphi = ROOT.TH1F('LeadLeptonPhi', 'Lead Lepton #phi', 800, -4, 4)
        self.h_subleadlepphi = ROOT.TH1F('SubleadLeptonPhi', 'Sublead Lepton #phi', 800, -4, 4)
        self.h_leadJetAndZPtHisto = ROOT.TH2F("leadJetAndZPt" , ";Lead jet p_{T} (GeV);Z p_{T} (GeV)" , 100 , 0 , 1000 , 100, 0, 1000);
        self.h_leadJetAndmjj = ROOT.TH2F("leadJetAndmjj" , ";Lead jet p_{T} (GeV); m_{jj}" , 200 , 0 , 2000 , 200, 0, 2000);
        self.h_leadJetAndptjj = ROOT.TH2F("leadJetAndptjj" , ";Lead jet p_{T} (GeV); p_{T}^{jj}" , 200 , 0 , 2000 , 200, 0, 2000);

    def eventweights(self, event):
        self.h_eventweight.Fill(event.eventWeight)

    def FillHists(self, event):
	self.h_eventcount.Fill(0.5, event.eventWeight)
        self.h_fourobjectinvariantmass.Fill(event.fourObjectInvariantMass, event.eventWeight)	
        self.h_fourobjectinvariantpt.Fill(event.fourObjectInvariantPt, event.eventWeight)
        self.h_leadjetpt.Fill(event.leadJetPt, event.eventWeight)
        self.h_subleadjetpt.Fill(event.subleadJetPt, event.eventWeight)
        self.h_leadjeteta.Fill(event.leadJetEta, event.eventWeight)
        self.h_subleadjeteta.Fill(event.subleadJetEta, event.eventWeight)
        self.h_leadjetphi.Fill(event.leadJetPhi, event.eventWeight)
        self.h_subleadjetphi.Fill(event.subleadJetPhi, event.eventWeight)
        self.h_dijetmass.Fill(event.diJetMass, event.eventWeight)
        self.h_dijetpt.Fill(event.diJetPt, event.eventWeight)
	self.h_ptjjOvermjj.Fill(event.PtjjOverMjj, event.eventWeight)
        self.h_leadleppt.Fill(event.leadLepPt, event.eventWeight)
        self.h_subleadleppt.Fill(event.subleadLepPt, event.eventWeight)
        self.h_leadlepeta.Fill(event.leadLepEta, event.eventWeight)
        self.h_subleadlepeta.Fill(event.subleadLepEta, event.eventWeight)
        self.h_leadlepphi.Fill(event.leadLepPhi, event.eventWeight)
        self.h_subleadlepphi.Fill(event.subleadLepPhi, event.eventWeight)
        self.h_dilepmass.Fill(event.diLepMass, event.eventWeight)

        self.h_dileppt.Fill(event.diLepPt,event.eventWeight*event.Zreweights)

        self.h_ptllOvermll.Fill(event.PtllOverMll, event.eventWeight)
        self.h_leadjetZmass.Fill(event.leadJetZMass, event.eventWeight)
        self.h_subleadjetZmass.Fill(event.subleadJetZMass, event.eventWeight)
	self.h_q2input.Fill(event.q2in, event.eventWeight)
        self.h_q2ZBoson.Fill(event.q2Z, event.eventWeight)
        self.h_qdifference.Fill(event.qhad, event.eventWeight)

        self.h_leadJetAndZPtHisto.Fill(event.leadJetPt, event.diLepPt, event.eventWeight)
        self.h_leadJetAndmjj.Fill(event.leadJetPt, event.diJetMass, event.eventWeight)
        self.h_leadJetAndptjj.Fill(event.leadJetPt, event.diJetPt, event.eventWeight)

    def WriteHists(self):
        self.h_eventweight.Write()
	self.h_eventcount.Write()
	self.h_q2input.Write()
        self.h_q2ZBoson.Write()
        self.h_qdifference.Write()
        self.h_fourobjectinvariantmass.Write()
	self.h_leadjetpt.Write()
        self.h_subleadjetpt.Write()
        self.h_ptllOvermll.Write()
        self.h_ptjjOvermjj.Write()
        self.h_dileppt.Write()
        self.h_leadjetZmass.Write()
        self.h_subleadjetZmass.Write()
        self.h_dijetmass.Write()
        self.h_dijetpt.Write()
        self.h_leadleppt.Write()
        self.h_subleadleppt.Write()
        self.h_dilepmass.Write()
	self.h_fourobjectinvariantpt.Write()
        self.h_leadjeteta.Write()
        self.h_subleadjeteta.Write()
        self.h_leadjetphi.Write()
        self.h_subleadjetphi.Write()
        self.h_leadlepeta.Write()
        self.h_subleadlepeta.Write()
        self.h_leadlepphi.Write()
        self.h_subleadlepphi.Write()
        self.h_leadJetAndZPtHisto.Write()
        self.h_leadJetAndmjj.Write()
        self.h_leadJetAndptjj.Write()
