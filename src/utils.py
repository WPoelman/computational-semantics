import logging
from typing import Any, Iterable


def accuracy_score(true: Iterable[Any], predicted: Iterable[Any]) -> float:
    ''' Returns the accuracy score between two iterables'''
    if len(true) != len(predicted):
        logging.warning('Provided different length lists for accuracy score')
        return 0

    if not len(true):
        logging.warning('Provided empty lists for accuracy score')
        return 0

    correct = sum(1 if t == p else 0 for t, p in zip(true, predicted))
    total = len(true)

    return correct / total
