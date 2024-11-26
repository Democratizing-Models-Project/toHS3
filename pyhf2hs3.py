#!/bin/env python

import os
import tempfile

def pyhf2hf(infile, outdir):
    from pyhf.cli.rootio import json2xml
    json2xml.callback(infile, outdir, 'config', 'data', 'FitConfig', [])

def hf2ws(configdir):
    os.system(f'hist2workspace {configdir}/FitConfig.xml')

def ws2hs3(outfile, rootdir):
    import ROOT, glob
    infile = ROOT.TFile.Open(*glob.glob(f'{rootdir}/config/FitConfig_combined*.root'),"READ")
    ws = infile.Get("combined")
    tool = ROOT.RooJSONFactoryWSTool(ws)
    tool.exportJSON(outfile)

def main(infile, outfile):
    with tempfile.TemporaryDirectory() as tmpdir:
        pyhf2hf(infile, tmpdir)
        hf2ws(tmpdir)
        ws2hs3(outfile, tmpdir)

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
