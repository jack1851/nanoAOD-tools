#!/usr/bin/env python

import ROOT
import copy
import math
import array

class mcFile:
   def __init__(self, inputfile, name, cross, fillcolor):
      self.infile=inputfile
      self.label=name
      self.cx=cross
      self.color=fillcolor

class stackInfo:
   def __init__(self, mc, lumi, precr, preda, data=None, xsec=None):
      self.mcFiles = mc
      self.lumi = lumi
      self.precr = precr
      self.preda = preda
      self.dataFile=data
      self.dataFile_xsec = xsec

   def plotAll(self, basedir, tag,outDir):
       #Histogram name, X-axis label, Log Scale, Title, Output Directory, Rebin
       self.stack("FourObjectInvariantMass","m_{lljj} (GeV)",True,tag,outDir, True)
       self.stack("LeadJetpT","p_{T} of the leading jet (GeV)",True,tag,outDir, True)
       self.stack("SubleadJetpT","p_{T} of the subleading jet (GeV)",True,tag,outDir, True)
       self.stack("PtllOverMll","p_{T}^{ll}/m_{ll}",True,tag,outDir, True)
       self.stack("DileptonpT","p_{T}^{ll} (GeV)",True,tag,outDir, True)
#       self.stack("LeadJetZMass","Mass of the leading jet and Z (GeV)",True,tag,outDir, True)
#       self.stack("SubleadJetZMass","Mass of the subleading jet and Z (GeV)",True,tag,outDir, True)
#       self.stack("DijetMass","m_{jj} (GeV)",True,tag,outDir, True)
#       self.stack("DijetpT","p_{T}^{jj} (GeV)",True,tag,outDir, True)
       self.stack("LeadLeptonpT","p_{T} of the leading lepton (GeV)",True,tag,outDir, True)
       self.stack("SubleadLeptonpT","p_{T} of the subleading lepton (GeV)",True,tag,outDir, True)
       self.stack("DileptonMass","m_{ll} (GeV)",True,tag,outDir, True)
       self.stack("LeadJetEta","#eta of the leading jet",True,tag,outDir, True)
       self.stack("SubleadJetEta","#eta of the subleading jet",True,tag,outDir, True)
       self.stack("LeadJetPhi","#phi of the leading jet",True,tag,outDir, True)
       self.stack("SubleadJetPhi","#phi of the subleading jet",True,tag,outDir, True)
       self.stack("LeadLeptonEta","#eta of the leading lepton",True,tag,outDir, True)
       self.stack("SubleadLeptonEta","#eta of the subleading lepton",True,tag,outDir, True)
       self.stack("LeadLeptonPhi","#phi of the leading lepton",True,tag,outDir, True)
       self.stack("SubleadLeptonPhi","#phi of the subleading lepton",True,tag,outDir, True)

   def getRatio(self, hist, reference):
        ratio = hist.Clone("%s_ratio"%hist.GetName())
        ratio.SetDirectory(0)
        ratio.SetLineColor(hist.GetLineColor())
        for xbin in xrange(1,reference.GetNbinsX()+1):
                ref = reference.GetBinContent(xbin)
                val = hist.GetBinContent(xbin)

                refE = reference.GetBinError(xbin)
                valE = hist.GetBinError(xbin)

                try:
                        ratio.SetBinContent(xbin, val/ref)
                        ratio.SetBinError(xbin, math.sqrt( (val*refE/(ref**2))**2 + (valE/ref)**2 ))
                except ZeroDivisionError:
                        #ratio.SetBinContent(xbin, 1.0)
                        ratio.SetBinError(xbin, 0.0)

        return ratio

   def TOTerror(self, hmc, ratio ):
      hmc.Sumw2()
      den1 = hmc.Clone ("den1");
      den2 = hmc.Clone ("den2");

      nvar = hmc.GetNbinsX();

      x1 = []
      y1 = []
      exl1 = []
      eyl1= []
      exh1= []
      eyh1= []

      for km in range(1,nvar+1):
        delta = hmc.GetBinError(km)
        den1.SetBinError(km,0)

      # ratio from variation and nominal
      ratiop = hmc.Clone("ratiop");
      ratiom = hmc.Clone("ratiom");

      ratiop.Divide(den1);
      ratiom.Divide(den1);
      #den1.Divide(ratiop)
      #den2.Divide(ratiom)

      return ratiop;
