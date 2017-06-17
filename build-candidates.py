#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
from modularAnalysis import inputMdstList
from vertex import vertexRave
from modularAnalysis import inputMdst, fillParticleList, reconstructDecay
from modularAnalysis import ntupleFile, ntupleTree, process, statistics
from modularAnalysis import analysis_main # the default analysis path

# load input ROOT file
inputMdst('default', 'mdst-dstars.root')
#files = glob.glob('/home/belle/rachac/skim/outputFiles/*ccbar.mdst.root')
#inputMdstList('default', files)

# --------------------------------------------------
# Create and fill final state ParticleLists
# --------------------------------------------------

fillParticleList('pi+:std', 'chiProb > 0.001 and abs(d0) < 2 and abs(z0) < 4')
fillParticleList('K+:std', 'chiProb > 0.001 and abs(d0) < 2 and abs(z0) < 4')

# reconstruct D0:kpi and perform a mass constrained vertex fit
reconstructDecay('D0:kpi -> K-:std pi+:std', '1.835 < M < 1.895')
vertexRave('D0:kpi', 0.001)

# reconstruct the D*+ from the D0:kpi and pi+:std
reconstructDecay('D*+:sig -> D0:kpi pi+:std', '1.7 < M < 2.3')

# --------------------------------------------------
# write out useful information to a ROOT file
# --------------------------------------------------

# information to be saved to file
toolsnu = ['EventMetaData', '^D*+:sig']
toolsnu += ['Kinematics', '^D*+:sig -> [^D0:kpi -> ^K-:std ^pi+:std] ^pi+:std']
toolsnu += ['InvMass[BeforeFit]', '^D*+:sig -> [^D0:kpi -> K-:std pi+:std] pi+:std']
toolsnu += ['MCTruth', '^D*+:sig -> [^D0:kpi -> ^K-:std ^pi+:std] ^pi+:std']
toolsnu += ['PID', 'D*+:sig -> [D0:kpi -> ^K-:std ^pi+:std] ^pi+:std']

# write out the flat ntuple
ntupleFile('candidates.root')
ntupleTree('dsttree', 'D*+:sig', toolsnu)


# --------------------------------------------------
# Process the events and print call statistics
# --------------------------------------------------

process(analysis_main)
print(statistics)
