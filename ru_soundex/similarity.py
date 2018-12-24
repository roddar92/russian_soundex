import editdistance


class SoundexSimilarity:
    def __init__(self, soundex, metrics=editdistance.eval):
        """
        Init a similarity object
        :param soundex: an object of Soundex class
        :param metrics: similarity function, optional, default is Levenstein distance
        """
        self.soundex_converter = soundex
        self.metrics = metrics

    def similarity(self, word1, word2):
        """
        Compute the similarity between Soundex codes
        :param word1: first original word
        :param word2: second original word
        :return: distance value
        """
        w1, w2 = self.soundex_converter.transform(word1), self.soundex_converter.transform(word2)
        if self.soundex_converter.is_delete_first_letter():
            return self.metrics(w1, w2)
        return self.metrics(w1[1:], w2[1:])
