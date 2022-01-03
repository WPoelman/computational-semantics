#!/usr/bin/env python

"""
Filename:   baseline.py
Date:       2-1-2022
Authors:    Wessel Poelman, Esther Ploeger, Frank van den Berg
Description:
    A baseline for the task of Word Sense Disambiguation that takes
    ...
    .
"""

import sys

from nltk.corpus import wordnet as wn

from src.conll import SNS_NONE, ConllDataset
from src.utils import accuracy_score

# Misschien wat overkill om heel sklearn te installeren hiervoor, als we nog
# meer gaan gebruiken dan kunnen we dit wel toevoegen (sorry, punaise poetsen
# I know I know)
# from sklearn.metrics import accuracy_score


def baseline(sns):
    """Uses the synsets for extracting the lemma and pos-tag, then
    always predicts the first sense: e.g. extracts 'cloud' and 'n'
    from 'cloud.n.02' and then predicts cloud.n.01"""
    predictions = []

    for syn in sns:
        if syn == SNS_NONE:
            # We can not predict the correct sense number for these words
            predictions.append(SNS_NONE)
        else:
            # Get the first sense from WordNet as our prediction
            lem = syn.split(".")[0]
            pos = syn.split(".")[1]
            senses = get_wn_sense(lem, pos)
            if senses:
                predictions.append(senses[0].name())
            else:
                predictions.append(SNS_NONE)

    return predictions


def get_wn_sense(lem, pos):
    """Uses the lemma and POS-tag to retrieve the WordNet senses"""
    pos_dict = {"v": wn.VERB, "n": wn.NOUN, "a": wn.ADJ, "r": wn.ADV}
    senses = wn.synsets(lem, pos=pos_dict[pos])

    return senses


def evaluation(gold, predictions):
    """Uses the gold senses and predictions to calculate the accuracy
    score, but only for actual senses (not for the 'O' cases)"""
    all_senses, all_predictions = [], []

    # First we only extract the actual senses, removing the SNS_NONE senses
    for sense, pred in zip(gold, predictions):
        if sense != SNS_NONE:
            all_senses.append(sense)
            all_predictions.append(pred)

    # Print accuracy score for the remaining cases
    print(f'Accuracy score: {accuracy_score(all_senses, all_predictions)} \n')


def main():
    # Load dataset, where argv[1] is the path to the right file
    dataset = ConllDataset(sys.argv[1])

    print(f'\nLoaded {len(dataset)} documents\n')
    print(f'First doc: {dataset.docs[0]}\n')

    # Predict senses for each document
    for doc in dataset.docs:
        predictions = baseline(doc.sns)
        print(doc.id, doc.tok)
        print(f"Golden synsets: {doc.sns}")
        print(f"Predicted synsets: {predictions}")

        # Evaluation per document
        evaluation(doc.sns, predictions)


if __name__ == '__main__':
    main()
