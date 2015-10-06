#!/usr/bin/env python

import urllib
import string
import os
import sys
import SUSYBSMAnalysis.HSCP.LaunchOnCondor as LaunchOnCondor  
import glob
import time
"""
check that a file exist and is not corrupted
"""
def checkInputFile(url):
    if(url.startswith('/store')==True):
       url= 'root://eoscms//eos/cms'+url
    command_out = commands.getstatusoutput("root -l -b -q " + url)
    if(command_out[1].find("Error")>=0 or command_out[1].find("probably not closed")>=0 or command_out[1].find("Corrupted")>=0):return False
    return True


samples = [
#SampleName, generator config file, NJobs, NEvents/Job
  ['Gluino_13TeV_M100' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluino_M_100_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M200' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluino_M_200_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M400' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluino_M_400_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M600' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluino_M_600_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M800' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluino_M_800_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M1000', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluino_M_1000_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M1200', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluino_M_1200_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M1400', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluino_M_1400_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M1600', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluino_M_1600_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M1800', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluino_M_1800_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M2000', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluino_M_2000_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M2200', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluino_M_2200_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M2400', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluino_M_2400_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M2600', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluino_M_2600_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M100N' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluinoonlyneutral_M_100_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M200N' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluinoonlyneutral_M_200_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M400N' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluinoonlyneutral_M_400_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M600N' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluinoonlyneutral_M_600_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M800N' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluinoonlyneutral_M_800_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M1000N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluinoonlyneutral_M_1000_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M1200N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluinoonlyneutral_M_1200_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M1400N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluinoonlyneutral_M_1400_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M1600N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluinoonlyneutral_M_1600_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M1800N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluinoonlyneutral_M_1800_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M2000N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluinoonlyneutral_M_2000_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M2200N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluinoonlyneutral_M_2200_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M2400N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluinoonlyneutral_M_2400_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Gluino_13TeV_M2600N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgluinoonlyneutral_M_2600_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],

  ['Stop_13TeV_M100' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPstop_M_100_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M200' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPstop_M_200_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M400' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPstop_M_400_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M600' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPstop_M_600_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M800' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPstop_M_800_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M1000', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstop_M_1000_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M1200', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstop_M_1200_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M1400', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstop_M_1400_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M1600', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstop_M_1600_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M1800', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstop_M_1800_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M2000', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstop_M_2000_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M2200', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstop_M_2200_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M2400', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstop_M_2400_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M2600', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstop_M_2600_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M100N' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPstoponlyneutral_M_100_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M200N' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPstoponlyneutral_M_200_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M400N' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPstoponlyneutral_M_400_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M600N' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPstoponlyneutral_M_600_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M800N' , 'Configuration/GenProduction/python/ThirteenTeV/HSCPstoponlyneutral_M_800_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M1000N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstoponlyneutral_M_1000_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M1200N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstoponlyneutral_M_1200_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M1400N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstoponlyneutral_M_1400_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M1600N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstoponlyneutral_M_1600_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M1800N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstoponlyneutral_M_1800_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M2000N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstoponlyneutral_M_2000_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M2200N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstoponlyneutral_M_2200_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M2400N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstoponlyneutral_M_2400_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],
  ['Stop_13TeV_M2600N', 'Configuration/GenProduction/python/ThirteenTeV/HSCPstoponlyneutral_M_2600_TuneCUETP8M1_13TeV_pythia8_cff.py', 50, 500],

  ['GMStau_13TeV_M156', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgmstau_M_156_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['GMStau_13TeV_M200', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgmstau_M_200_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['GMStau_13TeV_M247', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgmstau_M_247_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['GMStau_13TeV_M308', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgmstau_M_308_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['GMStau_13TeV_M432', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgmstau_M_432_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['GMStau_13TeV_M494', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgmstau_M_494_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['GMStau_13TeV_M557', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgmstau_M_557_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['GMStau_13TeV_M651', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgmstau_M_651_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['GMStau_13TeV_M745', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgmstau_M_745_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['GMStau_13TeV_M871', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgmstau_M_871_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['GMStau_13TeV_M1029', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgmstau_M_1029_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['GMStau_13TeV_M1218', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgmstau_M_1218_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['GMStau_13TeV_M1409', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgmstau_M_1409_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['GMStau_13TeV_M1599', 'Configuration/GenProduction/python/ThirteenTeV/HSCPgmstau_M_1599_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],

  ['PPStau_13TeV_M156', 'Configuration/GenProduction/python/ThirteenTeV/HSCPppstau_M_156_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['PPStau_13TeV_M200', 'Configuration/GenProduction/python/ThirteenTeV/HSCPppstau_M_200_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['PPStau_13TeV_M247', 'Configuration/GenProduction/python/ThirteenTeV/HSCPppstau_M_247_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['PPStau_13TeV_M308', 'Configuration/GenProduction/python/ThirteenTeV/HSCPppstau_M_308_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['PPStau_13TeV_M432', 'Configuration/GenProduction/python/ThirteenTeV/HSCPppstau_M_432_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['PPStau_13TeV_M494', 'Configuration/GenProduction/python/ThirteenTeV/HSCPppstau_M_494_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['PPStau_13TeV_M557', 'Configuration/GenProduction/python/ThirteenTeV/HSCPppstau_M_557_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['PPStau_13TeV_M651', 'Configuration/GenProduction/python/ThirteenTeV/HSCPppstau_M_651_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['PPStau_13TeV_M745', 'Configuration/GenProduction/python/ThirteenTeV/HSCPppstau_M_745_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['PPStau_13TeV_M871', 'Configuration/GenProduction/python/ThirteenTeV/HSCPppstau_M_871_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['PPStau_13TeV_M1029', 'Configuration/GenProduction/python/ThirteenTeV/HSCPppstau_M_1029_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['PPStau_13TeV_M1218', 'Configuration/GenProduction/python/ThirteenTeV/HSCPppstau_M_1218_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['PPStau_13TeV_M1409', 'Configuration/GenProduction/python/ThirteenTeV/HSCPppstau_M_1409_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
  ['PPStau_13TeV_M1599', 'Configuration/GenProduction/python/ThirteenTeV/HSCPppstau_M_1599_TuneZ2star_13TeV_pythia6_cff.py', 50, 500],
]


if sys.argv[1]=='1':  #GEN-SIM-DIGI-RECO-AOD in one shot
   #this is common to all samples, so we need to do it only once
   os.system('cmsDriver.py --filein file:step1.root --fileout XXX_OUTPUT_XXX_XXX_I_XXX.root --mc --eventcontent AODSIM --datatier GEN-SIM-DIGI-AOD --conditions auto:run2_mc --step HLT:GRun,RAW2DIGI,L1Reco,RECO --python_filename RECO_Template_cfg.py --magField 38T_PostLS1 --geometry Extended2015 --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --no_exec -n -1')

   for S in samples:
      if('HSCP' in S[1]):
         os.system('cmsDriver.py ' + S[1] + ' --fileout file:step1.root --mc --eventcontent RAWSIM --datatier GEN-SIM-RAW --conditions auto:run2_mc --step GEN,SIM,DIGI,L1,DIGI2RAW --python_filename GEN_SIM_Template_cfg.py --magField 38T_PostLS1 --geometry Extended2015 --customise SimG4Core/CustomPhysics/Exotica_HSCP_SIM_cfi.customise,SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --no_exec -n 10')
      else:
         os.system('cmsDriver.py ' + S[1] + ' --fileout file:step1.root --mc --eventcontent RAWSIM --datatier GEN-SIM-RAW --conditions auto:run2_mc --step GEN,SIM,DIGI,L1,DIGI2RAW --python_filename GEN_SIM_Template_cfg.py --magField 38T_PostLS1 --geometry Extended2015 --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --no_exec -n 10')

      with open("GEN_SIM_Template_cfg.py", "a") as f:
         f.write('process.RandomNumberGeneratorService.generator.initialSeed = cms.untracked.uint32(XXX_SEED_XXX)\n')
         f.write('process.RandomNumberGeneratorService.mix.initialSeed = cms.untracked.uint32(XXX_SEED_XXX)\n')
         f.write('process.maxEvents.input = cms.untracked.int32(XXX_NEVENTS_XXX)\n')
#         f.write('process.RAWSIMoutput.fileName = cms.untracked.string("file:XXX_OUTPUT_XXX_XXX_I_XXX.root")\n')
         f.write('process.source.firstLuminosityBlock =  cms.untracked.uint32(1XXX_I_XXX)\n')
         f.close()

      JobName = S[0]+"_SIMAOD"
      FarmDirectory = "FARM_"+JobName
      LaunchOnCondor.Jobs_NEvent = S[3]
      LaunchOnCondor.Jobs_Skip = 0
      LaunchOnCondor.SendCluster_Create(FarmDirectory, JobName)
      for i in range(0,S[2]):
           LaunchOnCondor.Jobs_Count = i
           LaunchOnCondor.Jobs_Skip+=LaunchOnCondor.Jobs_NEvent
           LaunchOnCondor.SendCluster_Push  (["CMSSW", ["GEN_SIM_Template_cfg.py", "RECO_Template_cfg.py"] ])
           LaunchOnCondor.Jobs_FinalCmds = ['rm step1.root']
      LaunchOnCondor.SendCluster_Submit()




elif sys.argv[1]=='2':  #AOD --> EDM files
   for S in samples:
      JobName = S[0]
      FarmDirectory = "FARM_EDM"
      LaunchOnCondor.SendCluster_Create(FarmDirectory, JobName)

      f = open("HSCPEDM_cfg.py", "w")
      f.write("import sys, os\n")
      f.write("import FWCore.ParameterSet.Config as cms\n")
      f.write("\n")
      if('HSCP' in S[1]):
         f.write("isSignal = True\n")
         f.write("isBckg = False\n")
      else:
         f.write("isSignal = False\n")
         f.write("isBckg = True\n")
      f.write("isData = False\n")
      f.write("isSkimmedSample = False\n")
      f.write("GTAG = 'MCRUN2_74_V8'\n")
      f.write("OUTPUTFILE = 'XXX_OUTPUT_XXX.root'\n")
      f.write("InputFileList = cms.untracked.vstring()\n")
      f.write("\n")
      for i in range(0,S[2]):
         inFile = os.getcwd()+"/FARM_"+S[0]+"_SIMAOD/outputs/"+S[0]+"_SIMAOD_%04i.root" % i
         f.write("InputFileList.extend(['file:"+inFile+"'])\n")
#         if(checkInputFile(inFile) ):
#            f.write("InputFileList.extend(['file:"+inFile+"'])\n")
#         else:
#            print "missing "+ inFile
      f.write("\n")
      f.write("#main EDM tuple cfg that depends on the above parameters\n")
      f.write("execfile( os.path.expandvars('${CMSSW_BASE}/src/SUSYBSMAnalysis/HSCP/test/MakeEDMtuples/HSCParticleProducer_cfg.py') )\n")
      f.close()

      LaunchOnCondor.SendCluster_Push  (["CMSSW", "HSCPEDM_cfg.py" ])
      LaunchOnCondor.SendCluster_Submit()

elif sys.argv[1]=='3':  #Transfert final EDM files from your place to CERN CMST3
   for S in samples:
      os.system('lcg-cp --verbose -b -D srmv2 "srm://ingrid-se02.cism.ucl.ac.be:8444/srm/managerv2?SFN=/storage/data/cms/store/user/quertenmont/15_05_20_HSCP_AODSIM/'+S[0]+'.root" "srm://srm-eoscms.cern.ch:8443/srm/v2/server?SFN=/eos/cms//store/cmst3/user/querten/15_03_25_HSCP_Run2EDMFiles/'+S[0]+'.root" &> LOG_'+S[0]+'.log &')
