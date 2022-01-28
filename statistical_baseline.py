#!/usr/bin/env python

"""
Filename:   statistical_baseline.py
Date:       25-01-2022
Authors:    Wessel Poelman, Esther Ploeger, Frank van den Berg
Description:
    A baseline for the task of Word Sense Disambiguation that takes
    tokens with their lemma and pos-tags and predicts the sense.
    It uses the most frequent senses from the PMB gold layer train
    data, and if the sense is not included in this, it predicts
    the first sense from WordNet.
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


def baseline(sns, lookup_dict):
    """Uses the synsets for extracting the lemma and pos-tag, then
    predicts the most frequent sense from the lookup dictionary
    or if this can't be found, predict the first sense """
    predictions = []
    for syn in sns:
        # This is done so we always end up with the same number of items per
        # list (predictions and actual dataset).
        if not syn:
            predictions.append(None)
            continue

        lem, pos, _ = syn.split(".")
        lem_pos = lem + "." + pos
        # Try and get the most frequent sense from the lookup dict:
        if lem_pos in lookup_dict:
            most_freq_sense = max(lookup_dict[lem_pos], key=lookup_dict[lem_pos].get)
            predictions.append(lem_pos+"."+most_freq_sense)

        # Else: take the first sense from WordNet as our prediction
        else:
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


def create_freq_dict(conll_dataset):
    """Creates a nested dictionary with the sense frequencies for each
    lemma, pos-tag combination.
    E.g. {'forget.v': {'02': 1, '04': 2}, 'week.n': {'01': 1}}"""
    sense_frequencies = {}
    for sns in conll_dataset.get_category(AnnCategory.SNS):
        for syn in sns:
            if syn:
                lem, pos, sen = syn.split(".")
                lem_pos = lem+"."+pos
                if lem_pos in sense_frequencies:
                    # Increase frequency count of the specific sense
                    sense_frequencies[lem_pos][sen] = sense_frequencies[lem_pos].get(sen, 0) + 1
                else:
                    # Add lemma & pos-tag to the dictionary
                    sense_frequencies[lem_pos] = {sen: 1}

    return sense_frequencies


def main():
    # Load data set
    args = create_arg_parser()
    dataset = ConllDataset("data/" + args.dataset + ".conll")

    print(f'\nLoaded {len(dataset)} documents\n')

    # Create lookup dictionary with sense frequencies for each
    # lemma, pos-tag combination from the training data
    sense_frequencies = create_freq_dict(ConllDataset("data/train.conll"))

    # Predict senses for each document
    predictions = [baseline(sns, sense_frequencies)
                   for sns in dataset.get_category(AnnCategory.SNS)]

    # Write results to pickle file
    with open('results/statistical_baseline_predictions_' + args.dataset + '.pickle', 'wb') as pred_file:
        pickle.dump(predictions, pred_file)
    print("Predictions have been written to file: 'results/statistical_baseline_predictions_" +
          args.dataset + ".pickle'")


if __name__ == '__main__':
    main()
