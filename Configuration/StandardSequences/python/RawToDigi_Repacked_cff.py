import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.RawToDigi_cff import *

from Configuration.ProcessModifiers.gpu_cff import gpu
from Configuration.ProcessModifiers.alpaka_cff import alpaka

scalersRawToDigi.scalersInputTag = 'rawDataRepacker'
csctfDigis.producer = 'rawDataRepacker'
dttfDigis.DTTF_FED_Source = 'rawDataRepacker'
gctDigis.inputLabel = 'rawDataRepacker'
gtDigis.DaqGtInputTag = 'rawDataRepacker'
gtEvmDigis.EvmGtInputTag = 'rawDataRepacker'
siPixelDigis.InputLabel = 'rawDataRepacker'
siStripDigis.ProductLabel = 'rawDataRepacker'
ecalDigisCPU.InputLabel = 'rawDataRepacker'
gpu.toModify(ecalDigisGPU, InputLabel = 'rawDataRepacker')
alpaka.toModify(ecalDigisPortable, InputLabel = 'rawDataRepacker')
ecalPreshowerDigis.sourceTag = 'rawDataRepacker'
hcalDigis.InputLabel = 'rawDataRepacker'
muonCSCDigis.InputObjects = 'rawDataRepacker'
muonDTDigis.inputLabel = 'rawDataRepacker'
muonRPCDigis.InputLabel = 'rawDataRepacker'
castorDigis.InputLabel = 'rawDataRepacker'

RawToDigiTask = cms.Task(
    csctfDigis,
    dttfDigis,
    gctDigis,
    gtDigis,
    gtEvmDigis,
    siPixelDigis,
    siStripDigis,
    ecalDigis,
    ecalPreshowerDigis,
    hcalDigis,
    muonCSCDigis,
    muonDTDigis,
    muonRPCDigis,
    castorDigis,
    scalersRawToDigi)

RawToDigi = cms.Sequence(RawToDigiTask)

RawToDigiTask_woGCT = RawToDigiTask.copyAndExclude([gctDigis])
RawToDigi_woGCT = cms.Sequence(RawToDigiTask_woGCT)

siStripVRDigis = siStripDigis.clone(ProductLabel = 'virginRawDataRepacker')
RawToDigiTask_withVR = cms.Task(RawToDigiTask, siStripVRDigis)
RawToDigi_withVR = cms.Sequence(RawToDigiTask_withVR)
