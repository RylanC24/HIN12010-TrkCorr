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

process.load('Appeltel.HIN12010_TrkCorr.RpPbTrackingCorrections_cfi')
process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('trackCorrections.root')
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
'/store/himc/HiFall13DR53X/Pyquen_Unquenched_AllQCDPhoton170_PhotonFilter35GeV_eta3_TuneZ2_Hydjet1p8_2760GeV/GEN-SIM-RECO/NoPileUp_STARTHI53_LV1-v1/30000/00018A42-C621-E411-B8FD-848F69FD4EB6.root'
    )
)

process.load("HLTrigger.HLTfilters.hltHighLevel_cfi")
process.hltMinBiasHFOrBSC= process.hltHighLevel.clone()
process.hltMinBiasHFOrBSC.HLTPaths = ["HLT_PAZeroBiasPixel_SingleTrack_v1"]


process.p = cms.Path(
			process.siPixelRecHits *
			process.hltMinBiasHFOrBSC * 
			process.collisionEventSelection *
			process.tpRecoAssocGeneralTracks *
			process.pPbTrkCorr
)			 


