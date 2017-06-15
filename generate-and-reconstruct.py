#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Generate D* -> D0 pi; D0 -> K pi to get K/pi samples """
__authors__ = ['Jake Bennett', 'Sam Cunliffe' ]

# Tested in release-00-08-00 June 2017

import os
import glob

# analysis_main is the default path created in the modularAnalysis.py
from modularAnalysis import analysis_main, generateContinuum, loadGearbox, process
from beamparameters import add_beamparameters
from simulation     import add_simulation
from reconstruction import add_reconstruction
from reconstruction import add_mdst_output

# ---------------------------------------------------
# GENERATION
# ---------------------------------------------------

# set the BeamParameters for running at the Y(4S)
beamparameters = add_beamparameters(analysis_main, "Y4S")

# generateContinuum function is defined in analysis/scripts/modularAnalysis.py
generateContinuum(1000, 'D*-', './ccbar-to-dstar.dec')

# Load geometry
loadGearbox()

# ---------------------------------------------------
# SIMULATION AND RECONSTRUCTION
# ---------------------------------------------------

# BKG files for running at KEKCC
bg = None
if 'BELLE2_BACKGROUND_DIR' in os.environ:
    bg = glob.glob(os.environ['BELLE2_BACKGROUND_DIR'] + '/*.root')

# Standard simulation and reconstruction
add_simulation(analysis_main, bkgfiles=bg)
add_reconstruction(analysis_main)

# ---------------------------------------------------
# SAVE TO OUTPUT
# ---------------------------------------------------

# Dump in MDST format
add_mdst_output(analysis_main, True, 'mdst-dstars.root')

# Process all modules added to the analysis_main path
process(analysis_main)

# Print out the summary
print(statistics)
