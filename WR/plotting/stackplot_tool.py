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
   def __init__(self, mc, lumi):
      self.mcFiles=mc
      self.lumi=lumi
   def plotAll(self,basedir,tag,outDir):
      #Histogram name, X-axis label, Log Scale, Title, Output Directory, Rebin
      self.stack(basedir+"/FourObjectInvariantMass","m_{lljj} (GeV)",True,tag,outDir, True)
#      self.stack(basedir+"/leadLepPtHisto","Lead lepton p_{T} (GeV)",True,tag,outDir, True)
#      self.stack(basedir+"/subleadLepPtHisto","Sublead lepton p_{T} (GeV)",True,tag,outDir, True)
#      self.stack(basedir+"/leadJetPtHisto","Lead jet p_{T} (GeV)",True,tag,outDir, True)
#      self.stack(basedir+"/subleadJetPtHisto","Sublead jet p_{T} (GeV)",True,tag,outDir, True)
#      self.stack(basedir+"/diJetMass","Dijet Mass m_{jj} (GeV)",True,tag,outDir, True)
#      self.stack(basedir+"/diLepPtHisto","Dilepton  p_{T} (GeV)",True,tag,outDir, True)
#      self.stack(basedir+"/diLepMassHisto","Dilepton Mass m_{ll} (GeV)",True,tag,outDir, True)
#      self.stack(basedir+"/ptllOverMllHisto","p_{T}_{ll}/m_{ll}",True,tag,outDir, True)
#      self.stack(basedir+"/leadJetZMass","m_{jz} (GeV)",True,tag,outDir, True)
#      self.stack(basedir+"/subleadJetZMass","m_{jz} (GeV)",True,tag,outDir, True)
  
#*************************************************************
# What does this do?                                         *
#*************************************************************
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
#*************************************************************
# What does this do?                                         *
#*************************************************************
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
   # Use # of muons passing tag for total weight because I know that there was no over/underflow
   def calcScaleFactor(self,name,inputFile):
       print "Name is ", name
       eff = inputFile.Get(name).Integral()/inputFile.Get("150mll400/EventWeight").Integral() #eff = eventCount/eventWeight 
       print "eventCount: ", inputFile.Get(name).Integral()
       print "eventWeight: ", inputFile.Get("150mll400/EventWeight").Integral()
       return eff
#*************************************************************
# Start the stack method                                         *
#*************************************************************
   def stack(self, name, xtitle, log, tag, outDir,rebin=False):
      stackplot = ROOT.THStack("stack","")
#*************************************************************
# Legend formatting: TLegend(x1, y1, x2, y2) *
#*************************************************************
      leg = ROOT.TLegend(0.55,0.6,0.8,0.65)
      leg.SetBorderSize(0)
      leg.SetTextSize(0.035)
      leg.SetTextFont(42)
#*************************************************************
# Create variable bin sizes                                  *
#*************************************************************
      if("FourObjectInvariantMass" in name):
        binBoundaries = [800,1000,1200,1400,1600, 2000,2400,2800, 3200, 8000]
#      elif ("leadLepPtHisto" in name):
#        binBoundaries = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 250, 300, 400, 500, 1000]
#      elif ("subleadLepPtHisto" in name):
#        binBoundaries = [0, 20,30,40,50, 60,70, 80,90, 100,120,140,160,180,200, 400, 1000]
#      elif ("leadJetPtHisto" in name):
#        binBoundaries = [30,40,50,60,70,80,100,120,140,160,180,200,250,300,400,600, 800,1000]
#      elif ("subleadJetPtHisto" in name):
#        binBoundaries = [30,40,50,60,70,80,100,120,140,160,180,200,250,300, 400,600,800, 1000]
#      elif ("diJetMass" in name):
#        binBoundaries = [0, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 450, 500, 550, 600, 700, 800, 900, 1000, 1250,1500, 2000, 3000]
#      elif ("diLepPtHisto" in name):
#        binBoundaries = [0, 25, 50, 100, 150, 200, 250, 400,600,2000]
#      elif ("ptllOverMllHisto" in name):
#        binBoundaries = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10]
#      elif ("leadJetZMass" in name):
#        binBoundaries = [0, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 450, 500, 550, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000]
#      elif ("subleadJetZMass" in name):
#        binBoundaries = [0, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 450, 500, 550, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000]
      binBoundariesArray = array.array('d', binBoundaries)
#*************************************************************
# Renormalize Histograms to 1 or the luminosity              *
#*************************************************************
      hists = []
      count = 0
      for mcFile in self.mcFiles:
 	  print "mcFile: ", mcFile.label
	  eff = self.calcScaleFactor(name,mcFile.infile)
 	  print "eff: ", eff
          print "cross section: ", mcFile.cx, "pb"
          print "lumi: ", float(self.lumi), "fb^-1"
          Nevents = mcFile.cx*1000*float(self.lumi)*eff
          print "Nevents: = X-sec*1000*eff*lumi =  ", Nevents

	  hist=(mcFile.infile.Get(name).Clone())

          if(hist.Integral()>0):
	      print "hist.Integral before scaling: ", hist.Integral()
             #hist.Scale(1.0/hist.Integral())
              hist.Scale(Nevents/hist.Integral())
              print "hist.Integral after scaling: ", hist.Integral()
          
          hist.SetFillColor(mcFile.color)
          hist.SetLineWidth(0) # Outlines the different MC files
          hist.SetDirectory(0)

          if(rebin):