#***********************************************************************************************
# Calculate the efficiency scale factor (event count / event weight)                           *
#***********************************************************************************************
   def calcScaleFactor(self,name,inputFile, pref):
       print "eventCount: ", inputFile.Get(pref+name).Integral()
       print "eventWeight: ", inputFile.Get(pref+"EventWeight").Integral()
       eff = inputFile.Get(pref+name).Integral()/inputFile.Get(pref+"EventWeight").Integral() #eff = eventCount/eventWeight
       return eff

   def stack(self, name, xtitle, log, tag, outDir,rebin=False):
      stackplot = ROOT.THStack("stack","")
      print "NAME", name
      print "Formatting legend"
      leg = ROOT.TLegend(0.50,0.72,0.8,0.77)
      leg.SetBorderSize(0)
      leg.SetTextSize(0.035)
      leg.SetTextFont(62)
      leg2 = ROOT.TLegend(0.50,0.77,0.8,0.82)
      leg2.SetBorderSize(0)
      leg2.SetTextSize(0.035)
      leg2.SetTextFont(62)

#*************************************************************
# Create variable bin sizes                                  *
#*************************************************************
      print "Rebin formatting"
      if(rebin):
          if("FourObjectInvariantMass" in name):
              binBoundaries = [800,1000,1200,1400,1600, 2000,2400,2800, 3200, 8000]
          elif ("LeadJetpT" in name):
              binBoundaries = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
          elif ("SubleadJetpT" in name):
              binBoundaries = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]          
          elif("PtllOverMll" in name):
              binBoundaries = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
          elif ("DileptonpT" in name):
              binBoundaries = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
