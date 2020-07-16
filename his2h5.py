#!/bin/env python3
# usage: python3 his2root.py run03642.HIS

import os,sys
import h5py
import numpy as np

from readerHIS import openHIS

def main(args,options):
    if len(args) < 1:
        print('syntax: python3 his2root.py <his file> [options]')
        sys.exit(1)

    his_file = args[0]
    stem, _ = os.path.splitext(his_file)
    outname =  stem if not options.outfile else options.outfile
    his = openHIS(his_file)
    for idx, section in enumerate(his):
        h5_file = outname + ('-%04d.h5' % idx)
        if options.maxEntries>-1 and idx>=options.maxEntries: 
            break
        if os.path.exists(h5_file):
            print('Refusing to write to ' + h5_file + ': file exists')
            sys.exit(1)
        print("transferring image ",idx)
        h5 = h5py.File(h5_file,'w')
        dset = h5.create_dataset("Image", section.shape, 'i')
        dset[...] = np.fliplr(np.transpose(section))
        #dset.attrs['comment'] = section.HIS.comment
        dset.attrs['his-header'] = repr(section.HIS.hdr)
        h5.close()

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage='%prog file.his [options] ')
    parser.add_option('-o',  '--outfile'    , dest='outfile'   , type="string", default=None, help='if given, assign this name to the ROOT output file (default is inputname.root)');
    parser.add_option('-m',  '--max-entries', dest='maxEntries', type=int     , default=-1,   help='if given, process only the first given images');
    (options, args) = parser.parse_args()

    main(args,options)

