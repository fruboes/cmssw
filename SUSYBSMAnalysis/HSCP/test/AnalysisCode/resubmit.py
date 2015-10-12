#! /usr/bin/env python

import os

indir = "Results/"

for root, dirs, files in os.walk(indir):
    if "Type" not in root: continue
    anaType = int(root.split("/")[-1].replace("Type",""))
    anatypeSpecificString = ", {}, ".format(anaType)

    print root
    #for f in files:
    #    print f
    #print dirs

