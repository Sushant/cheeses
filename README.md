# cheeses [![Build Status](https://travis-ci.org/Sushant/cheeses.svg?branch=master)](https://travis-ci.org/Sushant/cheeses)
CRDTs in Python

Heavily inspired by [Meangirls](https://github.com/aphyr/meangirls)

### Example usage

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
