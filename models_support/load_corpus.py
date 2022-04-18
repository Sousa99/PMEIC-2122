import os
import abc
import gensim
import pickle

from random import random
from typing import List, Optional

# ============================================================ MAIN CLASS DEFINITION ============================================================

class CorpusNotLoaded(abc.ABC):

    @abc.abstractmethod
    def __init__(self) -> None:
        if not os.path.exists('./exports/documents_clean/'):
            exit(f'🚨 The folder \'./exports/documents_clean/\' must exist')

    @abc.abstractmethod
    def __iter__(self):
        pass


class LemmatizedCorpusNotLoaded(CorpusNotLoaded):

    def __init__(self, path_to_corpora_files: str, number_of_documents_to_use: Optional[int] = None) -> None:
        super().__init__()
        
        self.path_to_corpora : str = path_to_corpora_files
        self.filenames : List[str] = os.listdir(path_to_corpora_files)

        if number_of_documents_to_use is not None:
            self.filenames = random.sample(self.filenames, number_of_documents_to_use)

    def __iter__(self):

        for filename in self.filenames:

            file_path = os.path.join(self.path_to_corpora, filename)
            if not os.path.isfile(file_path): continue

            file_save = open(file_path, 'rb')
            lemmatized_filtered : List[str] = pickle.load(file_save)
            file_save.close()
    
            yield lemmatized_filtered

class BOWCorpusNotLoaded(CorpusNotLoaded):

    def __init__(self, path_to_corpora_files: str, dictionary: gensim.corpora.Dictionary, number_of_documents_to_use: Optional[int] = None) -> None:
        super().__init__()

        self.path_to_corpora : str = path_to_corpora_files
        self.dictionary : gensim.corpora.Dictionary = dictionary
        self.filenames : List[str] = os.listdir(path_to_corpora_files)

        if number_of_documents_to_use is not None:
            self.filenames = random.sample(self.filenames, number_of_documents_to_use)

    def __iter__(self):

        for filename in self.filenames:

            file_path = os.path.join(self.path_to_corpora, filename)
            if not os.path.isfile(file_path): continue

            file_save = open(file_path, 'rb')
            lemmatized_filtered : List[str] = pickle.load(file_save)
            file_save.close()

            yield self.dictionary.doc2bow(lemmatized_filtered)

# ============================================================ MAIN FUNCTION DEFINITION ============================================================

def serialize_corpus(corpus: CorpusNotLoaded, path_to_save: str):
    gensim.corpora.MmCorpus.serialize(path_to_save, corpus)

def deserialize_corpus(path_to_corpus: str) -> gensim.corpora.MmCorpus:
    return gensim.corpora.MmCorpus(path_to_corpus)