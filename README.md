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
3. Download our best model from [here](https://drive.google.com/drive/folders/17uEFmE4vIzgVidxFCFQbvmDRvDerPeTi?usp=sharing) if you want to use it (huggingface transformers style model)

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

## Authors
* Frank van den Berg
* Esther Ploeger
* Wessel Poelman
