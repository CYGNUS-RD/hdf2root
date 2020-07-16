#!/bin/env python3
# usage: python3 his2root.py run03642.HIS

import os,sys
import h5py
import numpy as np 
import ROOT
from root_numpy import array2hist

from readerHIS import openHIS

def main(args,options):
    if len(args) < 1:
        print('syntax: python3 his2root.py <his file> [options]')
        sys.exit(1)

    his_file = args[0]
    stem, _ = os.path.splitext(his_file)
    his = openHIS(his_file)
    outname = stem+'.root' if not options.outfile else options.outfile
    rf = ROOT.TFile(outname,'recreate')

    runN = stem.split('run')[-1]
    run = runN if len(runN) else 'XXXX'

    for idx, section in enumerate(his):
        if options.maxEntries>-1 and idx>=options.maxEntries: 
            break
        print("transferring image ",idx)
        (nx,ny) = section.shape 
        title = stem + ('_%04d' % idx)
        postfix = 'run{run}_ev{ev}'.format(run=run,ev=idx)
        title = 'pic_{pfx}'.format(pfx=postfix)
        h2 = ROOT.TH2S(title,title,nx,0,nx,ny,0,ny)
        h2.GetXaxis().SetTitle('x')
        h2.GetYaxis().SetTitle('y')
        _ = array2hist(np.fliplr(np.transpose(section)),h2)
        h2.Write()
    rf.Close()

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage='%prog file.his [options] ')
    parser.add_option('-o',  '--outfile'    , dest='outfile'   , type="string", default=None, help='if given, assign this name to the ROOT output file (default is inputname.root)');
    parser.add_option('-m',  '--max-entries', dest='maxEntries', type=int     , default=-1,   help='if given, process only the first given images');
    (options, args) = parser.parse_args()

    main(args,options)
