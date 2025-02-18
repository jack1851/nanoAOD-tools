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
   def __init__(self, mc, lumi, pre):
      self.mcFiles = mc
      self.lumi = lumi
      self.pre = pre

   def plotAll(self, tag,outDir):
       #Histogram name, X-axis label, Log Scale, Title, Output Directory, Rebin
        self.stack("LeadJetpT","p_{T} of the leading jet (GeV)",True,tag,outDir, True)
        self.stack("DijetMass","m_{jj} (GeV)",True,tag,outDir, True)
#****************************************************************************************************
# Get the ratio of each event                                                                       *
#****************************************************************************************************
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
#***************************************************************************************************
# Get the total error                                                                              *
#***************************************************************************************************
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
   def calcScaleFactor(self,name,inputFile, pre):
       eff = inputFile.Get(pre+name).Integral()/inputFile.Get(self.pre+"EventWeight").Integral() #eff = eventCount/eventWeight 
       print "eventCount: ", inputFile.Get(pre+name).Integral()
       print "eventWeight: ", inputFile.Get(pre+"EventWeight").Integral()
       return eff

   def stack(self, name, xtitle, log, tag, outDir,rebin=False):
      stackplot = ROOT.THStack("stack","")

#*************************************************************
# Legend formatting: TLegend(x1, y1, x2, y2) *
#*************************************************************
      leg = ROOT.TLegend(0.50,0.7,0.8,0.75)
      leg.SetBorderSize(0)
      leg.SetTextSize(0.035)
      leg.SetTextFont(62)

#*************************************************************
# Create variable bin sizes                                  *
#*************************************************************
      if(rebin):

          if ("Q2In" in name):
              binBoundaries = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20]          
          elif ("Q2Z" in name):
#             binBoundaries = [0,0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.011, 0.012, 0.013, 0.014, 0.015, 0.016, 0.017, 0.018, 0.019, 0.020, 0.021, 0.022, 0.023, 0.024, 0.025, 0.026, 0.027, 0.028, 0.029,  0.03, 0.031, 0.032, 0.033, 0.034, 0.035, 0.036, 0.037, 0.038, 0.039, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
              binBoundaries = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.2, 2.4, 2.6, 2.8, 2.9, 3, 3.5, 4.0, 4.5, 5, 5.5, 6]
          elif ("Q2Diff" in name):
              binBoundaries = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20]
          if("DileptonpT" in name):
              binBoundaries = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
          elif("LeadJetpT" in name):
              binBoundaries = [0,40, 100, 200, 400, 600, 800, 1000, 1500, 2000]
          elif("SubleadJetpT" in name):
              binBoundaries = [0, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500]
          if("FourObjectInvariantMass" in name):
              binBoundaries = [800,1000,1200,1400,1600, 2000,2400,2800, 3200, 8000]
          binBoundariesArray = array.array('d', binBoundaries)

#*************************************************************
# Renormalize Histograms to 1 or the luminosity              *
#*************************************************************
      hists = []
      count = 0
      for mcFile in self.mcFiles:
	  print("\n%r") % (mcFile.infile)
	  eff = self.calcScaleFactor(name,mcFile.infile, self.pre)
          Nevents = mcFile.cx*1000*float(self.lumi)*eff
	  print("name: %r, eff: %r, X-sec: %r pb, lumi: %r, Nevents: %r") % (name, eff, mcFile.cx, float(self.lumi), Nevents)

	  hist=(mcFile.infile.Get(self.pre+name).Clone()) #Clones the current histogram into a variable called hist.

          if(hist.Integral()>0):
	      print "Integral before scaling: ", hist.Integral()
              #hist.Scale(1.0/hist.Integral())
              hist.Scale(Nevents/hist.Integral())
              print "Integral after scaling: ", hist.Integral()
          
          hist.SetFillColor(mcFile.color) #Fill with the color defined in allVariableStacks.py
          hist.SetLineWidth(0) # Outlines the different MC files
#         hist.SetDirectory(0) # Don't know what this does

          if(rebin):
              hist_Rebin = hist.Rebin(len(binBoundariesArray) - 1,"hnew",binBoundariesArray)

	      for i in range(1,hist_Rebin.GetNbinsX()+1):
	          binWidth = binBoundaries[i] - binBoundaries[i-1]
                  hist_Rebin.SetBinContent(i,hist_Rebin.GetBinContent(i))
                  hist_Rebin.SetBinError(i,hist_Rebin.GetBinError(i))

              hist_Rebin.SetDirectory(0) # Don't know what this does      
              hists.append(hist_Rebin)
          else:
              hists.append(hist)

	  if count < 1:
            leg.AddEntry(hist_Rebin, mcFile.label,"f")
	  count += 1

#************************************************************************************************************
# Go through all of the histograms, store the sum of squares of weights, and add the histogram to stackplot *                                        *
#************************************************************************************************************
      for hist in hists:
	 hist.Sumw2() #Create structure to store sum of squares of weights.
         stackplot.Add(hist)

#**************************************************************************************
# Create a new canvas with a predefined size form.
# By default ROOT creates a default style that can be accessed via the gStyle pointer.                                    *
#**************************************************************************************
      plot= ROOT.TCanvas("canvas_1","canvas_1",2) #TCanvas(const char *name, const char *title="", Int_t form=1)
      ROOT.gStyle.SetTextFont(43)
      ROOT.gStyle.SetPadTickY(1)
      ROOT.gStyle.SetPadTickX(1)

      pad1 = ROOT.TPad("pad1","pad1",0,0 ,1,1)
