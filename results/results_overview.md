## Summary of results for every experiment ##

This data can be put into a LaTeX table later on. Here, we simply list the outputs gathered for runs of the model on separate train data sets, in order to keep an overview (to avoid confusion due to having a separate evaluation script).

E = Example sentences, D = Definitions

### BASELINE 1: Always predicting the first synset ###


|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  0.5863069335654192 	| 
|  Acc. per sentence 	|  0.5986000051755811 	|   
|   Fully correct sent.	|  0.25979557069846676 	|   

### BASELINE 2: Statistical ###


|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  0.8378299970989266 	| 
|  Acc. per sentence 	|  0.8345881038024489 	|   
|   Fully correct sent.	|  0.6039182282793867 	|   


### SYSTEM 1: Trained on D and E of sentence tokens ###
|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  0.856396866840731 	| 
|  Acc. per sentence 	|  0.8468175410318867 	|   
|   Fully correct sent.	| 0.6405451448040886  	|   


### SYSTEM 1a: Trained on D only of sentence tokens ###
|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  0.8436321438932405 	| 
|  Acc. per sentence 	|  0.8353503006150307 	|   
|   Fully correct sent.	|  0.610732538330494 	|   

### SYSTEM 1b: Trained on E only of sentence tokens ###
|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|   0.6341746446185088 	| 
|  Acc. per sentence 	|  0.6401134684653035 	|   
|   Fully correct sent.	|  0.2972742759795571 	|   


### SYSTEM 2: Trained on D and E of sentence tokens + D and E of hyponyms ###
|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  0.8648099796924862 	| 
|  Acc. per sentence 	|   0.8566402095864084 	|   
|   Fully correct sent.	|  0.6575809199318569 	|   

### SYSTEM 3: Trained on D and E of sentence tokens + D and E of hypernyms ###
|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  0.8511749347258486 	| 
|  Acc. per sentence 	|  0.8430606849266102 	|   
|   Fully correct sent.	|  0.6252129471890971 	|   


### SYSTEM 4: Trained on D and E of sentence tokens + D and E of hyponyms and hypernyms ###
|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	| 0.8616187989556136  	| 
|  Acc. per sentence 	|  0.8535262962675424 	|   
|   Fully correct sent.	|  0.6575809199318569 	|   

 
 ### SYSTEM 5: Trained on D and E of sentence tokens + D and E of words in same hierarchical place (hyponyms of hypernym) ###
|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  TBD 	| 
|  Acc. per sentence 	|  TBD 	|   
|   Fully correct sent.	|  TBD 	|   

 ### SYSTEM 5: System with threshold ###
|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  TBD 	| 
|  Acc. per sentence 	|  TBD 	|   
|   Fully correct sent.	|  TBD 	|   

