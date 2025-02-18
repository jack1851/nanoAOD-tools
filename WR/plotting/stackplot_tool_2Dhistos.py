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
   def __init__(self, mc, lumi, unweight):
      self.mcFiles = mc
      self.lumi = lumi
      self.unweight = unweight

   def plotAll(self, tag,outDir):
       #Histogram name, X-axis label, Log Scale, Title, Output Directory, Rebin
#     self.stack("FourObjectInvariantMass","m_{lljj} (GeV)",True,tag,outDir, True)
#      self.stack("leadJetAndZPt","Lead jet p_{T} (GeV)",False,tag,outDir, True)
#      self.stack("leadJetAndPtllOverMll","Lead jet p_{T} (GeV)",False,tag,outDir, False)
      self.stack("leadJetAndmjj","Lead jet p_{T} (GeV)",False,tag,outDir, True)

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
      leg = ROOT.TLegend(0.50,0.72,0.85,0.77)
      leg.SetBorderSize(0)
      leg.SetTextSize(0.035)
      leg.SetTextFont(62)
      leg2 = ROOT.TLegend(0.50,0.77,0.85,0.82)
      leg2.SetBorderSize(0)
      leg2.SetTextSize(0.035)
      leg2.SetTextFont(62)

#*************************************************************
# Create variable bin sizes                                  *
#*************************************************************
      if(rebin):
          if("FourObjectInvariantMass" in name):
              binBoundaries = [800,1000,1200,1400,1600, 2000,2400,2800, 3200, 8000]
          if("leadJetAndZPt" in name):
              binBoundaries = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
          elif ("LeadJetpT" or "leadJetAndmjj" in name):
              binBoundaries = [40, 100, 200, 400, 600, 800, 1000, 1500, 2000]
          elif ("SubleadJetpT" in name):
              binBoundaries = [40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500]
          elif ("DileptonpT" in name):
              binBoundaries = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
          elif ("DileptonMass" in name):
              binBoundaries = [60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150]
          elif("PtllOverMll" in name):
              binBoundaries = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]
          elif ("DijetpT" in name):
              binBoundaries = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400]
#          elif ("DijetMass" in name):
#              binBoundaries = [0, 100, 200, 400, 600,800,1000,1200,1400,1600, 2000, 2500, 3000, 3500, 5000]
          elif ("PtjjOverMjj" in name):
              binBoundaries = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 10]
          elif ("LeadJetZMass" in name):
              binBoundaries = [400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2300, 2600, 3000, 3500, 4000]
          elif ("SubleadJetZMass" in name):
              binBoundaries = [400, 600, 800, 1000, 1200, 1500, 2500, 4000]
          elif ("LeadLeptonpT" in name):
              binBoundaries = [0, 50, 150, 250, 350, 450, 550, 650, 1000]
          elif ("SubleadLeptonpT" in name):
              binBoundaries = [50, 100, 150, 200, 250, 300, 350, 400, 500, 1000]
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
          elif ("Q2In" in name):
              binBoundaries = [0, 2, 4, 6, 8, 10, 12, 14, 16, 20, 32,60]
          elif ("Q2Z" in name):
              binBoundaries = [0,0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.011, 0.012, 0.013, 0.014, 0.015, 0.016, 0.017, 0.018, 0.019, 0.020, 0.021, 0.022, 0.023, 0.024, 0.025, 0.026]
          elif ("Q2Diff" in name):
              binBoundaries = [0, 2, 4, 6, 8, 10, 12, 14, 16, 20, 32, 60]

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
	  eff = self.calcScaleFactor(name,mcFile.infile, self.unweight)
          Nevents = mcFile.cx*1000*float(self.lumi)*eff
	  print("name: %r, eff: %r, X-sec: %r pb, lumi: %r, Nevents: %r") % (name, eff, mcFile.cx, float(self.lumi), Nevents)

	  hist=(mcFile.infile.Get(self.unweight+name).Clone()) #Clones the current histogram into a variable called hist.
          print "HIST: ", hist
          if(hist.Integral()>0):
	      print "Integral before scaling: ", hist.Integral()
#              hist.Scale(1.0/hist.Integral())
              hist.Scale(Nevents/hist.Integral())
              print "Integral after scaling to Nevents: ", hist.Integral()
          
#          hist.SetFillColor(mcFile.color) #Fill with the color defined in allVariableStacks.py
          hist.SetLineWidth(0) # Outlines the different MC files

          if(rebin):
#              hist.Rebin2D(4, 4)
              hist.Rebin(len(binBoundariesArray) - 1,"hnew",binBoundariesArray)
          hist.SetDirectory(0)
          hists.append(hist)
