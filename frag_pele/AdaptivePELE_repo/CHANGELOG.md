# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)

## [1.5] - 2018-MM-DD (Unreleased)

### New features:

    - Make code compatible with python2 and python3
    - Add posibility of using a third column as color in plotAdaptive
    - Add __version__ attribute to package
    - Add possibility of skipping first structure of each trajectory in
      clustering when calling cluster function

### Behaviour changes from previous version:

    - Change rmsd and be otions of plotAdaptive to lines and points
    - Change name of writePrecisePathToSnapshots to
    bactrackAdaptiveTrajectory, added name parameter to select the name of the
    output file and automatic detection of said name, so that if a file exists
    with the same name, a number is added at the end to differentiate them

### Bug fixes:

    - Fix bug in alternative structure when a cluster had no other structure
    than the representative
    - Fix several bugs related to unicode and string handling

## [1.4.2] - 2018-03-02

### New features:

    - Added null spawning calculator
    - Added possibility of max metric in epsilon

### Behaviour changes from previous version:

    - Improvements in REAP spawning
    - Metric columns in control file now start by 1
    - Changed symbolic links in rawData in freeEnergies calculation to
    relative paths

### Bug fixes:

    - Various bug fixes

## [1.4] - 2018-01-30

### New features:

    - Added scripts plot3DNetwork, plotSpawningClusters for better
    visualization of simulations
    - Added exitContinuous density for exit path simulations
    - Added possibility to change the simulation box at each epoch
    - Added equilibration procedure
    - Added possibility to test metric greater than in metric exit condition
    - Added metricMultipleTrajectories exit condition

### Behaviour changes from previous version:

    - Moved buildRevTransitionMatrixFunction to Cython code (speed-up of up to
    500x)

### Bug fixes:

    - Fixed minor bug in controlFileValidator
    - Fixed bug in writePrecisePathToSnapshot, where backtracking was not
    carried out until the initial structure

## [1.3] - 2017-06-01

### New features:

    - Added script to reconstruct precise path to a given snapshot
    (writePrecisePathToSnapshot.py)
    - Added possibility of chain and resnum selection in PDB
    - Added scripts to calculate free energies in pyemma_scripts
    - Added new parameter to control the number of clusters considered in
    epsilon scoring

### Behaviour changes from previous version:

    - Change names of clustering in control file 

### Bug fixes:

    - Minor bug fixes in scripts to calculate free energies
    - Fixed bug of incorrect trajectory selection in estimateDG
    - Fixed bug of multiple its plot not visible (bug due to pyemma)

## [1.2] - 2017-05-09

### New features:

    - Added conformation network and first discovery tree to improve
    simulation analysis
    - Added scripts to plot RMSF for each residue over a trajectory
    - Added scripts to calculate contact map histogram for each residue over a
    trajectory or a complete simulation
    - Added scripts to create a network of residues  over a trajectory or a
    complete simulation
    - Added more robust pickling interface so old simulation can be used with
    newer version (to some extent)
    - Added script to reconstruct approximate path to a given snapshot
    (writeTrajToSnapshot.py)

### Behaviour changes from previous version:

    - Alternative structures are stored in a priority queue with the priority
    set to the population of the subclusters spawn inversely proportinal way
    according to this population

### Bug fixes:

    - Fix bug in spawning of alternative structures, was not calling the new
    code for randomly spawn from cluster center of alternative structure
    - Fix bug in pickling (serializing) coordinates of Atom objects
    - Fix bug in pickling AltStructures objects

## [1.1] - 2017-02-17

### New features:

    - Follow proper packaging conventions for Python packaging
    - Added alternative structure to each cluster that will spawn 50% of the
    time
    - Implemented UCB algorithm for spawning
    
### Behaviour changes from previous version:

    - Atomset package implemented in Cython (faster)
    - Jaccard index is calcualed using only the cells of the matrix that are 1

## [1.0] - 2017-01-19

### New features:

    - Added support for symmetry with contactMap
    - Added lastSnapshot clustering for easy restart of sequential runs
    - Added independent spawning to perform classical PELE simulations
    - Added exitCondition on metric
    - Added support for changing clustering when clustering method parameter changes, and be able to handle
    metric column change in spawning
    - Added suport for wildcard in control file input structures
    - Added several scripts for analysis

### Behaviour changes from previous version:

    - Changed quadratic function for continuous
    - Changed symmetry dictionary for list of dictionaries, with symmetry groups

### Bug fixes:

    - Fixed bug of incorrect atom consideration in symmetries
    - Fixed bug of NaN correlation similarity evaluator in contactMap