import FWCore.ParameterSet.Config as cms

###################################################################
# Set default phase-2 settings
###################################################################
import Configuration.Geometry.defaultPhase2ConditionsEra_cff as _settings
_PH2_GLOBAL_TAG, _PH2_ERA = _settings.get_era_and_conditions(_settings.DEFAULT_VERSION)

process = cms.Process("ICALIB", _PH2_ERA)
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing('analysis')
options.register('algorithm',
                 2, # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Algorithm to populate output sqlite file")
options.parseArguments()

process.load("Configuration.StandardSequences.Services_cff")
process.RandomNumberGeneratorService.prod = cms.PSet(
    initialSeed = cms.untracked.uint32(789341),
    engineName = cms.untracked.string('TRandom3')
)

## specify the default phase2 detector
process.load("Configuration.Geometry.GeometryExtendedRun4Default_cff")
process.load('Configuration.Geometry.GeometryExtendedRun4DefaultReco_cff')

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, _PH2_GLOBAL_TAG, '')

###################################################################
# Messages
###################################################################
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.enable = False
process.MessageLogger.SiPhase2BadStripChannelBuilder=dict()
process.MessageLogger.SiStripBadStrip=dict()
process.MessageLogger.cout = cms.untracked.PSet(
    enable    = cms.untracked.bool(True),
    enableStatistics = cms.untracked.bool(True),
    threshold = cms.untracked.string("INFO"),
    default   = cms.untracked.PSet(limit = cms.untracked.int32(0)),
    FwkReport = cms.untracked.PSet(limit = cms.untracked.int32(-1),
                                   reportEvery = cms.untracked.int32(1000)
                                   ),
    SiPhase2BadStripChannelBuilder = cms.untracked.PSet( limit = cms.untracked.int32(-1)),
    SiStripBadStrip = cms.untracked.PSet( limit = cms.untracked.int32(-1)),
)

process.source = cms.Source("EmptyIOVSource",
    lastValue = cms.uint64(1),
    timetype = cms.string('runnumber'),
    firstValue = cms.uint64(1),
    interval = cms.uint64(1)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string('')
    ),
    timetype = cms.untracked.string('runnumber'),
    connect = cms.string('sqlite_file:SiStripBadStripPhase2_T33_v0.db'),
    toPut = cms.VPSet(cms.PSet(
        record = cms.string('SiStripBadStripRcd'),
        tag = cms.string('SiStripBadStripPhase2_T33')
    ))
)

process.prod = cms.EDAnalyzer("SiPhase2BadStripChannelBuilder",                    
                              Record = cms.string('SiStripBadStripRcd'),
                              SinceAppendMode = cms.bool(True),
                              IOVMode = cms.string('Run'),
                              printDebug = cms.untracked.bool(False),
                              doStoreOnDB = cms.bool(True),
                              #popConAlgo = cms.uint32(1), #NAIVE
                              #popConAlgo = cms.uint32(2), #RANDOM
                              popConAlgo = cms.uint32(options.algorithm), 
                              badComponentsFraction = cms.double(0.01)  #1% of bad strips
                              #badComponentsFraction = cms.double(0.05)  #5% of bad strips
                              #badComponentsFraction = cms.double(0.1)   #10% of bad strips
                              )

#process.print = cms.OutputModule("AsciiOutputModule")

process.p = cms.Path(process.prod)
#process.ep = cms.EndPath(process.print)