#            hist.Rebin(40)
             hist_Rebin = hist.Rebin(len(binBoundariesArray) - 1,"hnew",binBoundariesArray)

	  for i in range(1,hist_Rebin.GetNbinsX()+1):
	      binWidth = binBoundaries[i] - binBoundaries[i-1]
              hist_Rebin.SetBinContent(i,hist_Rebin.GetBinContent(i))
              hist_Rebin.SetBinError(i,hist_Rebin.GetBinError(i))             
   
#         hists.append(hist)
          hists.append(hist_Rebin)

	  if count < 1:
            leg.AddEntry(hist, mcFile.label,"f")

	  count += 1
#************************************************************************************************************
# Go through all of the histograms, store the sum of squares of weights, and add the histogram to stackplot *                                        *
#************************************************************************************************************
      for hist in hists:
	 hist.Sumw2() #Create structure to store sum of squares of weights.
         stackplot.Add(hist)
#**************************************************************************************
# Create the pad to draw the histograms on                                            *
#**************************************************************************************
      plot= ROOT.TCanvas("stackplot","stackplot",2)
      ROOT.gStyle.SetTextFont(43)
      pad1 = ROOT.TPad("pad1","pad1",0,0,1,1)
#     pad1.SetBottomMargin(0)
      pad1.SetFillStyle(4000)
      pad1.SetFrameFillStyle(1000)
      pad1.SetFrameFillColor(0)
      pad1.Draw()
      pad1.cd()
#**************************************************************************************
# I think this returns the total integral                                             *
#**************************************************************************************
      stackplot.Draw("hist")
      print "stackplot.Integral(): ", stackplot.GetStack().Last().Integral()
#**************************************************************************************
# Format the y-axis depending on whether or not to log                                *
#**************************************************************************************
      if(log):
         pad1.SetLogy()
         ROOT.gPad.SetLogy()
      maximum=stackplot.GetMaximum()
      minimum=min(stackplot.GetMinimum(),0)
      if log:
	 minimum=max(stackplot.GetMinimum(),100)
         stackplot.SetMinimum(minimum*0.002825) #Use if y-axis minimum is 10^{-1}
#        stackplot.SetMinimum(minimum*0.01525) #Use if y-axis minimum is 1

      if not log:
         minimum=0
         stackplot.SetMinimum(minimum) 
      
      if not log:
         stackplot.SetMaximum(maximum*1.2)
      else:
         stackplot.SetMaximum(maximum*6)
      
#**************************************************************************************
# Format the x-axis                                                                   *
#**************************************************************************************
      stackplot.GetXaxis().SetTitleOffset(1.15)
      stackplot.GetXaxis().SetTitle(xtitle)
      stackplot.GetXaxis().SetRangeUser(800,8000)
#     stackplot.GetXaxis().SetTitleSize(20)
      stackplot.GetXaxis().SetTickSize(0.02)
      stackplot.Draw("hist")
#**************************************************************************************
# Format the y-axis                                                                   *
#**************************************************************************************
      stackplot.GetYaxis().SetTitle("Events / bin")
      stackplot.GetYaxis().SetTitleSize(20)
      stackplot.GetYaxis().SetTitleFont(43)
      stackplot.GetYaxis().SetLabelFont(43)
      stackplot.GetYaxis().SetLabelSize(15)
      stackplot.GetYaxis().SetTitleOffset(1.15)
#**************************************************************************************
# Draw the legend                                                                     *
#**************************************************************************************
      leg.Draw()
#**************************************************************************************
# Draw the "59.74" luminosity and 13 TeV labels                                       *
#**************************************************************************************      
      label = ROOT.TLatex(0.65,0.905,"%.2f fb^{-1} (13 TeV)" % float(self.lumi))
      label.SetNDC()
      label.SetTextFont(42)
      label.SetTextSize(0.033)
      label.Draw()
#**************************************************************************************
# Create the "CMS" and "Internal" logos                                               *
#**************************************************************************************
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

      plot.Modified() #Not sure if this does anything
#**************************************************************************************
# Create the images                                                                   *
#**************************************************************************************
      img = ROOT.TImage.Create()
      img.FromPad(plot)
#     plot.Print(outDir+"/"+name.split("/")[0]+name.split("/")[1]+"_stack.png")
      plot.Print(outDir+"/"+name.split("/")[0]+name.split("/")[1]+"_stack.pdf")
#     plot.Print(outDir+"/"+name.split("/")[0]+name.split("/")[1]+"_stack.C")
