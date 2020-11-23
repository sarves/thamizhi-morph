## FST Models for Verbs:

- erbs-c3.fst: model for class 3
- verbs-c4.fst: model for class 4
- verbs-c62.fst: model for class 62
- verbs-c11.fst: model for class 11
- verbs-c12.fst: model for class 12
- verb-rest.fst: model for the rest of the classes
  
  > Note: Because of the orgthographical rule conflect among some of these classes, 
  we had to make them are separate classes. However, 
  from the computational point of view, this is not a problem. 
  You need to just iterate through these these models.
  
- verb-guesses.fst: model for morphological guesser 
  > Note: You need to use this after checking a word with all other verbal models listed above.

## FST Models for nouns:
  - nouns.fst: the model for noun morphological analyser
  - noun-guesser.fst: a guesser for noun morphology
  
  You can see how these can be used in your applications here: fomafst.github.io
  These models are compiled according to the foma specifications given in the website.
