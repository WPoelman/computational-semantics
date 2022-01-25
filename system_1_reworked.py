#!/usr/bin/env python

"""
Filename:   system_1.py
Date:       25-01-2022
Authors:    Wessel Poelman, Esther Ploeger, Frank van den Berg
Description:
    A first system that performs Word Sense Disambiguation
    by approaching it as a sentence(actually: text)-pair classification task.
"""

import argparse
import pickle
from typing import Any, List

import pandas as pd
import torch
from nltk.corpus.reader.wordnet import Synset
from simpletransformers.classification import (ClassificationArgs,
                                               ClassificationModel)

from src.conll import AnnCategory, ConllDataset
from src.wordnet import get_wn_senses, make_sns_str, make_wn_context


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--train_file", default='./data/train.conll', type=str,
                        help="Location of training file")
    parser.add_argument("-p", "--prediction_file", default='./data/dev.conll', type=str,
                        help="Location of training file")
    parser.add_argument("-o", "--outfile", default='./data/output_s1.pickle', type=str,
                        help="Location of training file")
    parser.add_argument('--add_hypo', action='store_true',
                        help='Adds hyponym gloss information to context.')
    parser.add_argument('--add_hyper', action='store_true',
                        help='Adds hypernym gloss information to context.')

    args = parser.parse_args()
    return args


def prepare_sense_data(
    syn: Synset,
    pmb_context: str,
    add_hypo: bool = False,
    add_hyper: bool = False,
    with_labels: bool = False
) -> List[List[Any]]:
    """Prepare data to be in a useful format for text-pair classification"""
    data = []

    # Look up all possible synsets (senses) for this lemma and POS
    lem, pos, _ = syn.split(".")
    senses = get_wn_senses(lem, pos)

    for sense in senses:
        # Get definitions and example sentences from WordNet gloss
        wn_context = make_wn_context(sense, add_hypo, add_hyper)

        # For correct synsets, add label 1 and add 0 for incorrect ones
        if with_labels:
            data.append([
                pmb_context,
                wn_context,
                1 if syn == sense._name else 0
            ])
        else:
            data.append([pmb_context, wn_context])
    return data


def prepare_train(
    conll_data: ConllDataset,
    add_hypo: bool = False,
    add_hyper: bool = False
) -> List[List[Any]]:
    """Prepare training data to be in a useful format for text-pair classification"""
    data = []

    for doc in conll_data.docs:
        pmb_context = doc.raw_sent
        for syn in doc.get_category(AnnCategory.SNS):
            if not syn:
                continue
            # We need a flat list here, not per document!
            data.extend(
                prepare_sense_data(
                    syn, pmb_context, add_hypo, add_hyper, with_labels=True
                )
            )
    return data


def predict(
    to_predict_file: ConllDataset,
    model: ClassificationModel,
    add_hypo: bool = False,
    add_hyper: bool = False
):
    """ Predict all synsets from a file """
    all_predictions = []
    for doc in to_predict_file.docs:
        doc_pred = []
        pmb_context = doc.raw_sent
        for syn in doc.get_category(AnnCategory.SNS):
            # Not sure if this is a good idea, but otherwise we risk ending up
            # with different sized lists at prediction time.
            if not syn:
                doc_pred.append(None)
                continue

            lem, pos, _ = syn.split(".")
            context = prepare_sense_data(syn, pmb_context, add_hypo, add_hyper)

            # Predict correct synset
            _, raw_outputs = model.predict(context)
            prob_1 = [r[1] for r in raw_outputs]
            sense_num_most_probable = prob_1.index(max(prob_1)) + 1
            sense_num_most_probable = 1

            sense_id = make_sns_str(lem, pos, sense_num_most_probable)
            doc_pred.append(sense_id)

        all_predictions.append(doc_pred)

    return all_predictions


def main():
    # if not torch.cuda.is_available():
    #     print('No gpu available!')
    #     exit(1)

    args = create_arg_parser()

    # Load input files
    train_file = ConllDataset(args.train_file)
    prediction_file = ConllDataset(args.prediction_file)
    prepared_dataset = prepare_train(
        train_file, add_hypo=args.add_hypo, add_hyper=args.add_hyper
    )

    # Prepare train set
    train_df = pd.DataFrame(prepared_dataset)
    train_df.columns = ["text_a", "text_b", "labels"]

    # Define and train model
    model_args = ClassificationArgs()
    model_args.evaluation_strategy = "steps"
    model_args.eval_steps = 1000
    model_args.save_steps = 5000
    model_args.per_device_train_batch_size = 8
    model_args.per_device_eval_batch_size = 8
    model_args.num_train_epochs = 1
    model_args.seed = 0
    model_args.load_best_model_at_end = True
    model_args.disable_tqdm = True
    model_args.use_early_stopping = True
    model_args.early_stopping_delta = 0.01
    model_args.early_stopping_metric = "mcc"
    model_args.early_stopping_metric_minimize = False
    model_args.early_stopping_patience = 1
    model_args.evaluate_during_training_steps = 1000

    model = ClassificationModel("bert", "bert-base-uncased", args=model_args)
    model.train_model(train_df)

    # Predict synsets
    predictions = predict(prediction_file, None)

    # Write results to pickle file
    with open(args.outfile, 'wb') as pred_file:
        pickle.dump(predictions, pred_file)
    print("Predictions have been written to file: " + args.outfile)


if __name__ == "__main__":
    main()
