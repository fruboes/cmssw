#!/bin/bash
root -l -b << EOF
  TString makeshared(gSystem->GetMakeSharedLib());
  TString dummy = makeshared.ReplaceAll("-W ", "-D__USE_XOPEN2K8 ");
  gSystem->SetMakeSharedLib(makeshared);
  gSystem->Load("libFWCoreFWLite");
  AutoLibraryLoader::enable();
  gSystem->Load("libDataFormatsFWLite.so");
  gSystem->Load("libDataFormatsCommon.so");
  .x GetLuminosity.C+
EOF
export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:$PATH
pip install --install-option="--prefix=$HOME/.local" brilws &> /dev/null #will be installed only the first time
brilcalc lumi -i out.json -n 0.962 -u /pb -o LUMI_TABLE
cat LUMI_TABLE
