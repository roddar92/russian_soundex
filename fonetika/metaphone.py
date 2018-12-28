import re

from .base import BasePhoneticsAlgorithm


class Metaphone(BasePhoneticsAlgorithm):
    def __init__(self, compress_ending=False):
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
    _vowels_table = str.maketrans('аяоыиеёэюу', 'ЯЯЯЯИИИИУУ')

    _j_vowel_regex = re.compile(r'[ий][ео]', re.I)

    _replacement_map = {
        re.compile(r'(^|ъ|ь|' + r'|'.join(_vowels) + r')(я)', re.IGNORECASE): 'йа',
        re.compile(r'(^|ъ|ь|' + r'|'.join(_vowels) + r')(ю)', re.IGNORECASE): 'йу',
        re.compile(r'(^|ъ|ь|' + r'|'.join(_vowels) + r')(е)', re.IGNORECASE): 'йе',
        re.compile(r'(^|ъ|ь|' + r'|'.join(_vowels) + r')(ё)', re.IGNORECASE): 'йо',
        re.compile(r'([тсзжцчшщ])([жцчшщ])', re.I): r'\2',
        re.compile(r'(с)(т)([лнц])', re.I): r'\1\3',
        re.compile(r'(н)([тд])(ств)', re.I): r'\1\3',
        re.compile(r'([нс])([тд])(ск)', re.I): r'\1\3',
        re.compile(r'(р)(д)([чц])', re.I): r'\1\3',
        re.compile(r'(з)(д)([нц])', re.I): r'\1\3',
        re.compile(r'(в)(ств)', re.I): r'\2',
        re.compile(r'(л)(нц)', re.I): r'\2',
        re.compile(r'[ъь]', re.I): '',
        re.compile(r'([дт][сц])', re.I): 'ц'
    }

    def __init__(self, compress_ending=False, reduce_phonemes=False):
        super().__init__(compress_ending)
        self.reduce_phonemes = reduce_phonemes

    def _replace_j_vowels(self, word):
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
                    letter in 'бздвг' and (word[i + 1] not in 'лмнр' or word[i + 1] not in self._vowels):
                res += [letter.translate(self._deaf_consonants)]
            else:
                res += [letter]
        return ''.join(res)

    def transform(self, word):
        if self.reduce_phonemes:
            word = self._reduce_phonemes(word)
        word = self._replace_j_vowels(word)
        return self._apply_metaphone_algorithm(word)
