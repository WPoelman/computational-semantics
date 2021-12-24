import sys

from src.conll import ConllDataset


def main():
    # Dit is een voorbeeld scriptje om de dataset te gebruiken.
    # argv[1] is het pad naar het dataset bestandje.
    dataset = ConllDataset(sys.argv[1])
    
    print(f'\nLoaded {len(dataset)} documents\n')
    print(f'First doc: {dataset.docs[0]}\n')

    for doc in dataset.docs[6:7]:
        tok_str = doc.tok[2]
        print(f'Labels {doc.id} second token: {doc.get_by_index(1)}')
        print(f'Labels {doc.id} third token:  {doc.get_by_token(tok_str)}\n')
    

if __name__ == '__main__':
    main()
