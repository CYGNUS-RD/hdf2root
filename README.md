# hdf2root
Some code to convert HDF5 images to root

* USAGE:
   * convert a list of h5 files:              `hdf2root.py Run720/run720*.h5 -o neutrons.root`

   * convert all the h5 files in a directory: `hdf2root.py -d Run720`  (by default will put TH2s into Run720.root)

# HIS conversion to ROOT or H5
* python3 his2root.py run03642.HIS
makes one root file (run03642.root) with all the TH2S inside with the usual format

* python3 his2h5.py run03642.HIS
makes one H5 file / image
