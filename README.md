# sbm-tools

Hello, here is the basic workflow of a SBM simulation:

![Atom coordinates -> contact Map -> Atom Pairs List -> Force Field Potential -> Pairs Section](workflow-simple.png?raw=true "workflow")

```python
import PairsList, AtomPair from PairsList

# Initiate with a list of iterables.
p1 = PairsList([[1,2],[1,3],[2,3])

# Initiate with a list of AtomPair objects.
ap1 = AtomPair(1,2)
ap2 = AtomPair(1,3)
ap3 = AtomPair(2,3)

p1 = PairsList([a1, a2, a3])

```

The following mathematical operations can be used with PairsList:

```python
import PairsList, AtomPair from PairsList

p1 = PairsList([a1,a2,a3,a4])
p2 = PairsList([a1,a2,a5])

# addition
p3 = p1 + p2           # returns PairsList([a1,a2,a3,a4,a1,a2,a5])
p3 = p1.add(p2)        # returns PairsList([a1,a2,a3,a4,a1,a2,a5])

# substraction (behaves as set difference)
p3 = p1 - p2           # returns PairsList([a3,a4])

```

The following set operations have been implemented:

```python
import PairsList, AtomPair from PairsList

p1 = PairsList([a1,a2,a3,a4])
p2 = PairsList([a1,a2,a5])

# union
p3 = p1.union(p2)      # returns PairsList([a1,a2,a3,a4,a5])

# intersection
p3 = p1.intersect(p2)  # returns PairsList([a1,a2])

# difference
p3 = p1 - p2           # returns PairsList([a3,a4])

# symmetric difference
p3 = p1.symmetric_difference # returns PairsList([a4,a5])


```