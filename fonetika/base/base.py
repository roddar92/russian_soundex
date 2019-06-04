import re

from abc import ABC, abstractmethod


class BasePhoneticsAlgorithm(ABC):
    _vowels = ''
    _reduce_regex = re.compile(r'(\w)(\1)+', re.I)

    def _reduce_seq(self, seq):
        return self._reduce_regex.sub(r'\1', seq)

    @abstractmethod
    def transform(self, word):
        """
        Converts a given word to phonetic code
        :param word: string
        :return: string code
        """
        return None
