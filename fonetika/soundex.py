import pymorphy2
import re

from .base import BasePhoneticsAlgorithm
from .config import RU_PHONEMES, RU_VOWELS, EN_VOWELS, FI_VOWELS, EE_VOWELS


class Soundex(BasePhoneticsAlgorithm):

    _table, _vowels_table = str.maketrans('', ''), str.maketrans('', '')
    _vowels_regex = re.compile(r'(0+)', re.I)

    def __init__(self, delete_first_letter=False, delete_first_coded_letter=False,
                 delete_zeros=False, code_vowels=False, cut_result=False, seq_cutted_len=4):
        """
        Initialization of Soundex object
        :param delete_first_letter: remove the first letter from the result code (A169 -> 169)
        :param delete_first_coded_letter: remove the first coded letter from the result code (A0169 -> A169)
        :param delete_zeros: remove vowels from the result code
        :param code_vowels: group and code vowels as ABC letters
        :param cut_result: cut result core till N symbols
        :param seq_cutted_len: length of the result code
        """
        self.delete_first_letter = delete_first_letter
        self.delete_first_coded_letter = delete_first_coded_letter
        self.delete_zeros = delete_zeros
        self.code_vowels = code_vowels
        self.cut_result = cut_result
        self.seq_cutted_len = seq_cutted_len

    def _is_vowel(self, letter):
        return letter in self._vowels

    def _translate_vowels(self, word):
        if self.code_vowels:
            return word.translate(self._vowels_table)
        else:
            return ''.join('0' if self._is_vowel(letter) else letter for letter in word)

    def _remove_vowels_and_paired_sounds(self, seq):
        seq = self._vowels_regex.sub('', seq)
        seq = self._reduce_seq(seq)
        return seq

    def _apply_soundex_algorithm(self, word):
        word = word.lower()
        first, last = word[0], word
        last = last.translate(self._table)
        last = self._translate_vowels(last)
        last = self._reduce_seq(last)
        if self.delete_zeros:
            last = self._remove_vowels_and_paired_sounds(last)
        if self.cut_result:
            last = last[:self.seq_cutted_len] if len(last) >= self.seq_cutted_len else last
            last += ('0' * (self.seq_cutted_len - len(last)))
        if self.delete_first_coded_letter:
            last = last[1:]
        first_char = '' if self.delete_first_letter else first.capitalize()
        return first_char + last.upper()

    def get_vowels(self):
        return self._vowels

    def is_delete_first_coded_letter(self):
        return self.delete_first_coded_letter

    def is_delete_first_letter(self):
        return self.delete_first_letter

    def transform(self, word):
        return self._apply_soundex_algorithm(word)


class EnglishSoundex(Soundex):
    """
    This version may have differences from original Soundex for English (consonants was splitted in more groups)
    """
    _hw_replacement = re.compile(r'[hw]', re.I)
    _au_ending = re.compile(r'au', re.I)
    _ea_ending = re.compile(r'e[ae]', re.I)
    _oo_ue_ew_ending = re.compile(r'(ew|ue|oo)', re.I)
    _iey_ending = re.compile(r'([ie]y|ai)', re.I)
    _iye_ire_ending = re.compile(r'([iy]e|[iy]re)$', re.I)
    _ye_ending = re.compile(r'^ye', re.I)
    _ere_ending = re.compile(r'(e[ae]r|ere)$', re.I)

    _vowels = EN_VOWELS
    _vowels_table = str.maketrans(_vowels, 'AABBBC')
    _table = str.maketrans('bpfvcksgjqxzdtlmnr', '112233344555667889')

    def _replace_vowels_seq(self, word):
        word = self._ye_ending.sub('je', word)
        word = self._au_ending.sub('o', word)
        word = self._ea_ending.sub('e', word)
        word = self._oo_ue_ew_ending.sub('u', word)
        word = self._iey_ending.sub('ei', word)
        word = self._iye_ire_ending.sub('ai', word)
        word = self._ere_ending.sub('ie', word)
        return word

    def transform(self, word):
        word = self._hw_replacement.sub('', word)
        if self.code_vowels:
            word = self._replace_vowels_seq(word)
        return self._apply_soundex_algorithm(word)


