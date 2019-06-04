from abc import abstractmethod

import editdistance

from .base.base import BasePhoneticsAlgorithm
from .metaphone import Metaphone
from .soundex import Soundex


class PhoneticsException(Exception):
    def __init__(self, msg):
        self.msg = msg


class PhoneticsDistance:
    @staticmethod
    def _hamming(word1, word2):
        if len(word1) != len(word2):
            raise PhoneticsException('For Hamming distance words should be the same length!')
        return sum(a != b for a, b in zip(word1, word2))

    @staticmethod
    def _levenstein(word1, word2):
        return editdistance.eval(word1, word2)

    _distance_metric = {
        'levenstein': _levenstein.__func__,
        'hamming': _hamming.__func__,
    }

    @abstractmethod
    def distance(self, word1, word2):
        """
        Compute the distance between phonetics codes
        :param word1: first original word
        :param word2: second original word
        :return: distance value
        """
        return None


class PhoneticsInnerLanguageDistance(PhoneticsDistance):
    def __init__(self, phonetics, metric_name='levenstein', metrics=None):
        """
        Init a distance object
        :param phonetics: an object of BasePhoneticsAlgorithm class
        :param metric_name: distance function name, optional, default is Levenstein distance
        :param metrics: another distance function, optional
        """
        assert isinstance(phonetics, BasePhoneticsAlgorithm)
        assert metric_name in self._distance_metric.keys()
        self.phonetics = phonetics

        if not metrics:
            self.metrics = self._distance_metric[metric_name]
        else:
            self.metrics = metrics

    def distance(self, word1, word2):
        """
        Compute the distance between phonetics codes
        :param word1: first original word
        :param word2: second original word
        :return: distance value
        """
        w1, w2 = self.phonetics.transform(word1), self.phonetics.transform(word2)
        if isinstance(self.phonetics, Soundex):
            return self.metrics(w1, w2) if self.phonetics.is_delete_first_letter() else self.metrics(w1[1:], w2[1:])
        return self.metrics(w1, w2)


class PhoneticsBetweenLanguagesDistance(PhoneticsDistance):
    def __init__(self, phonetics1, phonetics2, metric_name='levenstein', metrics=None):
        """
        Init a distance object
        :param phonetics1: first object of BasePhoneticsAlgorithm class
        :param phonetics2: second object of BasePhoneticsAlgorithm class
        :param metric_name: distance function name, optional, default is Levenstein distance
        :param metrics: another distance function, optional
        """
        assert (isinstance(phonetics1, Soundex) and isinstance(phonetics2, Soundex) or
                isinstance(phonetics1, Metaphone) and isinstance(phonetics2, Metaphone))
        assert metric_name in self._distance_metric.keys()
        self.phonetics1 = phonetics1
        self.phonetics2 = phonetics2

        if not metrics:
            self.metrics = self._distance_metric[metric_name]
        else:
            self.metrics = metrics

    def distance(self, word1, word2):
        """
        Compute the distance between phonetics codes
        :param word1: first original word
        :param word2: second original word
        :return: distance value
        """
        w1, w2 = self.phonetics1.transform(word1), self.phonetics2.transform(word2)
        if isinstance(self.phonetics1, Soundex) and isinstance(self.phonetics2, Soundex):
            if self.phonetics1.is_delete_first_letter() and self.phonetics2.is_delete_first_letter():
                return self.metrics(w1, w2)
            else:
                return self.metrics(w1[1:], w2[1:])
        return self.metrics(w1, w2)
