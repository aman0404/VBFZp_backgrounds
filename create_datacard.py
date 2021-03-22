import ROOT
from ROOT import TFile, TTree, TCanvas, TGraph, TMultiGraph, TGraphErrors, TLegend
#import CMS_lumi, tdrstyle
#import subprocess # to execute shell command
ROOT.gROOT.SetBatch(ROOT.kTRUE)
import sys

print("Enter masspoint signal fake tt DY VV ST in order")
def print_sampleinfo():
    mass_value = sys.argv[1]
    file1 = open(sys.argv[2],"r+")
    file2 = open(sys.argv[3],"r+")
    file3 = open(sys.argv[4],"r+")
    file4 = open(sys.argv[5],"r+")
    file5 = open(sys.argv[6],"r+")
    file6 = open(sys.argv[7],"r+")

if (len(sys.argv) < 5):
       print("Please enter inputs in order")
       sys.exit()

for i in range(len(sys.argv)):
    print(sys.argv[i])

mass_value = sys.argv[1]
file1 = open(sys.argv[2],"r+")
file2 = open(sys.argv[3],"r+")
file3 = open(sys.argv[4],"r+")
file4 = open(sys.argv[5],"r+")
file5 = open(sys.argv[6],"r+")
file6 = open(sys.argv[7],"r+")

#signal
lines=file1.readlines()
result=[]
integral=[]
for x in lines:
    integral.append(x.split(' ')[1])
    result.append(x.split(' ')[0])
file1.close()

#bkg1
lines_bkg1=file2.readlines()
result_bkg1=[]
integral_bkg1=[]
for x_bkg1 in lines_bkg1:
    integral_bkg1.append(x_bkg1.split(' ')[1])
    result_bkg1.append(x_bkg1.split(' ')[0])
file2.close()

#bkg2
lines_bkg2=file3.readlines()
result_bkg2=[]
integral_bkg2=[]
for x_bkg2 in lines_bkg2:
    integral_bkg2.append(x_bkg2.split(' ')[1])
    result_bkg2.append(x_bkg2.split(' ')[0])
  #  print(result_bkg2)
file3.close()

#bkg3
lines_bkg3=file4.readlines()
result_bkg3=[]
integral_bkg3=[]
for x_bkg3 in lines_bkg3:
    integral_bkg3.append(x_bkg3.split(' ')[1])
    result_bkg3.append(x_bkg3.split(' ')[0])
file4.close()

#bkg4
lines_bkg4=file5.readlines()
result_bkg4=[]
integral_bkg4=[]
for x_bkg4 in lines_bkg4:
    integral_bkg4.append(x_bkg4.split(' ')[1])
    result_bkg4.append(x_bkg4.split(' ')[0])
file5.close()

#bkg5
lines_bkg5=file6.readlines()
result_bkg5=[]
integral_bkg5=[]
for x_bkg5 in lines_bkg5:
    integral_bkg5.append(x_bkg5.split(' ')[1])
    result_bkg5.append(x_bkg5.split(' ')[0])
file6.close()


N = len(result)
def createCard(result):
    datacard_lines1 = ["#========= VBF temp",
                   
                    "imax 1  number of channels",
                    "jmax 5  number of backgrounds",
                    "kmax * number of nuisance parameters (sources of systematic uncertainties)",

                    "# we have just one channel and will use some dummy data",
                    "bin vbf_etau",
                    "observation 0",

                    "bin            vbf_etau       vbf_etau       vbf_etau       vbf_etau       vbf_etau       vbf_etau      ",
                    "process        SIG            fakes          tt             DY             VV             ST            ",
                    "process        0              1              2              3              4              5             ",
                    ]
    datacard_sys = ["lumi    lnN    1.025          1.025          1.025          1.025          1.025          1.025         ",
                    "STMC00  lnN    1.05           -              -              -              -              -             ",
                    "STMC01  lnN    -              1.30           -              -              -              -             ", 
                    "STMC02  lnN    -              -              1.30           -              -              -             ",
                    "STMC03  lnN    -              -              -              -              -              -             ",
                    "STMC04  lnN    -              -              -              -              -              -             ",
                    "STMC05  lnN    -              -              -              -              -              -             ",
                    "STMC06  lnN    -              -              -              -              -              -             ",
                    "Trig00  lnN    1.03           1.03           1.03           -              -              -             ",
                    ]
    
    for i in range(N):
        datacard = open("VBF_etau_M"+str(mass_value)+"_bin"+result[i]+".txt",'w')
        input_signal = float(integral[i])
        input_bkg1 =  float(integral_bkg1[i])
        input_bkg2 =  float(integral_bkg2[i])
	input_bkg3 =  float(integral_bkg3[i])
	input_bkg4 =  float(integral_bkg4[i])
	input_bkg5 =  float(integral_bkg5[i])

        second = result[i]
        for line in datacard_lines1:
            datacard.write(line+"\n")
        #datacard.write("rate           {0}      {1}      {2}    {3}     {4}      {5} \n".format(input_signal, input_bkg1, input_bkg2, input_bkg3, input_bkg4, input_bkg5))
        datacard.write("rate           {:<14.10f} {:<14.10f} {:<14.10f} {:<14.10f} {:<14.10f} {:<14.10f} \n".format(input_signal, input_bkg1, input_bkg2, input_bkg3, input_bkg4, input_bkg5))
	datacard.write("\n")
        for line_sys in datacard_sys:
            datacard.write(line_sys+"\n")
   #     theta_B = ("%.2f" % (input_signal)).rstrip('0').rstrip('.')
   #     print("rate       {0}        {1}        {2}        {3} ".format(input_signal, input_bkg1, input_bkg2, input_signal))
        datacard.close()


def main():
	print_sampleinfo()
	createCard(result)
if __name__ == '__main__':
    main()






