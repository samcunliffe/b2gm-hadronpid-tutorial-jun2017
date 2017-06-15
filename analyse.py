#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Make PID validation plots for D* -> D0 pi; D0 -> K pi """
__authors__ = ['Jake Bennett', 'Sam Cunliffe']

# Tested in release-00-08-00 June 2017

from ROOT import TFile, TTree, TCanvas, TEfficiency, TH1F, TLegend
from ROOT import kBlue, kRed, kMagenta, kGreen
from ROOT import gStyle
gStyle.SetOptStat(0) # turn off the stats box

# open the file and get the tree
fi = TFile("candidates.root")
tr = fi.Get("dsttree")
print("Got tree with: %i entries" % tr.GetEntries())

# the name of the pid variable to test
kaon_id_variable  = "PIDk"
pion_id_variable = "PIDpi"
benchmark_cut = "0.5"

# plot the efficiency as a function of momentum using the D* self-tagging
selection = "abs(DST_D0_M-1.86484)<0.012&&abs(DST_M-DST_D0_M-0.14543)<0.00075"

tr.Project("pkall(100, 0.0, 5.0)", "DST_D0_K_P",  selection)
tr.Project("pkacc(100, 0.0, 5.0)", "DST_D0_K_P", 
           "DST_D0_K_"+kaon_id_variable+">"+benchmark_cut+"&&"+selection)
tr.Project("pkfake(100, 0.0, 5.0)", "DST_D0_K_P",  
           "DST_D0_K_"+pion_id_variable+">"+benchmark_cut+"&&"+selection)
tr.Project("ppiall(100, 0.0, 5.0)", "DST_D0_pi_P", selection)
tr.Project("ppiacc(100, 0.0, 5.0)", "DST_D0_pi_P", 
           "DST_D0_pi_"+pion_id_variable+">"+benchmark_cut+"&&"+selection)
tr.Project("ppifake(100, 0.0, 5.0)", "DST_D0_pi_P", 
           "DST_D0_pi_"+kaon_id_variable+">"+benchmark_cut+"&&"+selection)

pkall   = fi.Get("pkall")
pkacc   = fi.Get("pkacc")
pkfake  = fi.Get("pkfake")
ppiall  = fi.Get("ppiall")
ppiacc  = fi.Get("ppiacc")
ppifake = fi.Get("ppifake")

ek  = TEfficiency(pkacc,   pkall)
fk  = TEfficiency(ppifake, ppiall)
epi = TEfficiency(ppiacc,  ppiall)
fpi = TEfficiency(pkfake,  pkall)
 
# plot the efficiency as a function of momentum using MC truth information
truekaon = "abs(DST_D0_K_mcPDG)==321"
truepion = "abs(DST_D0_pi_mcPDG)==211"

tr.Project("tpkall(100, 0.0, 5.0)", "DST_D0_K_P", truekaon+"&&"+selection)
tr.Project("tpkacc(100, 0.0, 5.0)", "DST_D0_K_P",
           "DST_D0_K_"+kaon_id_variable+">"+benchmark_cut+"&&"+truekaon+"&&"+selection)
tr.Project("tpkfake(100, 0.0, 5.0)", "DST_D0_K_P",
           "DST_D0_K_"+pion_id_variable+">"+benchmark_cut+"&&"+truekaon+"&&"+selection)
tr.Project("tppiall(100, 0.0, 5.0)", "DST_D0_pi_P",truepion+"&&"+selection)
tr.Project("tppiacc(100, 0.0, 5.0)", "DST_D0_pi_P",
           "DST_D0_pi_"+pion_id_variable+">"+benchmark_cut+"&&"+truepion+"&&"+selection)
tr.Project("tppifake(100, 0.0, 5.0)", "DST_D0_pi_P",
           "DST_D0_pi_"+kaon_id_variable+">"+benchmark_cut+"&&"+truepion+"&&"+selection)

tpkall   = fi.Get("tpkall")
tpkacc   = fi.Get("tpkacc")
tpkfake  = fi.Get("tpkfake")
tppiall  = fi.Get("tppiall")
tppiacc  = fi.Get("tppiacc")
tppifake = fi.Get("tppifake")

tek  = TEfficiency(tpkacc,   tpkall)
tfk  = TEfficiency(tppifake, tppiall)
tepi = TEfficiency(tppiacc,  tppiall)
tfpi = TEfficiency(tpkfake,  tpkall)

tekh  = tpkacc.Clone("tekh");   tekh.Divide(tpkall);
tfkh  = tppifake.Clone("tfkh"); tfkh.Divide(tppiall);
tepih = tppiacc.Clone("tepih"); tepih.Divide(tppiall);
tfpih = tpkfake.Clone("tfpih"); tfpih.Divide(tpkall);

# a dummy histogram to draw into
base = TH1F("base","",100,0,5)
base.SetTitle(";p  [GeV/c^{2}]; Efficiency")
base.SetMaximum(1.0)
base.SetMinimum(0.0)

# legends
legend1 = TLegend(0.3,0.5,0.5,0.6)
legend1.AddEntry(ek,"K (MC)","pl")
legend1.AddEntry(epi,"#pi (MC)","pl")
legend2 = TLegend(0.5,0.5,0.7,0.6)
legend2.AddEntry(tekh,"K (truth)","l")
legend2.AddEntry(tepih,"#pi (truth)","l")

# draw all of the plots
canvas = TCanvas("pid","",1200,600)
canvas.Divide(2,1);

canvas.cd(1)
base.Draw()
ek.SetMarkerColor(kBlue)
ek.SetLineColor(kBlue)
ek.Draw("P,same")
tekh.SetLineColor(kMagenta)
tekh.Draw("hist,same")
fk.SetMarkerColor(kRed)
fk.SetLineColor(kRed)
fk.Draw("P,same")
tfkh.SetLineColor(kGreen)
tfkh.Draw("hist,same")
legend1.Draw("same")
legend2.Draw("same")

canvas.cd(2)
base.Draw()
epi.SetMarkerColor(kRed)
epi.SetLineColor(kRed)
epi.Draw("P,same")
tepih.SetLineColor(kGreen)
tepih.Draw("hist,same")
fpi.SetMarkerColor(kBlue)
fpi.SetLineColor(kBlue)
fpi.Draw("P,same")
tfpih.SetLineColor(kMagenta)
tfpih.Draw("hist,same")

canvas.SaveAs("pid-performance.pdf")
fi.Close()