class FinnishSoundex(Soundex):
    """
    Soundex for Finnish language
    """
    _z_replacement = re.compile(r'z', re.I)
    _x_replacement = re.compile(r'x', re.I)

    _vowels = FI_VOWELS
    _vowels_table = str.maketrans(_vowels, 'AAABBBCC')
    _table = str.maketrans('bpfvcszkgqdtlmnrj', '11223334445567789')

    def transform(self, word):
        word = self._z_replacement.sub('ts', word)
        word = self._x_replacement.sub('ks', word)
        return self._apply_soundex_algorithm(word)


class EstonianSoundex(Soundex):
    """
    Soundex for Estonian language
    """
    _z_replacement = re.compile(r'z', re.I)
    _x_replacement = re.compile(r'x', re.I)

    _vowels = EE_VOWELS
    _vowels_table = str.maketrans(_vowels, 'AAABBBBCC')
    _table = str.maketrans('bpfvcszkgqdtlmnrj', '11223334445567789')

    def transform(self, word):
        word = self._z_replacement.sub('ts', word)
        word = self._x_replacement.sub('ks', word)
        return self._apply_soundex_algorithm(word)


class RussianSoundex(Soundex):
    _vowels = RU_VOWELS
    _vowels_table = str.maketrans(_vowels, 'AAAABBBBCC')
    _table = str.maketrans('бпвфгкхдтжшчщзсцлмнр', '11223334455556667889')
    _ego_ogo_endings = re.compile(r'([ео])(г)(о$)', re.I)
    _ia_ending = re.compile(r'[еи][ая]', re.I)
    _ii_ending = re.compile(r'и[еио]', re.I)

    _replacement_map = {
        re.compile(r'(^|ъ|ь|' + r'|'.join(_vowels) + r')(я)', re.I): 'jа',
        re.compile(r'(^|ъ|ь|' + r'|'.join(_vowels) + r')(ю)', re.I): 'jу',
        re.compile(r'(^|ъ|ь|' + r'|'.join(_vowels) + r')(е)', re.I): 'jэ',
        re.compile(r'(^|ъ|ь|' + r'|'.join(_vowels) + r')(ё)', re.I): 'jо',
        re.compile(r'й', re.IGNORECASE): 'j'
    }
    _replacement_map.update(RU_PHONEMES)

    def __init__(self, delete_first_letter=False, delete_first_coded_letter=False,
                 delete_zeros=False, cut_result=False, seq_cutted_len=4,
                 code_vowels=False, reduce_phonemes=True, use_morph_analysis=False):
        """
        Initialization of Russian Soundex object
        :param delete_first_letter:
        :param delete_first_coded_letter:
        :param delete_zeros:
        :param code_vowels:
        :param cut_result:
        :param seq_cutted_len:
        :param use_morph_analysis: use morphological grammems for phonemes analysis
        :param code_vowels: group and code vowels as ABC letters
        :param reduce_phonemes: simplify sequences of Russian consonants
        """
        super(RussianSoundex, self).__init__(delete_first_letter, delete_first_coded_letter,
                                             delete_zeros, code_vowels, cut_result, seq_cutted_len)

        self.reduce_phonemes = reduce_phonemes
        self.use_morph_analysis = use_morph_analysis
        self._moprh = pymorphy2.MorphAnalyzer()

    def _replace_ego_ogo_endings(self, word):
        return self._ego_ogo_endings.sub(r'\1в\3', word)

    def _use_morph_for_phoneme_replace(self, word):
        parse = self._moprh.parse(word)
        if parse and ('ADJF' in parse[0].tag or 'NUMB' in parse[0].tag or 'NPRO' in parse[0].tag):
            word = self._replace_ego_ogo_endings(word)
        return word

    def _replace_vowels_seq(self, word):
        word = self._ii_ending.sub('и', word)
        word = self._ia_ending.sub('я', word)
        return word

    def _reduce_phonemes(self, word):
        for replace, result in self._replacement_map.items():
            word = replace.sub(result, word)
        return word

    def transform(self, word):
        """
        Transforms a word into a sequence with coded phonemes
        :param word: string
        :return: Soundex string code
        """
        if self.use_morph_analysis:
            word = self._use_morph_for_phoneme_replace(word)
        if self.reduce_phonemes:
            word = self._reduce_phonemes(word)
        if self.code_vowels:
            word = self._replace_vowels_seq(word)
        return self._apply_soundex_algorithm(word)
