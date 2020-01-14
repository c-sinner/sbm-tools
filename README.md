# sbmtools

sbmtools is a simple python package for creating, modifying, and maintaining input files for native Structure-Based Model simulations to be used with the popular simulation software [GROMACS](http://www.gromacs.org/).

### Table of Contents
[Introduction](#introduction)  
[Installation](#installation)  
[Syntax](#syntax) 
[Usage](#usage)  
[Credits](#credits)  
[Licence](#license)  


<a name="installation"></a>  
### Installation

There is no specific installation script at the moment. Download the repository to your machine:

```shell script
wget https://github.com/c-sinner/sbm-tools.git
```

The software writes input files for [GROMACS](http://www.gromacs.org/). If you want to use gaussian potentials please install and use the GROMACS binary distributed on the SMOG website:

[Gromacs v4.5.4 containing Gaussian contact potentials](http://smog-server.org/SBMextension.html#gauss)


<a name="introduction"></a>  
### Introduction

Hello young Padawan<sup>TM</sup>, let me guide you through the world of protein folding and explain the purpose of this repository.

#### What is a protein?

#### MD
There are many ways of running a simulation and **Structure-Based Models combined with Gromacs is only one way of running a simulation**. The two important parts for a biomolecular simulation are the **force-field** and the **simulation software**. Structure-Based Models (SBM) can be understood as a specific kind of force-field (They are a class of implicit solvent models free of electrostatic interactions). Gromacs is one of many programs to run biomolecular simulations. It needs the input parameters in specific file formats, namely .top, .gro, and .mdp files.

<a name="usage"></a>  
### Syntax
#### TopFile

```python
from sbmtools import TopFile

# Initiate an empty TopFile
t1 = TopFile()

# Create/Load a TopFile from an existing file
t1 = TopFile(path=<Path to .top>)
t2 = TopFile().load(path=<Path to .top>)

# Save TopFile
t1.save(output_path)
#TODO: Before the TopFile saves it should validate if all atom numbers in pairs/bonds/dihedrals/angles
#are defined in the atoms list.

```

#### Pairs
```python
from sbmtools import TopFile

# Add pairs
t1 = TopFile(path=<Path to .top 1>)
dca_data = panda.read_csv('dca_pairs.txt', sep=" ", header=None)
dca_pairs = PairsList(dca_data)

#method one
pairs = t1.pairs #returns bound pairslist
pairs = pairs + dca_pairs
t1.pairs = pairs

#method two
t1.pairs += dca_pairs

#method three?
t1.pairs.append(dca_pairs)

```

### Bound and unbound Pairs
One of the central operations of the SBM is to take sets of atoms (2, 3, or 4) and apply a Potential
to them to get the strength of their interaction. Groups of atoms are stored in AtomPairs (AtomGroups?).
An AtomGroup can be bound by having a Potential, or it can be unbound. If it is unbound the default Potential of
the topFile will be applied. Bind your AtomGroup entries to override the default behaviors.

#### Pairs
```python
from sbmtools.pairs import AtomGroup
from sbmtools.potentials import LennardJonesPotential

#bound group
AtomGroup(1,2, distance=0.74, potential=LennardJonesPotential)
AtomGroup.write() #prints '1      2 1  8.67324E+00 7.78048E+00'

#unbound group
AtomGroup(1,2, distance=0.74)
AtomGroup.write() #prints ''

```


<a name="usage"></a>  
### Usage

![Atom coordinates -> contact Map -> Atom Pairs List -> Force Field Potential -> Pairs Section](workflow-simple.png?raw=true "workflow")

```python
from sbmtools.pairs import PairsList, AtomPair

# Initiate with a list of iterables.
p1 = PairsList([[1, 2],[1, 3],[2, 3]])

# Initiate with a list of AtomPair objects.
ap1 = AtomPair(1, 2, distance = 0.74)
ap2 = AtomPair(1, 3, distance = 0.74)
ap3 = AtomPair(2, 3, distance = 0.74)

p1 = PairsList([ap1, ap2, ap3])

```

The following mathematical operations can be used with PairsList:

```python
from sbmtools.pairs import PairsList, AtomPair

p1 = PairsList([ap1, ap2, ap3, ap4])
p2 = PairsList([ap1, ap2, ap5])

# add pairs
p3 = p1 + p2           # returns PairsList([ap1, ap2, ap3, ap4, ap1, ap2, ap5])
p3 = p1.add(p2)        # returns PairsList([ap1, ap2, ap3, ap4, ap1, ap2, ap5])

# remove pairs (behaves as set difference)
p3 = p1 - p2           # returns PairsList([ap3, ap4])
p3 = p1.remove(p2) # returns PairsList([ap3, ap4])

```

The following set operations have been implemented:

```python
from sbmtools.pairs import PairsList, AbstractAtomPair

p1 = PairsList([ap1, ap2, ap3, ap4])
p2 = PairsList([ap1, ap2, ap5])

# union
p3 = p1.union(p2)      # returns PairsList([ap1, ap2, ap3, ap4, ap5])

# intersection
p3 = p1.intersection(p2)  # returns PairsList([ap1, ap2])

# symmetric difference
p3 = p1.symmetric_difference # returns PairsList([ap3, ap4, ap5])

```


<a name="credits"></a>  
### Credits
Code written by Dr. Claude Sinner @ UTDallas. Please get in touch if this code was useful to you or you have any questions.


<a name="license"></a>  
### License

The project builds upon eSBMTools (Lutz, Sinner, Heuermann, Schug 2013) and copies its GPL3 licence.


