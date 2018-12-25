import editdistance
from .soundex import Soundex


class SoundexDistance:
    def __init__(self, soundex, metrics=editdistance.eval):
        """
        Init a distance object
        :param soundex: an object of Soundex class
        :param metrics: similarity function, optional, default is Levenstein distance
        """
        assert isinstance(soundex, Soundex)
        self.soundex_converter = soundex
        self.metrics = metrics

    def distance(self, word1, word2):
        """
        Compute the distance between Soundex codes
        :param word1: first original word
        :param word2: second original word
        :return: distance value
        """
        w1, w2 = self.soundex_converter.transform(word1), self.soundex_converter.transform(word2)
        if self.soundex_converter.is_delete_first_letter():
            return self.metrics(w1, w2)
        return self.metrics(w1[1:], w2[1:])
