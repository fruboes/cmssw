import FWCore.ParameterSet.Config as cms

process = cms.Process("runRivetAnalysis")

process.load('Configuration.StandardSequences.Services_cff')


process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(10000)

process.load("Configuration/Generator/MinBias_13TeV_cfi")


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10000)
)

process.source = cms.Source("EmptySource")


process.load("GeneratorInterface.RivetInterface.rivetAnalyzer_cfi")

process.rivetAnalyzer.AnalysisNames = cms.vstring('CMS_TMF_14_123')

process.p = cms.Path(process.generator*process.rivetAnalyzer)


