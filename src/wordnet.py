from typing import List, Literal
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset
from nltk import download as nltk_download

nltk_download('omw-1.4', quiet=True)
nltk_download('wordnet', quiet=True)

def make_sns_str(lem: str, pos: str, sense: int) -> str:
    ''' Formats a wordnet-style synset string'''
    if sense > 9:
        return f'{lem}.{pos}.{sense}'
    else:
        return f'{lem}.{pos}.0{sense}'


def get_sns_context(synset: Synset) -> List[str]:
    ''' Get the definition and example(s) from a synset'''
    context = []
    if definition := synset.definition():
        context.append(definition)

    if examples := synset.examples():
        context.extend(examples)

    return context


def make_wn_context(
    sns: Synset,
    add_hypo: bool = False,
    add_hyper: bool = False
) -> str:
    ''' Combines available wordnet gloss context into a single string'''
    wn_context = get_sns_context(sns)

    if add_hypo:
        if hyponyms := sns.hyponyms():
            for hypo in hyponyms:
                wn_context.extend(get_sns_context(hypo))

    if add_hyper:
        if hypernyms := sns.hypernyms():
            for hyper in hypernyms:
                wn_context.extend(get_sns_context(hyper))

    return '' if not wn_context else '. '.join(wn_context) + '.'


def get_wn_senses(lem: str, pos: Literal['v', 'n', 'a', 'r']) -> List[Synset]:
    """Uses the lemma and POS-tag to retrieve the WordNet senses"""
    pos_dict = {"v": wn.VERB, "n": wn.NOUN, "a": wn.ADJ, "r": wn.ADV}
    senses = wn.synsets(lem, pos=pos_dict[pos])

    return senses
