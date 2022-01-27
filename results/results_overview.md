## Summary of results for every experiment ##

This data can be put into a LaTeX table later on. Here, we simply list the outputs gathered for runs of the model on separate train data sets, in order to keep an overview (to avoid confusion due to having a separate evaluation script).

E = Example sentences, D = Definitions

### BASELINE 1: Always predicting the first synset ###


*** MICRO: EVALUATION ON SYNSET LEVEL ***

Correct synsets (accuracy): 0.5863069335654192


*** MICRO: EVALUATION ON SENTENCE LEVEL ***

Mean number of correct synsets (accuracy) per sentence: 0.5986000051755811

Fully correct sentences (accuracy): 0.25979557069846676

 <br />
 
### BASELINE 2: Statistical ###


*** MICRO: EVALUATION ON SYNSET LEVEL ***

Correct synsets (accuracy): 0.8378299970989266


*** MICRO: EVALUATION ON SENTENCE LEVEL ***

Mean number of correct synsets (accuracy) per sentence: 0.8345881038024489

Fully correct sentences (accuracy): 0.6039182282793867

 <br /> 


### SYSTEM 1: Trained on D and E of sentence tokens ###

*** MICRO: EVALUATION ON SYNSET LEVEL ***

Correct synsets (accuracy): 0.856396866840731

 <br />

*** MACRO: EVALUATION ON SENTENCE LEVEL ***

Mean number of correct synsets (accuracy) per sentence: 0.8468175410318867

Fully correct sentences (accuracy): 0.6405451448040886

 <br />
 

### SYSTEM 1a: Trained on D only of sentence tokens ###

*** MICRO: EVALUATION ON SYNSET LEVEL ***

Correct synsets (accuracy): 0.8436321438932405


*** MICRO: EVALUATION ON SENTENCE LEVEL ***

Mean number of correct synsets (accuracy) per sentence: 0.8353503006150307

Fully correct sentences (accuracy): 0.610732538330494

 <br /> 

### SYSTEM 1b: Trained on E only of sentence tokens ###

 <br /> 

### SYSTEM 2: Trained on D and E of sentence tokens + D and E of hyponyms ###


*** MICRO: EVALUATION ON SYNSET LEVEL ***

Correct synsets (accuracy): 0.8648099796924862


*** MACRO: EVALUATION ON SENTENCE LEVEL ***

Mean number of correct synsets (accuracy) per sentence: 0.8566402095864084

Fully correct sentences (accuracy): 0.6575809199318569

 <br /> 


### SYSTEM 3: Trained on D and E of sentence tokens + D and E of hypernyms ###

********** EVALUATION **********

*** MICRO: EVALUATION ON SYNSET LEVEL ***

Correct synsets (accuracy): 0.8511749347258486

*** MACRO: EVALUATION ON SENTENCE LEVEL ***

Mean number of correct synsets (accuracy) per sentence: 0.8430606849266102

Fully correct sentences (accuracy): 0.6252129471890971


 <br /> 


### SYSTEM 4: Trained on D and E of sentence tokens + D and E of hyponyms and hypernyms ###

*** MICRO: EVALUATION ON SYNSET LEVEL ***

Correct synsets (accuracy): 0.8616187989556136


*** MACRO: EVALUATION ON SENTENCE LEVEL ***

Mean number of correct synsets (accuracy) per sentence: 0.8535262962675424

Fully correct sentences (accuracy): 0.6575809199318569

 <br /> 
 
 ### SYSTEM 5: Trained on D and E of sentence tokens + D and E of words in same hierarchical place (hyponyms of hypernym) ###

TBD
