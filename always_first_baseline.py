#!/usr/bin/env python

"""
Filename:   baseline.py
Date:       25-01-2022
Authors:    Wessel Poelman, Esther Ploeger, Frank van den Berg
Description:
    A baseline for the task of Word Sense Disambiguation that takes
    tokens with their lemma and pos-tags and predicts the sense.
    The predicted sense is always the first returned sense from
    Wordnet, if any Wordnet entry can be found.
"""

import argparse
import pickle

from src.conll import AnnCategory, ConllDataset
from src.wordnet import get_wn_senses, make_sns_str


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", default='dev', type=str,
                        help="Type of data set: train, dev, eval or test",
                        choices=["dev", "eval", "test", "train"])
    args = parser.parse_args()
    return args


def baseline(sns):
    """Uses the synsets for extracting the lemma and pos-tag, then
    always predicts the first sense: e.g. extracts 'cloud' and 'n'
    from 'cloud.n.02' and then predicts cloud.n.01"""
    predictions = []

    for syn in sns:
        # This is done so we always end up with the same number of items per
        # list (predictions and actual dataset).
        if not syn:
            predictions.append(None)
            continue

        # Get the first sense from WordNet as our prediction
        lem, pos, _ = syn.split(".")
        senses = get_wn_senses(lem, pos)
        if not senses:
            print(f'No Wordnet entry found for: {syn}')
            predictions.append('NO WORDNET ENTRY FOUND')
            continue

        # Check whether the lemma is in the list of all lemmas
        lemma_names = {l.lower() for l in senses[0].lemma_names()}
        if lem.lower() in lemma_names:
            predictions.append(make_sns_str(lem, pos, 1))
        else:
            predictions.append(senses[0].name())

    return predictions


def main():
    # Load data set
    args = create_arg_parser()
    dataset = ConllDataset("data/" + args.dataset + ".conll")

    print(f'\nLoaded {len(dataset)} documents\n')

    # Predict senses for each document
    predictions = [baseline(sns)
                   for sns in dataset.get_category(AnnCategory.SNS)]

    # Write results to pickle file
    with open('results/baseline_predictions_' + args.dataset + '.pickle', 'wb') as pred_file:
        pickle.dump(predictions, pred_file)
    print("Predictions have been written to file: 'results/baseline_predictions_" +
          args.dataset + ".pickle")


if __name__ == '__main__':
    main()
