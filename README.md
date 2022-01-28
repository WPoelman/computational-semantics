# Final Project
Final project for the master's course Computational Semantics at the University of Groningen.

## Description
We have implemented a word sense disambiguation system.
We approached the problem as a sentence-pair classification task where the model has to compare the context from the target sentence and gloss information from Wordnet, such as the definition and / or example sentences.

We assume the lemma and part-of-speech tag are given and the model predicts the sense number.
### Data
The data we have used originally comes from the [Parallel Meaning Bank](https://pmb.let.rug.nl/) project.
We used a parsed subset of this data from here: <https://github.com/RikVN/DRS_parsing/tree/master/parsing/layer_data/4.0.0>.

## Installation
1. (Optional) create and activate a virtual environment (tested with python 3.8)
2. Install dependencies with `pip install -r requirements.txt`
3. Download our best model from here **add link** if you want to use it

## Usage
All our systems output a `.pickle` file with predictions that can be evaluated with the `evaluate.py` script.

We provide two baselines: `always_first_baseline.py` and `statistical_baseline.py`.
The `system.py` script is used to train the sentence classification model with various options and generate predictions for it.

As an example, the statistical baseline can be used on the development set as follows:

```bash
python always_first_baseline.py -d dev
```

Next, evaluate the system performance. As an example, evaluating the baseline predictions generated in the previous step on the development set can be done as follows:

```bash
python evaluate.py -e data/dev.conll -p results/baseline_predictions_dev.pickle
```

All scripts provide a `--help` argument to see what arguments they accept.

## TODO - done
- [x] Model trainen (eerste systeem trainen)
- [x] Evaluatie van dataset ipv per zin (macro / micro F1) (per woord)
- [x] Baseline description aanvullen & overbodige comments weghalen
- [x] Baseline todo overwegen: als er een WN result is, wellicht gewoon lemma & postag overnemen van gold en er handmatig 01 achter plakken. Of wel huidige code houden. (als we evaluatie van documenten hebben, dan even kijken of dit veel verschil geeft of dat het enkele uitzonderingen zijn)
- [x] Report begin maken (baseline, onderzoeksvraag, taak etc.)
- [x] Literatuur checken
- [x] Data variaties verzinnen (voorbeelden: met n aantal hypernymen en of hyponymen, met of zonder definitie, met pmb zinnen erbij of niet, zij-relaties)
- [x] Kijken of we nltk.download('wordnet') en nltk.download('omw-1.4') nog moeten automatiseren of niet

## TODO - programming / running experiments
- [ ] Model trainen op context van 'zijrelaties' (hyponyms of hypernym)
- [ ] Beste model (=hoogste scores op dev): trainen op meerdere epochs, evt. model anders tweaken
- [ ] Testscores genereren (welke modellen precies? allemaal of alleen de beste?)
- [x] Analysescript schrijven
- [ ] Analysescript toepassen op gegenereerde test output van beste model
- [ ] Beste model: pre-trained model uploaden / downloadbaar maken (in readme installation zetten)


## TODO - administrative / cleaning up / writing
- [x] Als we het uiteindelijke model hebben, uitleggen hoe te gebruiken (README bijwerken)
- [x] De commands in de ReadMe checken (bijv of het klopt nu 'dev' naar 'data/dev.conll' is aangepast)
- [ ] Methode herschrijven: voorbeelden data toevoegen & evaluatie meer in literatuur betrekken
- [ ] Analyse maken m.b.v. script
- [ ] Alles herschrijven voor stijl en cohesie


## Authors
* Frank van den Berg
* Esther Ploeger
* Wessel Poelman
