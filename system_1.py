#!/usr/bin/env python

"""
Filename:   baseline.py
Date:       2-1-2022
Authors:    Wessel Poelman, Esther Ploeger, Frank van den Berg
Description:
    A first system that performs Word Sense Disambiguation
    by approaching it as a sentence(actually: text)-pair classification task
    .
"""

import argparse

from src.conll import SNS_NONE, ConllDataset
from baseline import get_wn_sense

from simpletransformers.classification import ClassificationModel, ClassificationArgs
import pandas as pd
import logging
import pickle
import torch


# Disable logging to get cleaner output
logger = logging.getLogger()
logger.disabled = True


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--train_file", default='./data/train.conll', type=str,
                        help="Location of training file")
    parser.add_argument("-p", "--prediction_file", default='./data/dev.conll', type=str,
                        help="Location of training file")
    parser.add_argument("-o", "--outfile", default='./data/output_s1.pickle', type=str,
                        help="Location of training file")

    args = parser.parse_args()
    return args


def prepare_train(conll_data):
    """Prepare training data to be in a useful format for text-pair classification"""
    data = []

    for doc in conll_data.docs:
        sns = doc.sns
        tok = doc.tok
        pmb_context = " ".join(tok)
        for syn in sns:
            if syn == SNS_NONE:
                # We can not predict the correct sense number for these words
                pass
            else:
                # Look up all possible synsets (senses) for this lemma and POS
                lem = syn.split(".")[0]
                pos = syn.split(".")[1]
                senses = get_wn_sense(lem, pos)

                for sense in senses:
                    sense_text = str(sense)[8:-2]
                    # Get definitions and example sentences from WordNet gloss
                    if sense.examples() or sense.definition():
                        wn_context = sense.definition() + " . " + " . ".join(sense.examples())
                    else:
                        wn_context = ""

                    # For correct synsets, add label 1 and add 0 for incorrect ones
                    if syn == sense_text:
                        data.append([pmb_context, wn_context, 1])
                    else:
                        data.append([pmb_context, wn_context, 0])

    return data


def predict_synset(tok, syn, model):
    """ Predict an individual synset """
    data = []
    pmb_context = " ".join(tok)

    # Look up all possible synsets (senses) for this lemma and POS
    lem = syn.split(".")[0]
    pos = syn.split(".")[1]
    senses = get_wn_sense(lem, pos)

    for sense in senses:
        # Get definitions and example sentences from WordNet gloss
        if sense.examples() or sense.definition():
            wn_context = sense.definition() + " . " + " . ".join(sense.examples())
        else:
            wn_context = ""

        # Add list containing both contexts to file
        data.append([pmb_context, wn_context])

    # Predict correct synset
    predictions, raw_outputs = model.predict(data)
    prob_1 = [r[1] for r in raw_outputs]
    sense_num_most_probable = str(prob_1.index(max(prob_1)) + 1)

    return lem + "." + pos + "." + "0" + sense_num_most_probable


def predict(to_predict_file, model):
    """ Predict all synsets from a file """
    all_predictions = []
    for doc in to_predict_file.docs:
        doc_pred = []
        sns = doc.sns
        tok = doc.tok
        for syn in sns:
            if syn == SNS_NONE:
                # We can not predict the correct sense number for these words
                pass
            else:
                doc_pred.append(predict_synset(tok, syn, model))

        all_predictions.append(doc_pred)

    return all_predictions


def main():

    if not torch.cuda.is_available():
        print('No gpu available!')
        exit(1)

    args = create_arg_parser()

    # Load input files
    train_file = ConllDataset(args.train_file)
    prediction_file = ConllDataset(args.prediction_file)

    # Prepare train set
    train_df = pd.DataFrame(prepare_train(train_file))
    train_df.columns = ["text_a", "text_b", "labels"]

    # Define and train model
    model_args = ClassificationArgs()
    model_args.evaluation_strategy="steps"
    model_args.eval_steps=1000
    model_args.save_steps=5000
    model_args.per_device_train_batch_size=8
    model_args.per_device_eval_batch_size=8
    model_args.num_train_epochs=1
    model_args.seed=0
    model_args.load_best_model_at_end=True
    model_args.disable_tqdm=True
    model_args.use_early_stopping = True
    model_args.early_stopping_delta = 0.01
    model_args.early_stopping_metric = "mcc"
    model_args.early_stopping_metric_minimize = False
    model_args.early_stopping_patience = 1
    model_args.evaluate_during_training_steps = 1000

    model = ClassificationModel("bert", "bert-base-uncased", args=model_args)
    model.train_model(train_df)

    # Predict synsets
    predictions = predict(prediction_file, model)

    # Write results to pickle file
    with open(args.outfile, 'wb') as pred_file:
        pickle.dump(predictions, pred_file)
    print("Predictions have been written to file: " + args.outfile)


if __name__ == "__main__":
    main()
