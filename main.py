import sys

from src.conll import ConllDataset


def main():
    # Dit is een voorbeeld scriptje om de dataset te gebruiken.
    # argv[1] is het pad naar het dataset bestandje.
    dataset = ConllDataset(sys.argv[1])
    print(f'\nLoaded {len(dataset)} documents, showing first 2:\n')
    for doc in dataset.docs[:2]:
        print(doc)


if __name__ == '__main__':
    main()
