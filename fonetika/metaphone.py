import re

from .base.base import BasePhoneticsAlgorithm
from .config import RU_PHONEMES, FI_VOWELS, RU_VOWELS, EE_VOWELS, \
    RU_REPLACEMENT_VOWEL_MAP, RU_DEAF_CONSONANTS, EE_FI_DEAF_CONSONANTS, SE_VOWELS, SE_DEAF_CONSONANTS, \
    SE_PHONEMES


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

    def __compress_word_ending(self, word):
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
    __j_vowel_regex = re.compile(r'[ий][ео]', re.I)

    __replacement_vowel_map = RU_REPLACEMENT_VOWEL_MAP
    __replacement_vowel_map.update({
        re.compile(r'[ъь]', re.I): ''
    })

    __replacement_phoneme_map = RU_PHONEMES

    _vowels = RU_VOWELS
    _deaf_consonants_seq = RU_DEAF_CONSONANTS
    _deaf_consonants = str.maketrans(_deaf_consonants_seq, 'пстфк')
    _vowels_table = str.maketrans(_vowels, 'ААААИИИИУУ')

    def __init__(self, compress_ending=False, reduce_phonemes=False):
        super().__init__(compress_ending)
        self.reduce_phonemes = reduce_phonemes

    def __replace_j_vowels(self, word):
        for replace, result in self.__replacement_vowel_map.items():
            word = replace.sub(result, word)
        return self.__j_vowel_regex.sub('и', word)

    def _reduce_phonemes(self, word):
        for replace, result in self.__replacement_phoneme_map.items():
            word = replace.sub(result, word)
        return word

    def _compress_ending(self, word):
        return word

    def _deaf_consonants_letters(self, word):
        return self._reduce_deaf_consonants_letters(word, self._vowels + 'лмнр')

    def transform(self, word):
        word = self._latin2cyrillic(word)
        if self.reduce_phonemes:
            word = self._reduce_phonemes(word)
        word = self.__replace_j_vowels(word)
        return self._apply_metaphone_algorithm(word)


class FinnishMetaphone(Metaphone):
    """
    Metaphone for Finnish language
    """
    __sh_replacement = re.compile(r'sh', re.I)
    __ng_replacement = re.compile(r'ng', re.I)
    __z_replacement = re.compile(r'z', re.I)
    __q_replacement = re.compile(r'q', re.I)
    __w_replacement = re.compile(r'w', re.I)
    __x_replacement = re.compile(r'x', re.I)

    _vowels = FI_VOWELS
    _deaf_consonants_seq = EE_FI_DEAF_CONSONANTS
    _deaf_consonants = str.maketrans(_deaf_consonants_seq, 'pftk')
    _vowels_table = str.maketrans(FI_VOWELS, 'AAAIIIUU')

    def _deaf_consonants_letters(self, word):
        return self._reduce_deaf_consonants_letters(word, self._vowels + 'lmnr')

    def transform(self, word):
        word = self._cyrillic2latin(word)
        word = self.__sh_replacement.sub('s', word)
        word = self.__ng_replacement.sub('n', word)
        word = self.__z_replacement.sub('ts', word)
        word = self.__q_replacement.sub('kv', word)
        word = self.__w_replacement.sub('v', word)
        word = self.__x_replacement.sub('ks', word)
        return self._apply_metaphone_algorithm(word)


class EstonianMetaphone(Metaphone):
    """
    Metaphone for Estonian language
    """
    __cz_replacement = re.compile(r'[cz]', re.I)
    __q_replacement = re.compile(r'q', re.I)
    __w_replacement = re.compile(r'w', re.I)
    __x_replacement = re.compile(r'x', re.I)
    __y_replacement = re.compile(r'y', re.I)

    _vowels = EE_VOWELS
    _deaf_consonants_seq = EE_FI_DEAF_CONSONANTS
    _deaf_consonants = str.maketrans(_deaf_consonants_seq, 'pftk')
    _vowels_table = str.maketrans(EE_VOWELS, 'AAAIIIIUU')

    def _deaf_consonants_letters(self, word):
        return self._reduce_deaf_consonants_letters(word, self._vowels + 'lmnr')

    def transform(self, word):
        word = self._cyrillic2latin(word)
        word = self.__cz_replacement.sub('ts', word)
        word = self.__q_replacement.sub('kv', word)
        word = self.__w_replacement.sub('v', word)
        word = self.__x_replacement.sub('ks', word)
        word = self.__y_replacement.sub('i', word)
        return self._apply_metaphone_algorithm(word)


class SwedenMetaphone(Metaphone):
    """
    Metaphone for Sweden language
    """
    __replacement_phoneme_map = SE_PHONEMES

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
        for replace, result in self.__replacement_phoneme_map.items():
            word = replace.sub(result, word)
        return self._apply_metaphone_algorithm(word)
