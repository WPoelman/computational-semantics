import logging
from dataclasses import dataclass
from typing import List, Optional


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


class ConllDataset:
    ''' A ConllDataset is a collection of Conll Docs.'''

    def __init__(self, file_path: str) -> None:
        self.docs: List[ConllDoc] = self.__parse_docs(file_path)

    @staticmethod
    def __parse_docs(file_path: str) -> List[ConllDoc]:
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
            # sentence / line contains this exact string for some reason
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
                    # Use the assertion to see it for yourself.
                    tok, _, sym, sem, cat, sns, rol = items
                    # assert tok == tok1, "What is different here"

                    # TODO misschien is het fijner werken als we alle
                    # NIL, O, [] e.d. omzetten naar een python None. Nu moet
                    # je maar net weten wat de nil-value is. Voor later.
                    temp_doc['tok'].append(tok)
                    temp_doc['sym'].append(sym)
                    temp_doc['sem'].append(sem)
                    temp_doc['cat'].append(cat)
                    temp_doc['sns'].append(sns)
                    temp_doc['rol'].append(rol)

            if not found_id:
                logging.warning('No id for doc with sent: %s' %
                                temp_doc['raw_sent'])

            result.append(ConllDoc(**temp_doc))
        return result

    def __len__(self) -> int:
        return len(self.docs)
