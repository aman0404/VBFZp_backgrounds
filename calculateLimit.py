import ROOT
from ROOT import TFile, TTree, TCanvas, TGraph, TMultiGraph, TGraphErrors, TLegend
import CMS_lumi, tdrstyle
import subprocess # to execute shell command
ROOT.gROOT.SetBatch(ROOT.kTRUE)

points = [250, 500, 750, 1000, 1250, 1500,1750, 2000, 2250, 2500]
def executeCards(points):
    mass = len(points)
    for j in range(mass):
        file_name = "VBF_combined_M"+str(points[j])+".txt" 
        combine_command = "combine -M AsymptoticLimits -m %s %s" % (points[j], file_name)
        print(">>> " + combine_command)
        p = subprocess.Popen(combine_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print line.rstrip("\n")
            print(">>>   higgsCombine_M"+str(points[j])+"_AsymptoticLimits.root created")
            retval = p.wait()

#get limits from root file


def getLimits(file_name):
	file = TFile(file_name)
    	tree = file.Get("limit")
 
    	limits = [ ]
    	for quantile in tree:
            limits.append(tree.limit)
            print ">>>   %.2f" % limits[-1]
 
    	return limits[:6]

#plot limits

def plotUpperLimits(file_name):
    # see CMS plot guidelines: https://ghm.web.cern.ch/ghm/plots/
 
    N = len(points)
    yellow = TGraph(2*N)    # yellow band
    green = TGraph(2*N)     # green band
    median = TGraph(N)      # median line
 
    up2s = [ ]
    for i in range(N):
        file_name = "higgsCombineTest.AsymptoticLimits.mH"+str(points[i])+".root" 
        limit = getLimits(file_name)
        up2s.append(limit[4])
        yellow.SetPoint(    i,    points[i], limit[4] ) # + 2 sigma
        green.SetPoint(     i,    points[i], limit[3] ) # + 1 sigma
        median.SetPoint(    i,    points[i], limit[2] ) # median
        green.SetPoint(  2*N-1-i, points[i], limit[1] ) # - 1 sigma
        yellow.SetPoint( 2*N-1-i, points[i], limit[0] ) # - 2 sigma
 
    W = 800
    H  = 600
    T = 0.08*H
    B = 0.12*H
    L = 0.12*W
    R = 0.04*W
    c = TCanvas("c","c",100,100,W,H)
    c.SetFillColor(0)
    c.SetBorderMode(0)
    c.SetFrameFillStyle(0)
    c.SetFrameBorderMode(0)
    c.SetLeftMargin( L/W )
    c.SetRightMargin( R/W )
    c.SetTopMargin( T/H )
    c.SetBottomMargin( B/H )
    c.SetTickx(0)
    c.SetTicky(0)
    c.SetLogy()
    c.SetGrid()
    c.cd()
    frame = c.DrawFrame(2000.4,0.001, 2400.1, 10)
    
    frame.GetYaxis().CenterTitle()
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetTitleOffset(0.9)
    frame.GetXaxis().SetNdivisions(508)
    frame.GetYaxis().CenterTitle(True)
    frame.GetYaxis().SetTitle("#sigma #times BR")
#    frame.GetYaxis().SetTitle("95% upper limit on #sigma #times BR / (#sigma #times BR)_{SM}")
    frame.GetXaxis().SetTitle("M_{Z'} [GeV]")
    frame.SetMinimum(0.001)
#    frame.SetMaximum(max(up2s)*1.05)
    frame.SetMaximum(max(up2s)*6.05)
    frame.GetXaxis().SetLimits(min(points),max(points))
    yellow.SetFillColor(ROOT.kOrange)
    yellow.SetLineColor(ROOT.kOrange)
    yellow.SetFillStyle(1001)
    yellow.Draw('F')
 
    green.SetFillColor(ROOT.kGreen+1)
    green.SetLineColor(ROOT.kGreen+1)
    green.SetFillStyle(1001)
    green.Draw('Fsame')
 
    median.SetLineColor(1)
    median.SetLineWidth(2)
    median.SetLineStyle(2)
    median.Draw('Lsame')
 
    CMS_lumi.CMS_lumi(c,14,11)
    ROOT.gPad.SetTicks(1,1)
    frame.Draw('sameaxis')
 
    x1 = 0.15
    x2 = x1 + 0.24
    y2 = 0.76
    y1 = 0.60
    legend = TLegend(x1,y1,x2,y2)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.041)
    legend.SetTextFont(42)
    legend.AddEntry(median, "Asymptotic CL_{s} expected",'L')
    legend.AddEntry(green, "#pm 1 std. deviation",'f')
#    legend.AddEntry(green, "Asymptotic CL_{s} #pm 1 std. deviation",'f')
    legend.AddEntry(yellow,"#pm 2 std. deviation",'f')
#    legend.AddEntry(green, "Asymptotic CL_{s} #pm 2 std. deviation",'f')
    legend.Draw()
 
    print " "
    c.SaveAs("UpperLimit.png")
    c.Close()

def main():
	executeCards(points)
	plotUpperLimits(points)

if __name__ == '__main__':
    main()
