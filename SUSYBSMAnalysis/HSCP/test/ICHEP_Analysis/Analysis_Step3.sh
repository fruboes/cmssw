root -l -b << EOF
  TString makeshared(gSystem->GetMakeSharedLib());
  TString dummy = makeshared.ReplaceAll("-W ", "-Wno-deprecated-declarations -Wno-deprecated -Wno-unused-local-typedefs -Wno-attributes ");
  TString dummy = makeshared.ReplaceAll("-Woverloaded-virtual ", " ");
  TString dummy = makeshared.ReplaceAll("-Wshadow ", " -std=c++0x -D__USE_XOPEN2K8 ");
  cout << "Compilling with the following arguments: " << makeshared << endl;
  gSystem->SetMakeSharedLib(makeshared);
  gSystem->Load("libFWCoreFWLite");
  AutoLibraryLoader::enable();
  gSystem->Load("libDataFormatsFWLite.so");
  gSystem->Load("libAnalysisDataFormatsSUSYBSMObjects.so");
  gSystem->Load("libDataFormatsVertexReco.so");
  gSystem->Load("libDataFormatsCommon.so");
  gSystem->Load("libDataFormatsHepMCCandidate.so");
  gSystem->Load("libPhysicsToolsUtilities.so");
  .x Analysis_Step3.C++("ANALYSE_0_to_0", 0);
EOF

