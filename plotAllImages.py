import ROOT
ROOT.gROOT.SetBatch(True)

if __name__ == '__main__':

    from optparse import OptionParser
    parser = OptionParser(usage='%prog rootfile [opts] ')
    parser.add_option('-d', '--dir', dest='dirWithPlot', default=None, type='string', help='directory where to put plots')
    (options, args) = parser.parse_args()

    ROOT.gStyle.SetOptStat(0)
    tf = ROOT.TFile.Open(args[0])
    
    c = ROOT.TCanvas('c','c',600,600)
    for i,e in enumerate(tf.GetListOfKeys()):
        name=e.GetName()
        obj=e.ReadObj()
        if not obj.InheritsFrom('TH2'): continue

        print("Plotting ",name,"...")
        obj.GetZaxis().SetRangeUser(90,130)
        obj.Draw('colz')
        c.SaveAs('{pdir}/{name}.jpeg'.format(pdir=options.dirWithPlot,name=name))

    print("DONE.")

