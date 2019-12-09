# sbmtools

sbmtools is a simple python package for creating, modifying, and maintaining input files for native Structure-Based Model simulations to be used with the popular simulation software [GROMACS](http://www.gromacs.org/).

### Table of Contents
[Introduction](#introduction)  
[Installation](#installation)  
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
### Usage


![Atom coordinates -> contact Map -> Atom Pairs List -> Force Field Potential -> Pairs Section](workflow-simple.png?raw=true "workflow")

```python
from sbmtools.pairs import PairsList, AtomPair

# Initiate with a list of iterables.
p1 = PairsList([[1, 2],[1, 3],[2, 3]])

# Initiate with a list of AtomPair objects.
ap1 = AtomPair(1, 2)
ap2 = AtomPair(1, 3)
ap3 = AtomPair(2, 3)

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


