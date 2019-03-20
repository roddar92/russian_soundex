import editdistance
from .base import BasePhoneticsAlgorithm
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
