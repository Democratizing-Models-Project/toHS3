#!/bin/env python

import os

def pyhf2hf(infile):
    from pyhf.cli.rootio import json2xml
    json2xml.callback(infile, 'tmp', 'config', 'data', 'FitConfig', [])

def hf2ws():
    os.system('hist2workspace ./tmp/FitConfig.xml')

def ws2hs3(outfile):
    import ROOT, glob
    infile = ROOT.TFile.Open(*glob.glob('./tmp/config/FitConfig_combined*.root'),"READ")
    ws = infile.Get("combined")
    tool = ROOT.RooJSONFactoryWSTool(ws)
    tool.exportJSON(outfile)

def main(infile, outfile):
    pyhf2hf(infile)
    hf2ws()
    ws2hs3(outfile)
    if os.path.isdir('./tmp'):
        import shutil
        shutil.rmtree('./tmp')

if __name__ == "__main__":
    """
    Convert from pyhf json to HS3 json.
    Usage:
        python pyhf2hs3.py [INPUT] [OUTPUT]
    """
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("outfile")
    args = parser.parse_args()
    main(args.infile, args.outfile)