#              hist_Rebin = hist.Rebin2D(len(binBoundariesArray) - 1,"hnew",binBoundariesArray)

#	      for i in range(1,hist_Rebin.GetNbinsX()+1):
#	          binWidth = binBoundaries[i] - binBoundaries[i-1]
#                  hist_Rebin.SetBinContent(i,hist_Rebin.GetBinContent(i))
#                  hist_Rebin.SetBinError(i,hist_Rebin.GetBinError(i))

#              print "Rebinned integral:", hist_Rebin.Integral()
#              hist_Rebin.SetDirectory(0) # Don't know what this does      
#              hists.append(hist_Rebin)
#          else#:
#              hists.append(hist)

#	  if count < 1:
#            leg.AddEntry(hist_Rebin, mcFile.label,"f")
#	  count += 1
       
#*****************************************************************************
# Error tracking                                                             *
#***************************************************************************** 
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

      pad1 = ROOT.TPad("pad1","pad1",0,0,1,1)
#      pad2 = ROOT.TPad('pad2','pad2',0,0.0,1.0,0.22)
#      pad1.SetBottomMargin(0.00)
#      pad2.SetTopMargin(0.03)
#      pad2.SetBottomMargin(0.35)

      pad1.SetFillStyle(4000)
      pad1.SetFrameFillStyle(1000)
      pad1.SetFrameFillColor(0)
#      pad2.SetFillStyle(4000)
#      pad2.SetFrameFillStyle(1000)
#      pad2.SetFrameFillColor(0)
      pad1.Draw()
#      pad2.Draw()
      pad1.cd()

#     stackplot.Draw("hist")
#      stackplot.Draw("colz")
#**************************************************************************************
# Format the y-axis depending on whether or not to log                                *
#**************************************************************************************
      print "Formatting the log axis"
      if(log):
	 pad1.SetLogy()
         ROOT.gPad.SetLogy()
      if not log:
         stackplot.SetMinimum(0) 
      

      allMCunweighted = stackplot.GetStack().Last().Clone()
      allMCunweighted.Draw("colz")
#**************************************************************************************
# Draw the legend                                                                     *
#**************************************************************************************
#      leg.Draw()
#      leg2.Draw()
#**************************************************************************************
# Create and draw all of the labels                                                   *
#**************************************************************************************      
      label = ROOT.TLatex(0.66,0.905,"%.2f fb^{-1} (13 TeV)" % float(self.lumi))
      label.SetNDC()
      label.SetTextFont(42)
      label.SetTextSize(0.03)
      label.Draw()

#**************************************************************************************
# Format the x-axis and the y axis                                                                  *
#**************************************************************************************
      allMCunweighted.GetXaxis().SetTitleSize(15)
      allMCunweighted.GetXaxis().SetTitleFont(43)
      allMCunweighted.GetXaxis().SetLabelFont(43)
      allMCunweighted.GetXaxis().SetLabelSize(13)
      allMCunweighted.GetXaxis().SetTitleOffset(1.2)
      allMCunweighted.GetXaxis().SetTitle("p_{T} of the leading jet (GeV)")
#      allMCunweighted.GetXaxis().SetRangeUser(0,1000)

      allMCunweighted.GetYaxis().SetTitleSize(15)
      allMCunweighted.GetYaxis().SetTitleFont(43)
      allMCunweighted.GetYaxis().SetLabelFont(43)
      allMCunweighted.GetYaxis().SetLabelSize(13)
      allMCunweighted.GetYaxis().SetTitleOffset(1.5)
      allMCunweighted.GetYaxis().SetTitle("Dijet Mass (GeV)")

#      allMCunweighted.SetStats(0)

      lab_x0 = 0.10
      lab_y0 = 0.905

      tag1 = ROOT.TLatex(lab_x0,lab_y0,"CMS")
      tag1.SetNDC()
      tag1.SetTextFont(62)
      tag1.SetTextSize(0.045)
      tag1.Draw()

      tag2 = ROOT.TLatex(lab_x0+0.1, lab_y0, "Internal")
      tag2.SetNDC()
      tag2.SetTextFont(52)
      tag2.SetTextSize(0.035)
      tag2.Draw()

      plot.Modified() #Not sure if this does anything
     
#     pad2.cd()

      pad1.cd()
#**************************************************************************************
# Create the images                                                                   *
#**************************************************************************************
      print "Calling TImage"
      img = ROOT.TImage.Create()
      img.FromPad(plot)
#     plot.Print(outDir+"/"+name.split("/")[0]+name.split("/")[1]+"_stack.png")
      plot.Print(outDir+"/"+name.split("/")[0]+"_250mll.pdf")
#     plot.Print(outDir+"/"+name.split("/")[0]+name.split("/")[1]+"_stack.C")
