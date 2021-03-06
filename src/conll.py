import logging
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

# Aliases for nil/none values in the dataset
ROL_NONE = '[]'
SNS_NONE = 'O'
SEM_NONE = 'NIL'


class AnnCategory(Enum):
    ''' Annotation category type (just for ease of use) '''
    TOK = 'tok'
    SYM = 'sym'
    SEM = 'sem'
    CAT = 'cat'
    SNS = 'sns'
    ROL = 'rol'


@dataclass
class ConllTok:
    ''' A ConllTok is a single token with all its annotation layers from the
        Parallel Meaning Bank.
    '''
    tok: str
    sym: str
    sem: str
    cat: str
    sns: str
    rol: str


@dataclass
class ConllDoc:
    ''' A ConllDoc is a document / sentence, in this case with the annotation
        layers from the Parallel Meaning Bank. The annotations are per token
        and might not exist.
    '''
    id: Optional[str]  # Warning: some docs don't have an id in the conll files
    raw_sent: str
    tok: List[str]
    sym: List[str]
    sem: List[str]
    cat: List[str]
    sns: List[str]
    rol: List[str]

    def get_by_token(self, token: str) -> Optional[ConllTok]:
        ''' Get all annotations for a specific token by string.
            Returns None if the token does not exist in the sentence.
        '''
        try:
            return self.get_by_index(self.tok.index(token))
        except ValueError:
            return None

    def get_by_index(self, idx: int) -> Optional[ConllTok]:
        ''' Get all annotations for a specific token by index.
            Returns None if the token does not exist in the sentence.
        '''
        if 0 < idx >= len(self.tok):
            return None

        # Misschien alles direct op token niveau doen?
        return ConllTok(
            tok=self.tok[idx],
            sym=self.sym[idx],
            sem=self.sem[idx],
            cat=self.cat[idx],
            sns=self.sns[idx],
            rol=self.rol[idx],
        )

    def get_category(self, category: AnnCategory) -> List[str]:
        ''' Returns all annotations of a certain category'''
        return getattr(self, category.value)

    def __str__(self) -> str:
        ''' Nicely formatted doc '''
        return '\n'.join((
            'ConllDoc(',
            f'  id: {self.id}',
            f'  raw_sent: {self.raw_sent}',
            f'  tok: {self.tok}',
            f'  sym: {self.sym}',
            f'  sem: {self.sem}',
            f'  cat: {self.cat}',
            f'  sns: {self.sns}',
            f'  rol: {self.rol}',
            ')',
        ))


class ConllDataset:
    ''' A ConllDataset is a collection of ConllDocs. The Docs are essentially
        the rows and the annotation layers the columns, stored in lists.

            tok, sym, sem, cat, sns, rol
        doc1
        doc2
        ...
    '''

    def __init__(self, file_path: str, debug_log: bool = False) -> None:
        self.debug_log = debug_log
        self.docs: List[ConllDoc] = self.__parse_docs(file_path)

    def __parse_docs(self, file_path: str) -> List[ConllDoc]:
        with open(file_path) as f:
            docs = f.read().rstrip().split('\n\n')

        result: List[ConllDoc] = []
        for doc in docs:
            temp_doc = {
                'id': None,
                'raw_sent': None,
                'tok': [],
                'sym': [],
                'sem': [],
                'cat': [],
                'sns': [],
                'rol': [],
            }
            # This is done in order to ensure we don't overwrite an id if a
            # sentence / line contains this exact string for some reason.
            found_id, found_sent = False, False
            for line in doc.split('\n'):
                if line.startswith('#'):
                    if not found_id and 'newdoc id' in line:
                        temp_doc['id'] = line.split(' = ')[-1]
                        found_id = True
                    elif not found_sent and 'raw sent' in line:
                        temp_doc['raw_sent'] = line.split(' = ')[-1]
                        found_sent = True
                else:
                    # Sanity check.
                    items = line.split('\t')
                    assert len(items) == 7, "Error in doc %s" % temp_doc['id']

                    # tok:gold is in there two times for some reason?
                    # That is why it is ignored here.
                    tok, _, sym, sem, cat, sns, rol = items
                    # assert tok == tok1, "What is different here"

                    # None aliases are defined above.
                    temp_doc['tok'].append(tok)
                    temp_doc['sym'].append(sym)
                    temp_doc['sem'].append(sem if sem != SEM_NONE else None)
                    temp_doc['cat'].append(cat)
                    temp_doc['sns'].append(sns if sns != SNS_NONE else None)
                    temp_doc['rol'].append(rol if rol != ROL_NONE else None)

            if not found_id and self.debug_log:
                logging.warning('No id for doc with sent: %s' %
                                temp_doc['raw_sent'])

            result.append(ConllDoc(**temp_doc))
        return result

    def get_category(self, category: AnnCategory) -> List[List[str]]:
        ''' Returns all annotations of a certain category, this is sort of
            getting the docs by column:

                 |
                 V
                tok, sym, sem, cat, sns, rol
            doc1
            doc2
            ...
        '''
        return [getattr(doc, category.value) for doc in self.docs]

    def get_sents(self) -> List[str]:
        ''' Returns all raw sentences in the dataset '''
        return [doc.raw_sent for doc in self.docs]

    def get_ids(self) -> List[Optional[str]]:
        ''' Returns all document ids in the dataset '''
        return [doc.id for doc in self.docs]

    def __len__(self) -> int:
        return len(self.docs)
