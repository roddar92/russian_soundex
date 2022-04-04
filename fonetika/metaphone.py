from .base.base import BasePhoneticsAlgorithm
from .config import FI_VOWELS, RU_VOWELS, EE_VOWELS, RU_DEAF_CONSONANTS, \
    EE_FI_DEAF_CONSONANTS, SE_VOWELS, SE_DEAF_CONSONANTS
from .ruleset import EstonianRuleSet, FinnishRuleSet, RussianRuleSet, SwedenRuleSet


class Metaphone(BasePhoneticsAlgorithm):
    """
    Basic class for Metaphone algorithm
    """
    def __init__(self, compress_ending=False, reduce_word=True):
        """
        Initialization of Metaphone object
        :param compress_ending: not used
        :param reduce_word: remove repeated letters from word
        """
        self._compress_ending = compress_ending
        self._reduce_word = reduce_word

    _deaf_consonants_seq = ''
    _deaf_consonants = str.maketrans(_deaf_consonants_seq, '')
    _vowels_table = str.maketrans('', '')

    def _deaf_consonants_letters(self, word):
        return word

    def _reduce_deaf_consonants_letters(self, word, criteria):
        res = []
        for i, letter in enumerate(word):
            if letter in self._deaf_consonants_seq and (i == len(word) - 1 or word[i + 1].lower() not in criteria):
                letter = letter.translate(self._deaf_consonants)
            res += [letter]
        return ''.join(res)

    @staticmethod
    def __compress_word_ending(word):
        return word

    def _apply_metaphone_algorithm(self, word):
        if self._reduce_word:
            word = self._reduce_seq(word)
        word = word.translate(self._vowels_table)
        word = self._deaf_consonants_letters(word)
        if self._compress_ending:
            word = self.__compress_word_ending(word)
        return word.upper()

    def transform(self, word):
        return self._apply_metaphone_algorithm(word)


class RussianMetaphone(Metaphone):
    """
    Metaphone for Russian language
    """

    _vowels = RU_VOWELS
    _deaf_consonants_seq = RU_DEAF_CONSONANTS
    _deaf_consonants = str.maketrans(_deaf_consonants_seq, 'пстфк')
    _vowels_table = str.maketrans(_vowels, 'ААААИИИИУУ')

    def __init__(self, compress_ending=False, reduce_phonemes=False, replace_ego_ogo_endings=False):
        """
        Initialization of Russian Metaphone object
        :param compress_ending: compress an ending of the transcribed word
        :param reduce_phonemes: simplify sequences of Russian consonants
        :param replace_ego_ogo_endings: replace "-его/-ого" endings with "-ево/-ово"
        """
        super().__init__(compress_ending)
        self.reduce_phonemes = reduce_phonemes
        self.replace_ego_ogo_endings = replace_ego_ogo_endings
        self.rule_set = RussianRuleSet()

    def __replace_j_vowels(self, word):
        word = self.rule_set.replace_j_vowel_phonemes(word)
        word = self.rule_set.replace_j_and_signs(word)
        return self.rule_set.replace_ii_ending(word)

    @staticmethod
    def _compress_ending(word):
        return word

    def _deaf_consonants_letters(self, word):
        return self._reduce_deaf_consonants_letters(word, self._vowels + 'лмнр')

    def transform(self, word):
        word = self._latin2cyrillic(word)
        if self.replace_ego_ogo_endings:
            word = self.rule_set.replace_ego_ogo_ending(word)
        if self.reduce_phonemes:
            word = self.rule_set.reduce_phonemes(word)
        word = self.__replace_j_vowels(word)
        return self._apply_metaphone_algorithm(word)


class FinnishMetaphone(Metaphone):
    """
    Metaphone for Finnish language
    """
    __rule_set = FinnishRuleSet()

    _vowels = FI_VOWELS
    _deaf_consonants_seq = EE_FI_DEAF_CONSONANTS
    _deaf_consonants = str.maketrans(_deaf_consonants_seq, 'pftk')
    _vowels_table = str.maketrans(FI_VOWELS, 'AAAIIIUU')

    def _deaf_consonants_letters(self, word):
        return self._reduce_deaf_consonants_letters(word, self._vowels + 'lmnr')

    def transform(self, word):
        word = self._cyrillic2latin(word)
        word = self.__rule_set.reduce_phonemes(word)
        return self._apply_metaphone_algorithm(word)


class EstonianMetaphone(Metaphone):
    """
    Metaphone for Estonian language
    """
    __rule_set = EstonianRuleSet()

    _vowels = EE_VOWELS
    _deaf_consonants_seq = EE_FI_DEAF_CONSONANTS
    _deaf_consonants = str.maketrans(_deaf_consonants_seq, 'pftk')
    _vowels_table = str.maketrans(EE_VOWELS, 'AAAIIIIUU')

    def _deaf_consonants_letters(self, word):
        return self._reduce_deaf_consonants_letters(word, self._vowels + 'lmnr')

    def transform(self, word):
        word = self._cyrillic2latin(word)
        word = self.__rule_set.reduce_phonemes(word)
        return self._apply_metaphone_algorithm(word)


class SwedenMetaphone(Metaphone):
    """
    Metaphone for Sweden language
    """
    __rule_set = SwedenRuleSet()

    _vowels = SE_VOWELS
    _deaf_consonants_seq = SE_DEAF_CONSONANTS
    _deaf_consonants = str.maketrans(_deaf_consonants_seq, 'pftk')
    _vowels_table = str.maketrans(SE_VOWELS, 'AAIIIIIUU')

    def _deaf_consonants_letters(self, word):
        return self._reduce_deaf_consonants_letters(word, self._vowels + 'lmnr')

    def transform(self, word):
        word = self._cyrillic2latin(word)
        if word.endswith('on') and not word.endswith('hon'):
            word = word[:-2] + 'ån'
        word = self.__rule_set.reduce_phonemes(word)
        return self._apply_metaphone_algorithm(word)
