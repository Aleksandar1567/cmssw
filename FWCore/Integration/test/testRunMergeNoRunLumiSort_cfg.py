# A test of the noRunLumiSort configuration parameter
# where the input has non-contiguous event sequences
# from the same run.

# It is expected there are 8 warnings and 8 errors that
# print out while this runs related to merging.
# The test should pass with these errors and warnings.

import FWCore.ParameterSet.Config as cms

process = cms.Process("NORUNLUMISORT")

from IOPool.Input.modules import PoolSource
process.source = PoolSource(
    fileNames = [
        'file:testRunMergeMERGE6.root', 
        'file:testRunMergeMERGE6.root'
    ],
    duplicateCheckMode = 'checkEachRealDataFile',
    noRunLumiSort = True
)

from FWCore.Framework.modules import RunLumiEventAnalyzer
process.test2 = RunLumiEventAnalyzer(
    verbose = True,
    expectedRunLumiEvents = [
1, 0, 0,
1, 1, 0,
1, 1, 11,
1, 1, 12,
1, 1, 13,
1, 1, 14,
1, 1, 15,
1, 1, 16,
1, 1, 17,
1, 1, 18,
1, 1, 19,
1, 1, 20,
1, 1, 21,
1, 1, 22,
1, 1, 23,
1, 1, 24,
1, 1, 25,
1, 1, 0,
1, 0, 0,
2, 0, 0,
2, 1, 0,
2, 1, 1,
2, 1, 2,
2, 1, 3,
2, 1, 4,
2, 1, 5,
2, 1, 0,
2, 0, 0,
1, 0, 0,
1, 1, 0,
1, 1, 1,
1, 1, 2,
1, 1, 3,
1, 1, 4,
1, 1, 5,
1, 1, 6,
1, 1, 7,
1, 1, 8,
1, 1, 9,
1, 1, 10
]
)
process.test2.expectedRunLumiEvents.extend([
1, 1, 11,
1, 1, 12,
1, 1, 13,
1, 1, 14,
1, 1, 15,
1, 1, 16,
1, 1, 17,
1, 1, 18,
1, 1, 19,
1, 1, 20,
1, 1, 21,
1, 1, 22,
1, 1, 23,
1, 1, 24,
1, 1, 25,
1, 1, 0,
1, 0, 0,
2, 0, 0,
2, 1, 0,
2, 1, 1,
2, 1, 2,
2, 1, 3,
2, 1, 4,
2, 1, 5,
2, 1, 0,
2, 0, 0,
1, 0, 0,
1, 1, 0,
1, 1, 1,
1, 1, 2,
1, 1, 3,
1, 1, 4,
1, 1, 5,
1, 1, 6,
1, 1, 7,
1, 1, 8,
1, 1, 9,
1, 1, 10,
1, 1, 0,
1, 0, 0,
])

from IOPool.Output.modules import PoolOutputModule
process.out = PoolOutputModule(fileName = 'testRunMergeNoRunLumiSort.root')

process.path1 = cms.Path(process.test2)

process.e = cms.EndPath(process.out)