#     pad1 = ROOT.TPad("pad1","pad1",0,0.3,1,1) #Use if plotting with ratio
      pad2 = ROOT.TPad('pad2','pad2',0,0.0,1.0,0.3)
#     pad1.SetBottomMargin(0)
      pad2.SetTopMargin(0.)
      pad2.SetBottomMargin(0.35)

      pad1.SetFillStyle(4000)
      pad1.SetFrameFillStyle(1000)
      pad1.SetFrameFillColor(0)
      pad2.SetFillStyle(4000)
      pad2.SetFrameFillStyle(1000)
      pad2.SetFrameFillColor(0)
      pad1.Draw()
#     pad2.Draw()
      pad1.cd()

      stackplot.Draw("hist")
      print "stackplot.Integral(): ", stackplot.GetStack().Last().Integral()

#**************************************************************************************
# Format the y-axis depending on whether or not to log                                *
#**************************************************************************************
      print "Formatting the log axis"
      if(log):
         ROOT.gPad.SetLogy()
	 if("FourObjectInvariantMass" in name):
             stackplot.SetMinimum(3.4)
             stackplot.SetMaximum(7e4)
             stackplot.GetYaxis().SetTitle("Events / bin")
         elif("LeadJetpT" in name):
             stackplot.SetMinimum(3.4)
             stackplot.SetMaximum(2.5e5)
             stackplot.GetYaxis().SetTitle("Events / bin")
         elif("SubleadJetpT" in name):
             stackplot.SetMinimum(3.4)
             stackplot.SetMaximum(2.5e5)
             stackplot.GetYaxis().SetTitle("Events / 20 GeV")
         elif("DileptonpT" in name):
             stackplot.SetMinimum(40)
             stackplot.SetMaximum(2.5e6)
             stackplot.GetYaxis().SetTitle("Events / 50 GeV")
         elif("Q2In" in name):
             stackplot.SetMinimum(0.425)
             stackplot.SetMaximum(2.5e6)
             stackplot.GetYaxis().SetTitle("Events / 0.5 TeV^{2}")
         elif("Q2Z" in name):
             stackplot.SetMinimum(0.425)
             stackplot.SetMaximum(2.5e6)
             stackplot.GetYaxis().SetTitle("Events / bin")
         elif("Q2Diff" in name):
             stackplot.SetMinimum(0.425)
             stackplot.SetMaximum(2.5e6)
             stackplot.GetYaxis().SetTitle("Events / 0.5 TeV^{2}")
      if not log:
         stackplot.SetMinimum(0) 
      
#     stackplot.SetMaximum(stackplot.GetMaximum()*6)

#**************************************************************************************
# Format the x-axis and the y axis                                                                  *
#**************************************************************************************
      stackplot.GetXaxis().SetTitleOffset(1.15)
      stackplot.GetXaxis().SetTitle(xtitle)
#     stackplot.GetXaxis().SetRangeUser(800,8000)
#     stackplot.GetXaxis().SetTitleSize(20)
      stackplot.GetXaxis().SetTickSize(0.02)
#     stackplot.Draw("hist")

      stackplot.GetYaxis().SetTitleSize(20)
      stackplot.GetYaxis().SetTitleFont(43)
#     stackplot.GetYaxis().SetLabelFont(43)
#     stackplot.GetYaxis().SetLabelSize(15)
      stackplot.GetYaxis().SetTitleOffset(1.2)

#**************************************************************************************
# Draw the legend                                                                     *
#**************************************************************************************
      leg.Draw()

#**************************************************************************************
# Create and draw all of the labels                                                   *
#**************************************************************************************      
      label = ROOT.TLatex(0.65,0.905,"%.2f fb^{-1} (13 TeV)" % float(self.lumi))
      label.SetNDC()
      label.SetTextFont(42)
      label.SetTextSize(0.033)
      label.Draw()

      lab_x0 = 0.10
      lab_y0 = 0.905

      tag1 = ROOT.TLatex(lab_x0,lab_y0,"CMS")
      tag1.SetNDC()
      tag1.SetTextFont(62)
      tag1.SetTextSize(0.04)
      tag1.Draw()

      tag2 = ROOT.TLatex(lab_x0+0.08, lab_y0, "Internal")
      tag2.SetNDC()
      tag2.SetTextFont(52)
      tag2.SetTextSize(0.03)
      tag2.Draw()
	
      if "mu_mu" in name:
          flavor = "#mu#mu"
      elif "e_e" in name:
          flavor = "ee"
      elif "l_l" in name:
          flavor = "ll"
      else:
          flavor=""

      tag3 = ROOT.TLatex(lab_x0+0.05, lab_y0-0.05, flavor)
      tag3.SetNDC()
      tag3.SetTextFont(42)
      tag3.SetTextSize(0.035)
      tag3.Draw()

      tag4 = ROOT.TLatex(lab_x0+0.05, lab_y0-0.09, "Resolved DY CR")
      tag4.SetNDC()
      tag4.SetTextFont(42)
      tag4.SetTextSize(0.035)
      tag4.Draw()

      plot.Modified() #Not sure if this does anything

#**************************************************************************************
# Create the images                                                                   *
#**************************************************************************************
      print "Calling TImage"
      img = ROOT.TImage.Create()
      img.FromPad(plot)
#     plot.Print(outDir+"/"+name.split("/")[0]+name.split("/")[1]+"_stack.png")
      plot.Print(outDir+"/"+name.split("/")[2]+"_stack.pdf")
#     plot.Print(outDir+"/"+name.split("/")[0]+name.split("/")[1]+"_stack.C")
