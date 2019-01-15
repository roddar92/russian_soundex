import re

from .base import BasePhoneticsAlgorithm


class Metaphone(BasePhoneticsAlgorithm):
    def __init__(self, compress_ending=False):
        """
        Initialization of Metaphone object
        :param compress_ending: not used
        """
        self.compress_ending = compress_ending

    _deaf_regex = re.compile(r'', re.I)
    _vowels_table = str.maketrans('', '')

    def _deaf_consonants_letters(self, word):
        return word

    def _compress_ending(self, word):
        return word

    def _apply_metaphone_algorithm(self, word):
        word = self._reduce_seq(word)
        word = word.translate(self._vowels_table)
        word = self._deaf_consonants_letters(word)
        if self.compress_ending:
            word = self._compress_ending(word)
        return word.upper()

    def transform(self, word):
        return self._apply_metaphone_algorithm(word)


class RussianMetaphone(Metaphone):
    _vowels = 'аэиоуыеёюя'
    _deaf_consonants = str.maketrans('бздвг', 'пстфк')
    _vowels_table = str.maketrans('аяоыиеёэюу', 'ААААИИИИУУ')

    _j_vowel_regex = re.compile(r'[ий][ео]', re.I)

    _replacement_vowel_map = {
        re.compile(r'(^|ъ|ь|' + r'|'.join(_vowels) + r')(я)', re.I): 'йа',
        re.compile(r'(^|ъ|ь|' + r'|'.join(_vowels) + r')(ю)', re.I): 'йу',
        re.compile(r'(^|ъ|ь|' + r'|'.join(_vowels) + r')(е)', re.I): 'йе',
        re.compile(r'(^|ъ|ь|' + r'|'.join(_vowels) + r')(ё)', re.I): 'йо',
        re.compile(r'[ъь]', re.I): ''
    }

    _replacement_map = {
        re.compile(r'сч', re.I): r'щ',
        re.compile(r'([тсзжцчшщ])([жцчшщ])', re.I): r'\2',
        re.compile(r'(с)(т)([лнц])', re.I): r'\1\3',
        re.compile(r'(н)([тд])(ств)', re.I): r'\1\3',
        re.compile(r'([нс])([тд])(ск)', re.I): r'\1\3',
        re.compile(r'(р)(д)([чц])', re.I): r'\1\3',
        re.compile(r'(з)(д)([нц])', re.I): r'\1\3',
        re.compile(r'(ль|н)(д)(ш)', re.I): r'\1\3',
        re.compile(r'(н)(т)(г)', re.I): r'\1\3',
        re.compile(r'(в)(ств)', re.I): r'\2',
        re.compile(r'(л)(нц)', re.I): r'\2',
        re.compile(r'([дт][сц])', re.I): 'ц'
    }

    def __init__(self, compress_ending=False, reduce_phonemes=False):
        super().__init__(compress_ending)
        self.reduce_phonemes = reduce_phonemes

    def _replace_j_vowels(self, word):
        for replace, result in self._replacement_vowel_map.items():
            word = replace.sub(result, word)
        return self._j_vowel_regex.sub('и', word)

    def _reduce_phonemes(self, word):
        for replace, result in self._replacement_map.items():
            word = replace.sub(result, word)
        return word

    def _compress_ending(self, word):
        return word

    def _deaf_consonants_letters(self, word):
        res = []
        for i, letter in enumerate(word):
            if i == len(word) - 1 or \
                    letter in self._deaf_consonants and (word[i + 1] not in 'лмнр' or word[i + 1] not in self._vowels):
                res += [letter.translate(self._deaf_consonants)]
            else:
                res += [letter]
        return ''.join(res)

    def transform(self, word):
        if self.reduce_phonemes:
            word = self._reduce_phonemes(word)
        word = self._replace_j_vowels(word)
        return self._apply_metaphone_algorithm(word)


class FinnishMetaphone(Metaphone):
    _vowels = 'aäeioöuy'
    _deaf_consonants = str.maketrans('bvdg', 'pftk')
    _vowels_table = str.maketrans('aäeioöuy', 'ÄÄIIIIУУ')

    _z_replacement = re.compile(r'z', re.I)
    _q_replacement = re.compile(r'q', re.I)
    _w_replacement = re.compile(r'w', re.I)
    _x_replacement = re.compile(r'x', re.I)

    def _deaf_consonants_letters(self, word):
        res = []
        for i, letter in enumerate(word):
            if i == len(word) - 1 or \
                    letter in self._deaf_consonants and (word[i + 1] not in 'lmnr' or word[i + 1] not in self._vowels):
                res += [letter.translate(self._deaf_consonants)]
            else:
                res += [letter]
        return ''.join(res)

    def transform(self, word):
        word = self._z_replacement.sub('ts', word)
        word = self._q_replacement.sub('k', word)
        word = self._w_replacement.sub('v', word)
        word = self._x_replacement.sub('ks', word)
        return self._apply_metaphone_algorithm(word)
