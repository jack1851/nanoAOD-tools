 #!/usr/bin/env python
import argparse
import os
import ROOT
import stackplot_tool_full_SR as stack
#****************************************************************************************************************
#  ARGMENTS FOR COMMAND LINE OPTONS                                                                             *
#****************************************************************************************************************
parser = argparse.ArgumentParser(description="Create stack plots for the mu+X skim")
parser.add_argument("--o", "--outputdir", dest="outDir", help="output directory", default=os.getcwd()+"/plots/")
parser.add_argument("--l", "--lumi", dest="lumi", help="luminosity", default=0)
parser.add_argument("--t", "--title", dest="label", help="Data label", default="Mu+X Data Skim")
arg = parser.parse_args()

outDir = arg.outDir
#Check for trailing slash on ouput dir and delete
if arg.outDir.split("/")[-1] == "": outDir = arg.outDir[:-1]
if not os.path.isdir(outDir):
     print "Output directory " + outDir + " does not exist!"
     quit()
#***************************************************************************************************************
#  CROSS SECTIONS IN PB                                                                                        *
#***************************************************************************************************************
DYJetsToLL_M50_HT_70to100_Xsec=208.977
DYJetsToLL_M50_HT_100to200_Xsec=181.30
DYJetsToLL_M50_HT_200to400_Xsec=50.4177
DYJetsToLL_M50_HT_400to600_Xsec=6.98394
DYJetsToLL_M50_HT_600to800_Xsec=1.68141
DYJetsToLL_M50_HT_800to1200_Xsec=0.775392
DYJetsToLL_M50_HT_1200to2500_Xsec=0.186222
DYJetsToLL_M50_HT_2500toinf_Xsec=0.00438495
#*****************************************************************************************************************
#    MAKE A LIST OF ALL THE MONTE CARLO FILES                                                                    *
#*****************************************************************************************************************
mcFiles = []
mcFiles.append(stack.mcFile(ROOT.TFile("reweighting_variables/dijet_pt/files/DYJetsToLL_M-50_HT-70to100.root","READ"), "Z+Jets (reweighted)", DYJetsToLL_M50_HT_70to100_Xsec,5))
mcFiles.append(stack.mcFile(ROOT.TFile("reweighting_variables/dijet_pt/files/DYJetsToLL_M-50_HT-100to200.root","READ"), "100 < HT < 200", DYJetsToLL_M50_HT_100to200_Xsec,5))
mcFiles.append(stack.mcFile(ROOT.TFile("reweighting_variables/dijet_pt/files/DYJetsToLL_M-50_HT-200to400.root","READ"), "200 < HT < 400", DYJetsToLL_M50_HT_200to400_Xsec,5))
mcFiles.append(stack.mcFile(ROOT.TFile("reweighting_variables/dijet_pt/files/DYJetsToLL_M-50_HT-400to600.root","READ"), "400 < HT < 600", DYJetsToLL_M50_HT_400to600_Xsec,5))
mcFiles.append(stack.mcFile(ROOT.TFile("reweighting_variables/dijet_pt/files/DYJetsToLL_M-50_HT-600to800.root","READ"), "600 < HT < 800", DYJetsToLL_M50_HT_600to800_Xsec,5))
mcFiles.append(stack.mcFile(ROOT.TFile("reweighting_variables/dijet_pt/files/DYJetsToLL_M-50_HT-800to1200.root","READ"), "800 < HT < 1200", DYJetsToLL_M50_HT_800to1200_Xsec,5))
mcFiles.append(stack.mcFile(ROOT.TFile("reweighting_variables/dijet_pt/files/DYJetsToLL_M-50_HT-1200to2500.root","READ"), "1200 < HT < 2500", DYJetsToLL_M50_HT_1200to2500_Xsec,5))
mcFiles.append(stack.mcFile(ROOT.TFile("reweighting_variables/dijet_pt/files/DYJetsToLL_M-50_HT-2500toinf.root","READ"), "2500 < HT", DYJetsToLL_M50_HT_2500toinf_Xsec,5))
#********************************************************************************************************************
#    MAKE A LIST OF ALL THE MONTE CARLO FILES                                                                       *
#********************************************************************************************************************
unweighted = "400mll/400mll_unweighted/l_l/"
pseudodata = "400mll/400mll_pseudodata/l_l/"
reweighted = "400mll/400mll_reweighted/l_l/"

info = stack.stackInfo(mcFiles, arg.lumi, unweighted, pseudodata, reweighted)
info.plotAll("Passing Events",outDir)
