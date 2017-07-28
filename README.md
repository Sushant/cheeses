# cheeses [![Build Status](https://travis-ci.org/Sushant/cheeses.svg?branch=master)](https://travis-ci.org/Sushant/cheeses)
CRDTs in Python

Heavily inspired by [Meangirls](https://github.com/aphyr/meangirls)

### Example usage

#### Sets
All sets support `add, remove, merge, clone, to_dict, to_list, to_json` methods and a `from_dict` class method.

Following examples use a hypothetical set up of 3 replicas which receive requests to add or remove an element and a cache layer that merges the results from all the replicas before returning a read response.

```
>>> import crdt
# Replica A
>>> a = crdt.TwoPhaseSet() # or crdt.LWWSet() or crdt.ORSet()
# Replica B
>>> b = crdt.TwoPhaseSet() # or crdt.LWWSet() or crdt.ORSet()
# Replica C
>>> c = crdt.TwoPhaseSet() # or crdt.LWWSet() or crdt.ORSet()

>>> a.add('foo')
>>> b.add('bar')
>>> c.remove('foo') # TwoPhaseSet will raise an exception here

# Cache layer that merges all replicas before returning the read response. 
# To do this over the wire:
# 1) to_json() to serialize
# 2) json.loads() to deserialize
# 3) and from_dict() to instantiate object again
>>> d = a.clone()

>>> d.merge(b)
>>> d.merge(c)

>>> d.to_list()

# if d is TwoPhaseSet, to_list() will return ['foo', 'bar']
#    d is LWWSet,      to_list() will return ['bar']
# for ORSet,           to_list() will return ['foo', 'bar']
```


### Running tests

```
$ python -m unittest discover -s tests -p '*_test.py'
```

### Resources

- [The paper that introduced CRDTs](https://hal.inria.fr/file/index/docid/555588/filename/techreport.pdf) and [the morning paper entry](https://blog.acolyer.org/2015/03/18/a-comprehensive-study-of-convergent-and-commutative-replicated-data-types/) on it
- [Readings in conflict-free replicated data types](http://christophermeiklejohn.com/crdt/2014/07/22/readings-in-crdts.html) should cover pretty much everything else in terms of theory.
- If you prefer watching talks like me:
  - [Consistency without consensus in production systems](https://www.youtube.com/watch?v=em9zLzM8O7c) by Peter Bourgon is the talk that got me excited about CRDTs because of their practical applications.
  - [CRDTs Illustrated](https://www.youtube.com/watch?v=9xFfOhasiOE) by Arnout Engelen is also acts as a good companion to the paper.
  - In [Practical Demystification of CRDT](https://www.youtube.com/watch?v=PQzNW8uQ_Y4), Dmitry Ivanov & Nami Naserazad discuss pros & cons of a few of the CRDTs and some practical implementation issues.
- Other CRDT projects:
  - [Meangirls](https://github.com/aphyr/meangirls) in Ruby
  - [Knockbox](https://github.com/reiddraper/knockbox) in Clojure
  - [Akka CRDT](https://github.com/jboner/akka-crdt) for Akka
  - [Roshi](https://github.com/soundcloud/roshi) An LWW-element-set based implementation by SoundCloud
