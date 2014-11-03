import FWCore.ParameterSet.Config as cms

process = cms.Process('TRACKANA')
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.ReconstructionHeavyIons_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.GlobalTag.globaltag = 'STARTHI53_V27::All'
#process.GlobalTag.globaltag = 'GR_R_53_LV6::All'
process.GlobalTag.globaltag = 'STARTHI53_LV1::All'

process.load('Appeltel.HIN12010_TrkCorr.PbPbTrackingCorrections_cfi')
process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('trackCorrections.root')
#    fileName = cms.string('/net/hisrv0001/home/rconway/HIN_12_010/TrkCorr/CMSSW_5_3_20/src/Appeltel/HIN12010_TrkCorr/test/output/trackCorrections.root')
)


from HeavyIonsAnalysis.Configuration.CommonFunctions_cff import *
overrideCentrality(process)

process.HeavyIonGlobalParameters = cms.PSet(
  centralityVariable = cms.string("HFtowers"),
#  nonDefaultGlauberModel = cms.string(""),
  nonDefaultGlauberModel = cms.string("Hydjet_Drum"),
  centralitySrc = cms.InputTag("hiCentrality"),
  )

process.load("SimTracker.TrackAssociation.trackingParticleRecoTrackAsssociation_cfi")
process.tpRecoAssocGeneralTracks = process.trackingParticleRecoTrackAsssociation.clone()
process.tpRecoAssocGeneralTracks.label_tr = cms.InputTag("hiGeneralTracks")

process.load("SimTracker.TrackAssociation.TrackAssociatorByHits_cfi")
process.TrackAssociatorByHits.SimToRecoDenominator = cms.string('reco')

# Input source
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames =  cms.untracked.vstring(
'/store/himc/HiFall13DR53X/Pyquen_DiJet_Pt120_TuneZ2_Unquenched_Hydjet1p8_2760GeV/GEN-SIM-RECO/NoPileUp_STARTHI53_LV1-v3/00000/0010470D-A6DD-E311-99E2-00266CF9AE10.root'
    )
)

#process.load("HLTrigger.HLTfilters.hltHighLevel_cfi")
#process.hltMinBiasHFOrBSC= process.hltHighLevel.clone()
#process.hltMinBiasHFOrBSC.HLTPaths = ["HLT_HIMinBiasHfOrBSC_v1"]


process.p = cms.Path(
			process.siPixelRecHits *
#            process.hltMinBiasHFOrBSC * 
			process.collisionEventSelection *
			process.tpRecoAssocGeneralTracks *
			process.PbPbTrkCorr
)			 


