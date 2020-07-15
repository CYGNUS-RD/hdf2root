# usage: python3 his2root.py run03642.HIS
import os,sys
import h5py
import numpy as np 
import ROOT
from root_numpy import array2hist

from readerHIS import openHIS

def main():
    if len(sys.argv) < 2:
        print('syntax: ' + sys.argv[0] + ' <his file>')
        sys.exit(1)

    his_file = sys.argv[1]
    stem, _ = os.path.splitext(his_file)
    his = openHIS(his_file)
    rf = ROOT.TFile(stem+'.root','recreate')

    for idx, section in enumerate(his):
        print("transferring image ",idx)
        (nx,ny) = section.shape 
        title = stem + ('_%04d' % idx)
        h2 = ROOT.TH2S(title,title,nx,0,nx,ny,0,ny)
        h2.GetXaxis().SetTitle('x')
        h2.GetYaxis().SetTitle('y')
        _ = array2hist(np.transpose(section),h2)
        h2.Write()
    rf.Close()

if __name__ == '__main__':
    main()

# vim:sw=4:sts=4:et
