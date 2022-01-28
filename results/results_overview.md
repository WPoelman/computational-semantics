## Summary of results for every experiment ##

This data can be put into a LaTeX table later on. Here, we simply list the outputs gathered for runs of the model on separate train data sets, in order to keep an overview (to avoid confusion due to having a separate evaluation script).

E = Example sentences, D = Definitions

## Dev results

### BASELINE 1: Always predicting the first synset (dev) ###


|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  0.5863069335654192 	| 
|  Acc. per sentence 	|  0.5986000051755811 	|   
|   Fully correct sent.	|  0.25979557069846676 	|   

### BASELINE 2: Statistical (dev) ###


|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  0.8378299970989266 	| 
|  Acc. per sentence 	|  0.8345881038024489 	|   
|   Fully correct sent.	|  0.6039182282793867 	|   


### SYSTEM 1: Trained on D and E of sentence tokens (dev) ###
|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  0.856396866840731 	| 
|  Acc. per sentence 	|  0.8468175410318867 	|   
|   Fully correct sent.	| 0.6405451448040886  	|   


### SYSTEM 1a: Trained on D only of sentence tokens (dev) ###
|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  0.8436321438932405 	| 
|  Acc. per sentence 	|  0.8353503006150307 	|   
|   Fully correct sent.	|  0.610732538330494 	|   

### SYSTEM 1b: Trained on E only of sentence tokens (dev) ###
|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|   0.6341746446185088 	| 
|  Acc. per sentence 	|  0.6401134684653035 	|   
|   Fully correct sent.	|  0.2972742759795571 	|   


### SYSTEM 2: Trained on D and E of sentence tokens + D and E of hyponyms (dev) ###
|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  0.8648099796924862 	| 
|  Acc. per sentence 	|   0.8566402095864084 	|   
|   Fully correct sent.	|  0.6575809199318569 	|   

### SYSTEM 3: Trained on D and E of sentence tokens + D and E of hypernyms (dev) ###
|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  0.8511749347258486 	| 
|  Acc. per sentence 	|  0.8430606849266102 	|   
|   Fully correct sent.	|  0.6252129471890971 	|   


### SYSTEM 4: Trained on D and E of sentence tokens + D and E of hyponyms and hypernyms (dev) ###
|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	| 0.8616187989556136  	| 
|  Acc. per sentence 	|  0.8535262962675424 	|   
|   Fully correct sent.	|  0.6575809199318569 	|   

 ### SYSTEM 5: Best system (=DE,words+hypo) with threshold ###
|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  TBD 	| 
|  Acc. per sentence 	|  TBD 	|   
|   Fully correct sent.	|  TBD 	|   

---

## Test results

### BASELINE 1: Always predicting the first synset (test) ###


|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  58.9%	| 
|  Acc. per sentence 	|  59.6% 	|   
|   Fully correct sent.	|  23.2% 	|   

### BASELINE 2: Statistical (test) ###


|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  84.5% 	| 
|  Acc. per sentence 	|  84.7% 	|   
|   Fully correct sent.	|  60.0% 	|  

 ### SYSTEM 2: Best model (=DE,words+hypo) (test) ###
|  Eval. type 	|   Score	|  
|---	|---	|
|  Acc. synsets 	|  86.9% 	| 
|  Acc. per sentence 	|  86.4% 	|   
|   Fully correct sent.	|  64.8% 	|   

