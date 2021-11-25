#!/bin/env python3

import os,sys
import ROOT

def main(args,options):
    if len(args) < 1:
        print('syntax: python3 rename_histos.py <his file> [options]')
        sys.exit(1)
    exotic_rootfiles = args[0:]
    print ("Will translate files: ",exotic_rootfiles)
    for f in exotic_rootfiles:

        print ("\t===> Converting exotic ROOT file: ",f)
        outname = f.replace('.root','_std.root')
        print ("new file will be ",outname)
        # std_tf = ROOT.TFile.Open(outname,'recreate')

        exo_tf = ROOT.TFile.Open(f)

        pics = [k.GetName() for k in exo_tf.GetListOfKeys() if 'pic' in k.GetName()]
        # print ("Pics are :",pics)

        for i,pic in enumerate(pics):
            if options.maxEntries>-1 and i>=options.maxEntries: 
                break
            name = pic.split('/')[-1]
            run = (name.split('_')[0])[-5:]
            event = (name.split('_')[-1]).split('ev')[-1]
            newname = 'pic_run{r}_ev{e}'.format(r=run,e=event)
            print(pic)
            print(newname)

            exo_tf.cd()
            exo_histo = exo_tf.Get(pic)
            print(exo_histo.GetName())
            std_histo = exo_histo.Clone(newname)

            #std_tf.cd()
            #std_histo.Write()
            
    #std_tf.Close()
    exo_tf.Close()
        
if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage='%prog file1.his, file2.his... (or file*.his) [options] ')
    parser.add_option('-o',  '--outfile'    , dest='outfile'   , type="string", default=None, help='if given, assign this name to the ROOT output file (default is inputname.root)');
    parser.add_option('-m',  '--max-entries', dest='maxEntries', type=int     , default=-1,   help='if given, process only the first given images');
    (options, args) = parser.parse_args()

    main(args,options)
