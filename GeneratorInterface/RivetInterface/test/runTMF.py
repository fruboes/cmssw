import FWCore.ParameterSet.Config as cms

process = cms.Process("runRivetAnalysis")

process.load('Configuration.StandardSequences.Services_cff')


process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(10000)

process.load("Configuration/Generator/MinBias_13TeV_cfi")


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10000*10)
)

process.source = cms.Source("EmptySource")


process.load("GeneratorInterface.RivetInterface.rivetAnalyzer_cfi")

process.rivetAnalyzer.AnalysisNames = cms.vstring('CMS_TMF_14_123')


# 7.830D+01
# mb 1e-27
# pb 1e-36

# minbias:
#process.rivetAnalyzer.CrossSection = cms.double(7.830E+01*1e9) # 
# 15...1500
#process.rivetAnalyzer.CrossSection = cms.double(2.084E+00*1e9) # 
# 30...1500
#process.rivetAnalyzer.CrossSection = cms.double(1.677E-01*1e9) # 
# 50...1500
process.rivetAnalyzer.CrossSection = cms.double(2.234D-02*1e9) # 


process.p = cms.Path(process.generator*process.rivetAnalyzer)


process.generator.PythiaParameters.processParameters = cms.vstring(
                'MSEL = 1 ! QCD hight pT processes',
                'CKIN(3) = 50 ! minimum pt hat for hard interactions',
                'CKIN(4) = 1500 ! maximum pt hat for hard interactions',
        )      


print process.generator.PythiaParameters.processParameters 
