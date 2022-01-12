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

import pickle
import argparse
from nltk.corpus import wordnet as wn
from src.conll import SNS_NONE, ConllDataset


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", default='dev', type=str,
                        help="Type of data set: train, dev, eval or test")

    args = parser.parse_args()
    return args

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
                # Check whether the lemma is in the list of all lemmas
                # todo: Wellicht als er een Wordnet resultaat is gewoon altijd ervoor
                #  kiezen om gewoon lemma.pos.01 te voorspellen ipv deze moeilijke code,
                #  maar ik weet niet wat het eerlijkst is tegenover ons eindsysteem
                if lem in senses[0].lemma_names() \
                        or lem.capitalize() in senses[0].lemma_names() \
                        or lem.upper() in senses[0].lemma_names():
                    sense = lem + "." + pos + ".01"
                    predictions.append(sense)
                else:
                    predictions.append(senses[0].name())
            else:
                predictions.append(SNS_NONE)

    return predictions


def get_wn_sense(lem, pos):
    """Uses the lemma and POS-tag to retrieve the WordNet senses"""
    pos_dict = {"v": wn.VERB, "n": wn.NOUN, "a": wn.ADJ, "r": wn.ADV}
    senses = wn.synsets(lem, pos=pos_dict[pos])

    return senses


def main():

    # Load data set
    args = create_arg_parser()
    if args.dataset in ["dev", "eval", "test", "train"]:
        dataset = ConllDataset("data/" + args.dataset + ".conll")
    else:
        raise ValueError("The evaluation set must be specified as one of the following: 'dev', 'eval', 'test', 'train'")

    # Print size and an example of the data
    print(f'\nLoaded {len(dataset)} documents\n')
    print(f'First doc: {dataset.docs[0]}\n')

    # Predict senses for each document
    predictions = [baseline(doc.sns) for doc in dataset.docs]

    # Write results to pickle file
    with open('results/baseline_predictions_' + args.dataset + '.pickle', 'wb') as pred_file:
        pickle.dump(predictions, pred_file)
    print("Predictions have been written to file: 'results/baseline_predictions_" + args.dataset + ".pickle")


if __name__ == '__main__':
    main()