#          elif ("LeadJetZMass" in name):
#              binBoundaries = [800,1000,1200,1400,1600, 2000,2400,2800, 3200, 8000]
#          elif ("SubleadJetZMass" in name):
#              binBoundaries = [800,1000,1200,1400,1600, 2000,2400,2800, 3200, 8000]
#          elif ("DijetMass" in name):
#              binBoundaries = [800,1000,1200,1400,1600, 2000,2400,2800, 3200, 8000]
#          elif ("DijetpT" in name):
#              binBoundaries = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
          elif ("LeadLeptonpT" in name):
              binBoundaries = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
          elif ("SubleadLeptonpT" in name):
              binBoundaries = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
          elif ("DileptonMass" in name):
              binBoundaries = [60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
          elif ("LeadJetEta" in name):
              binBoundaries = [-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3]
          elif ("SubleadJetEta" in name):
              binBoundaries = [-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3]
          elif ("LeadJetPhi" in name):
              binBoundaries = [-4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
          elif ("SubleadJetPhi" in name):
              binBoundaries = [-4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
          elif ("LeadLeptonEta" in name):
              binBoundaries = [-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3]
          elif ("SubleadLeptonEta" in name):
              binBoundaries = [-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3]
          elif ("LeadLeptonPhi" in name):
              binBoundaries = [-4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
          elif ("SubleadLeptonPhi" in name):
              binBoundaries = [-4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
          binBoundariesArray = array.array('d', binBoundaries)

#*************************************************************
# Renormalize Histograms to 1 or the luminosity              *
#*************************************************************
      hists = []
      datahists = []
      count = 0
      print "Entering for loop of files"
      for mcFile in self.mcFiles:
	  print("\n%r") % (mcFile.infile)
	  eff = self.calcScaleFactor(name,mcFile.infile, self.precr)
          Nevents = mcFile.cx*1000*float(self.lumi)*eff
	  print("name: %r, eff: %r, X-sec: %r pb, lumi: %r, Nevents: %r") % (name, eff, mcFile.cx, float(self.lumi), Nevents)

	  hist=(mcFile.infile.Get(self.precr+name).Clone()) #Clones the current histogram into a variable called hist.
          print "HIST: ", hist
          if(hist.Integral()>0):
	      print "Integral before scaling: ", hist.Integral()
#              hist.Scale(1.0/hist.Integral())
              hist.Scale(Nevents/hist.Integral())
              print "Integral after scaling to 1: ", hist.Integral()
          
          hist.SetFillColor(mcFile.color) #Fill with the color defined in allVariableStacks.py
          hist.SetLineWidth(0) # Outlines the different MC files
          hist.SetDirectory(0) # Don't know what this does

          if(rebin):
              hist_Rebin = hist.Rebin(len(binBoundariesArray) - 1,"hnew",binBoundariesArray)

	      for i in range(1,hist_Rebin.GetNbinsX()+1):
	          binWidth = binBoundaries[i] - binBoundaries[i-1]
                  hist_Rebin.SetBinContent(i,hist_Rebin.GetBinContent(i))
                  hist_Rebin.SetBinError(i,hist_Rebin.GetBinError(i))

              print "Rebinned integral:", hist_Rebin.Integral()
              hist_Rebin.SetDirectory(0) # Don't know what this does      
              hists.append(hist_Rebin)
          else:
              hists.append(hist)

	  if count < 1:
            leg.AddEntry(hist_Rebin, mcFile.label,"f")
	  count += 1

      print "exiting for loop"
      print "Getting new data hist file"
     
      print "self.preda+name: ", self.preda+name
 
      dataHist=self.dataFile.Get(self.preda+name).Clone() #Clones the current histogram into a variable called hist.
      eff = self.calcScaleFactor(name,self.dataFile,self.preda)
      Nevents = self.dataFile_xsec*1000*float(self.lumi)*eff*0.5
      if(dataHist.Integral()>0):
        # print "mll > 200 integral:", dataHist.Integral()
#         dataHist.Scale(1.0/dataHist.Integral())
          dataHist.Scale(Nevents/dataHist.Integral())


      for hist in hists:
         hist.Sumw2() #Create structure to store sum of squares of weights.
         stackplot.Add(hist)


#**************************************************************************************
# Create a new canvas with a predefined size form.
# By default ROOT creates a default style that can be accessed via the gStyle pointer.                                    *
#**************************************************************************************
      plot= ROOT.TCanvas("stackplot","stackplot",2) #TCanvas(const char *name, const char *title="", Int_t form=1)
      ROOT.gStyle.SetTextFont(43)
      ROOT.gStyle.SetPadTickY(1)
      ROOT.gStyle.SetPadTickX(1)

      pad1 = ROOT.TPad("pad1","pad1",0,0.23,1,1)
      pad2 = ROOT.TPad('pad2','pad2',0,0.0,1.0,0.22)
      pad1.SetBottomMargin(0.02)
      pad2.SetTopMargin(0.03)
      pad2.SetBottomMargin(0.35)

      pad1.SetFillStyle(4000)
      pad1.SetFrameFillStyle(1000)
      pad1.SetFrameFillColor(0)
      pad2.SetFillStyle(4000)
      pad2.SetFrameFillStyle(1000)
      pad2.SetFrameFillColor(0)
      pad1.Draw()
      pad2.Draw()
      pad1.cd()


#*******************************************************************************************************
      dataHist.Sumw2()
      dataHist.SetLineWidth(1)
      dataHist.SetLineColor(1)
      dataHist.SetMarkerStyle(20)
      dataHist.SetMarkerSize(0.5)
      if(rebin):
         #dataHist.Rebin(4)
         dataHist_Rebin = dataHist.Rebin(len(binBoundariesArray)-1,"hnew",binBoundariesArray)

      for i in range(1,dataHist_Rebin.GetNbinsX()+1):
         binWidth = binBoundaries[i]-binBoundaries[i-1]
         dataHist_Rebin.SetBinContent(i,dataHist_Rebin.GetBinContent(i))
         dataHist_Rebin.SetBinError(i,dataHist_Rebin.GetBinError(i))
      
      dataHist_Rebin.SetStats(0)

   
#      print "stackplot.Integral(): ", stackplot.GetStack().Last().Integral()
#      print "Data Integral: ", dataHist_Rebin.Integral()
#      stackplot.GetStack().Last().Scale(dataHist_Rebin.Integral()/stackplot.GetStack().Last().Integral())
#      print "stackplot.Integral() new: ", stackplot.GetStack().Last().Integral()
#      print "Data Integral new: ", dataHist_Rebin.Integral()

#      test.draw("hist")
      stackplot.Draw("hist")
     #print "dataHist.Integral(): ", dataHist_Rebin.Integral()
      dataHist_Rebin.Draw("pesame") 
#**************************************************************************************
# Format the y-axis depending on whether or not to log                                *
#**************************************************************************************
      print "Formatting the log axis"
      if(log):
	 pad1.SetLogy()
         ROOT.gPad.SetLogy()
         if("FourObjectInvariantMass" in name):
             stackplot.SetMinimum(3.75)
             stackplot.SetMaximum(1.5e6)
             stackplot.GetYaxis().SetTitle("Events / bin")
         elif ("LeadJetpT" in name):
             stackplot.SetMinimum(3.75)
             stackplot.SetMaximum(1.5e6)
             stackplot.GetYaxis().SetTitle("Events / 50 GeV")
         elif ("SubleadJetpT" in name):
             stackplot.SetMinimum(3.75)
             stackplot.SetMaximum(1.5e6)
             stackplot.GetYaxis().SetTitle("Events / 50 GeV")
         elif("PtllOverMll" in name):
             stackplot.SetMinimum(3.75)
             stackplot.SetMaximum(1.5e6)
             stackplot.GetYaxis().SetTitle("Events / 1.00")
         elif ("DileptonpT" in name):
             stackplot.SetMinimum(3.75)
             stackplot.SetMaximum(1.5e6)
             stackplot.GetYaxis().SetTitle("Events / 50 GeV")
#         elif ("LeadJetZMass" in name):
#             stackplot.SetMinimum(3.75)
#             stackplot.SetMaximum(1.5e6)
#             stackplot.GetYaxis().SetTitle("Events / bin")
#         elif ("SubleadJetZMass" in name):
#             stackplot.SetMinimum(3.75)
#             stackplot.SetMaximum(1.5e6)
#             stackplot.GetYaxis().SetTitle("Events / bin")
#         elif ("DijetMass" in name):
#             stackplot.SetMinimum(3.75)
#             stackplot.SetMaximum(1.5e6)
#             stackplot.GetYaxis().SetTitle("Events / 50 GeV")
##         elif ("DijetpT" in name):
##             stackplot.SetMinimum(3.75)
#             stackplot.SetMaximum(1.5e6)
#             stackplot.GetYaxis().SetTitle("Events / 50 GeV")
         elif ("LeadLeptonpT" in name):
             stackplot.SetMinimum(3.75)
             stackplot.SetMaximum(1.5e6)
             stackplot.GetYaxis().SetTitle("Events / 50 GeV")
         elif ("SubleadLeptonpT" in name):
             stackplot.SetMinimum(3.75)
             stackplot.SetMaximum(1.5e6)
             stackplot.GetYaxis().SetTitle("Events / 50 GeV")
         elif ("DileptonMass" in name):
             stackplot.SetMinimum(3.75)
             stackplot.SetMaximum(1.5e6)
             stackplot.GetYaxis().SetTitle("Events / 10 GeV")
         elif ("LeadJetEta" in name):
             stackplot.SetMinimum(3.75)
             stackplot.SetMaximum(1.5e6)
             stackplot.GetYaxis().SetTitle("Events / 0.50")
         elif ("SubleadJetEta" in name):
             stackplot.SetMinimum(3.75)
             stackplot.SetMaximum(1.5e6)
             stackplot.GetYaxis().SetTitle("Events / 0.50")
         elif ("LeadJetPhi" in name):
             stackplot.SetMinimum(3.75)
             stackplot.SetMaximum(1.5e6)
             stackplot.GetYaxis().SetTitle("Events / 0.50")
         elif ("SubleadJetPhi" in name):
             stackplot.SetMinimum(3.75)
             stackplot.SetMaximum(1.5e6)
             stackplot.GetYaxis().SetTitle("Events / 0.50")
         elif ("LeadLeptonEta" in name):
             stackplot.SetMinimum(3.75)
             stackplot.SetMaximum(1.5e6)
             stackplot.GetYaxis().SetTitle("Events / 0.50")
         elif ("SubleadLeptonEta" in name):
             stackplot.SetMinimum(3.75)
             stackplot.SetMaximum(1.5e6)
             stackplot.GetYaxis().SetTitle("Events / 0.50")
         elif ("LeadLeptonPhi" in name):
             stackplot.SetMinimum(3.75)
             stackplot.SetMaximum(1.5e6)
             stackplot.GetYaxis().SetTitle("Events / 0.50")
         elif ("SubleadLeptonPhi" in name):
             stackplot.SetMinimum(3.75)
             stackplot.SetMaximum(1.5e6)
             stackplot.GetYaxis().SetTitle("Events / 0.50")

      if not log:
         stackplot.SetMinimum(0) 
      
      stackplot.GetXaxis().SetTitleOffset(2)
      stackplot.GetXaxis().SetTitle("")
      stackplot.GetXaxis().SetTickSize(0)
      stackplot.Draw("hist")
      if self.dataFile is not None:
         dataHist_Rebin.Draw("psame") 

      newDataHist = copy.deepcopy(dataHist_Rebin)

      allMC = stackplot.GetStack().Last().Clone()

      herr = allMC.Clone('herr')
      theErrorGraph = ROOT.TGraphErrors(herr)
      theErrorGraph.SetFillColor(ROOT.kGray+2)
      theErrorGraph.SetFillStyle(3002)
      herr.SetFillColor(ROOT.kGray+2)
      herr.SetFillStyle(3002)
      herr.SetMarkerColor(1111)

      theErrorGraph.Draw('SAME2')

      leg2.AddEntry(dataHist, "Pseudodata", "PE1l") 

#**************************************************************************************
# Format the x-axis and the y axis                                                                  *
#**************************************************************************************

#**************************************************************************************
# Draw the legend                                                                     *
#**************************************************************************************
      leg.Draw()
      leg2.Draw()
#**************************************************************************************
# Create and draw all of the labels                                                   *
#**************************************************************************************      
      label = ROOT.TLatex(0.66,0.905,"%.2f fb^{-1} (13 TeV)" % float(self.lumi))
      label.SetNDC()
      label.SetTextFont(42)
      label.SetTextSize(0.04)
      label.Draw()

#**************************************************************************************
# Format the x-axis and the y axis                                                                  *
#**************************************************************************************
      stackplot.GetXaxis().SetTitleOffset(2)
      stackplot.GetXaxis().SetTitle("")
#     stackplot.GetXaxis().SetRangeUser(800,8000)
#      stackpaot.GetXaxis().SetTitleSize(20)
      stackplot.GetXaxis().SetTickSize(0.02)
      stackplot.GetXaxis().SetLabelSize(0)
#     stackplot.Draw("hist")

      stackplot.GetYaxis().SetTitleSize(20)
      stackplot.GetYaxis().SetTitleFont(43)
      stackplot.GetYaxis().SetLabelFont(43)
      stackplot.GetYaxis().SetLabelSize(15)
      stackplot.GetYaxis().SetTitleOffset(1.2)

      lab_x0 = 0.10
      lab_y0 = 0.905

      tag1 = ROOT.TLatex(lab_x0,lab_y0,"CMS")
      tag1.SetNDC()
      tag1.SetTextFont(62)
      tag1.SetTextSize(0.045)
      tag1.Draw()

      tag2 = ROOT.TLatex(lab_x0+0.07, lab_y0, "Internal")
      tag2.SetNDC()
      tag2.SetTextFont(52)
      tag2.SetTextSize(0.035)
      tag2.Draw()

      tag3 = ROOT.TLatex(lab_x0+0.06, lab_y0-0.09, "#splitline{#mu#mu}{Resolved DY CR}")
#      tag3 = ROOT.TLatex(lab_x0+0.06, lab_y0-0.09, "#splitline{#font[12]{ll}}{Resolved DY CR}")
      tag3.SetNDC()
      tag3.SetTextFont(42)
      tag3.SetTextSize(0.046)
      tag3.Draw()
	
      plot.Modified() #Not sure if this does anything
     
      pad2.cd()


#      ratio = self.getRatio(newDataHist,allMC)
#      herr3= self.TOTerror(ratio, newDataHist);

      ratio = self.getRatio(allMC, newDataHist)
      herr3= self.TOTerror(ratio,allMC);

      toterree = ROOT.TGraphErrors(herr3)

      ratio.SetStats(0)
   
      ratio.GetYaxis().SetRangeUser(0.6,1.4)
      if("FourObjectInvariantMass" in name):
          ratio.GetYaxis().SetRangeUser(0.6, 1.4)
      elif("LeadLeptonpT" in name):
          ratio.GetYaxis().SetRangeUser(0,2)
      elif("SubleadLeptonpT" in name):
          ratio.GetYaxis().SetRangeUser(0.6, 1.4)
      elif("DileptonpT" in name):
          ratio.GetYaxis().SetRangeUser(0,2)
      elif("DileptonMass" in name):
          ratio.GetYaxis().SetRangeUser(0,2)
      elif("PtllOverMll" in name):
          ratio.GetYaxis().SetRangeUser(0,2)
      elif("LeadJetpT" in name):
          ratio.GetYaxis().SetRangeUser(0.6,1.4)
      elif("SubleadJetpT" in name):
          ratio.GetYaxis().SetRangeUser(0, 2)
      elif ("LeadJetEta" in name):
          ratio.GetYaxis().SetRangeUser(0.8, 1.2)
      elif ("SubleadJetEta" in name):
          ratio.GetYaxis().SetRangeUser(0.8, 1.2)
      elif ("LeadJetPhi" in name):
          ratio.GetYaxis().SetRangeUser(0.8, 1.2)
      elif ("SubleadJetPhi" in name):
          ratio.GetYaxis().SetRangeUser(0.8, 1.2)
      elif ("LeadLeptonEta" in name):
          ratio.GetYaxis().SetRangeUser(0.8, 1.2)
      elif ("SubleadLeptonEta" in name):
          ratio.GetYaxis().SetRangeUser(0.8, 1.2)
      elif ("LeadLeptonPhi" in name):
          ratio.GetYaxis().SetRangeUser(0.8, 1.2)
      elif ("SubleadLeptonPhi" in name):
          ratio.GetYaxis().SetRangeUser(0.8, 1.2)

      ratio.GetYaxis().SetNdivisions(504)
      ratio.GetYaxis().SetTitle("#frac{Sim.}{Data.}")
      ratio.GetYaxis().CenterTitle(True)
      ratio.GetYaxis().SetTitleSize(0.14)
      ratio.GetYaxis().SetTitleOffset(0.3)
      ratio.GetYaxis().SetLabelSize(0.11)

      ratio.GetXaxis().SetTitle(xtitle)
      ratio.GetXaxis().SetTitleSize(0.14)
      ratio.GetXaxis().SetTitleOffset(1.0)
      ratio.GetXaxis().SetLabelOffset(0.005)
      ratio.GetXaxis().SetLabelSize(0.11)

      ratio.SetLineStyle(1)
      ratio.SetLineWidth(2)
      ratio.SetLineColor(ROOT.kBlack)
      ratio.SetMarkerStyle(20)
      ratio.SetMarkerSize(0.5)

      line = ROOT.TLine(ratio.GetXaxis().GetXmin(), 1.0,ratio.GetXaxis().GetXmax(), 1.0)
      line.SetLineColor(ROOT.kBlack)
      line.SetLineStyle(1)
      line.Draw()

#      Save ratio plot to output root file      

#      outfile = ROOT.TFile("hists/New_PtllOverMll_NominalRatio.root","CREATE")
#      ratio.Write()
#      outfile.Close()
 
      ratio.Draw("PE")

      toterree.SetFillColor(ROOT.kGray+2)
#     toterree.SetLineColor(ROOT.kGray+2)
#     toterree.SetLineWidth(5)
      toterree.SetFillStyle(3244)
#      toterree.Draw("2 same")
      line.Draw("same")

      pad1.cd()
      leg4 = ROOT.TLegend(0.50,0.82,0.8,0.87)
      leg4.SetFillStyle(0)
      leg4.SetBorderSize(0)
      leg4.SetTextSize(0.035)
      leg4.SetTextFont(62)
      leg4.AddEntry(toterree,"MC stat. uncert.","fl")
      leg4.Draw()
#**************************************************************************************
# Create the images                                                                   *
#**************************************************************************************
      print "Calling TImage"
      img = ROOT.TImage.Create()
      img.FromPad(plot)
#     plot.Print(outDir+"/"+name.split("/")[0]+name.split("/")[1]+"_stack.png")
      plot.Print(outDir+"/"+name.split("/")[0]+"_stack.pdf")
#     plot.Print(outDir+"/"+name.split("/")[0]+name.split("/")[1]+"_stack.C")
