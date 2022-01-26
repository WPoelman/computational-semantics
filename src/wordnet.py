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


def make_wn_context(
    sense: Synset,
    add_hypo: bool = False,
    add_hyper: bool = False
) -> str:
    ''' Combines available wordnet gloss context into a single string'''
    wn_context = ''

    if definition := sense.definition():
        wn_context += definition + ' . '

    if examples := sense.examples():
        wn_context += ' . '.join(examples)

    # TODO: het was even zoeken wat een logische plek hiervoor was. We kunnen
    # elke keer dat we deze aanroepen kijken hoe we de context willen gebruiken
    # dan weet je (hopelijk) zeker dat het tussen train / pred niet verkeerd
    # gaat.
    if add_hypo:
        assert False, 'Add hypo is not implemented yet!'

    if add_hyper:
        assert False, 'Add hyper is not implemented yet!'

    return wn_context


def get_wn_senses(lem: str, pos: Literal['v', 'n', 'a', 'r']) -> List[Synset]:
    """Uses the lemma and POS-tag to retrieve the WordNet senses"""
    pos_dict = {"v": wn.VERB, "n": wn.NOUN, "a": wn.ADJ, "r": wn.ADV}
    senses = wn.synsets(lem, pos=pos_dict[pos])

    return senses
