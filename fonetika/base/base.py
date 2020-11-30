import re

from abc import ABC, abstractmethod


class BasePhoneticsAlgorithm(ABC):
    _vowels = ''
    __reduce_regex = re.compile(r'(\w)(\1)+', re.I)
    __cyrillic2latin_table = str.maketrans('АВЕСКМОТРХУаескопртху', 'ABECKMOTPXYaeckonpmxy')
    __latin2cyrillic_table = str.maketrans('ABECKMOTPXYaeckonpmxy', 'АВЕСКМОТРХУаескопртху')

    def _reduce_seq(self, seq):
        """
        Reduces several repeated symbols in a given string
        :param seq: string
        :return: reduced string
        """
        return self.__reduce_regex.sub(r'\1', seq)

    def _cyrillic2latin(self, seq):
        """
        Converts all cyrillic letters into latin
        :param seq: string
        :return: updated string
        """
        return seq.translate(self.__cyrillic2latin_table)

    def _latin2cyrillic(self, seq):
        """
        Converts all latin letters into cyrillic
        :param seq: string
        :return: updated string
        """
        return seq.translate(self.__latin2cyrillic_table)

    @abstractmethod
    def transform(self, word):
        """
        Converts a given word to phonetic code
        :param word: string
        :return: string code
        """
        return None
