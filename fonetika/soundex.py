import pymorphy2
import re

from .base.base import BasePhoneticsAlgorithm
from .config import RU_PHONEMES, RU_VOWELS, EN_VOWELS, FI_VOWELS, EE_VOWELS, \
    RU_REMOVE_MAP, RU_REPLACEMENT_J_MAP, RU_REPLACEMENT_VOWEL_MAP, SE_VOWELS, SE_PHONEMES


class Soundex(BasePhoneticsAlgorithm):
    """
    Basic class for Soundex algorithm
    """
    _table, _vowels_table = str.maketrans('', ''), str.maketrans('', '')
    _vowels_regex = re.compile(r'(0+)', re.I)

    def __init__(self, delete_first_letter=False, delete_first_coded_letter=False, reduce_word=True,
                 delete_zeros=False, code_vowels=False, cut_result=False, seq_cutted_len=4):
        """
        Initialization of Soundex object
        :param delete_first_letter: remove the first letter from the result code (A169 -> 169)
        :param delete_first_coded_letter: remove the first coded letter from the result code (A0169 -> A169)
        :param reduce_word: reduce repeated characters (A00169 -> A0169)
        :param delete_zeros: remove vowels from the result code
        :param code_vowels: group and code vowels as ABC letters
        :param cut_result: cut result core till N symbols
        :param seq_cutted_len: length of the result code
        """
        self.__delete_first_letter = delete_first_letter
        self.__delete_first_coded_letter = delete_first_coded_letter
        self.__reduce_word = reduce_word
        self.__delete_zeros = delete_zeros
        self._code_vowels = code_vowels
        self.__cut_result = cut_result
        self.__seq_cutted_len = seq_cutted_len

    def __is_vowel(self, letter):
        return letter in self._vowels

    def __translate_vowels(self, word):
        if self._code_vowels:
            return word.translate(self._vowels_table)
        else:
            return ''.join('0' if self.__is_vowel(letter) else letter for letter in word)

    def __remove_vowels_and_paired_sounds(self, seq):
        seq = self._vowels_regex.sub('', seq)
        seq = self._reduce_seq(seq)
        return seq

    def _apply_soundex_algorithm(self, word):
        word = word.lower()
        first, last = word[0], word
        last = last.translate(self._table)
        last = self.__translate_vowels(last)
        if self.__reduce_word:
            last = self._reduce_seq(last)
        if self.__delete_zeros:
            last = self.__remove_vowels_and_paired_sounds(last)
        if self.__cut_result:
            last = last[:self.__seq_cutted_len] if len(last) >= self.__seq_cutted_len else last
            last += ('0' * (self.__seq_cutted_len - len(last)))
        if self.__delete_first_coded_letter:
            last = last[1:]
        first_char = '' if self.__delete_first_letter else first.capitalize()
        return first_char + last.upper()

    def get_vowels(self):
        return self._vowels

    def is_delete_first_coded_letter(self):
        return self.__delete_first_coded_letter

    def is_delete_first_letter(self):
        return self.__delete_first_letter

    def transform(self, word):
        return self._apply_soundex_algorithm(word)


class EnglishSoundex(Soundex):
    """
    This version may have differences from original Soundex for English (consonants was splitted in more groups)
    """
    __hw_replacement = re.compile(r'[hw]', re.I)
    __au_ending = re.compile(r'au', re.I)
    __ea_ending = re.compile(r'e[ae]', re.I)
    __oo_ue_ew_ending = re.compile(r'(ew|ue|oo)', re.I)
    __iey_ending = re.compile(r'([ie]y|ai)', re.I)
    __iye_ire_ending = re.compile(r'([iy]e|[iy]re)$', re.I)
    __ye_ending = re.compile(r'^ye', re.I)
    __ere_ending = re.compile(r'(e[ae]r|ere)$', re.I)

    _vowels = EN_VOWELS
    _vowels_table = str.maketrans(_vowels, 'AABBBC')
    _table = str.maketrans('bpfvcksgjqxzdtlmnr', '112233344555667889')

    def _replace_vowels_seq(self, word):
        word = self.__ye_ending.sub('je', word)
        word = self.__au_ending.sub('o', word)
        word = self.__ea_ending.sub('e', word)
        word = self.__oo_ue_ew_ending.sub('u', word)
        word = self.__iey_ending.sub('ei', word)
        word = self.__iye_ire_ending.sub('ai', word)
        word = self.__ere_ending.sub('ie', word)
        return word

    def transform(self, word):
        word = self._cyrillic2latin(word)
        word = self.__hw_replacement.sub('', word)
        if self._code_vowels:
            word = self._replace_vowels_seq(word)
        return self._apply_soundex_algorithm(word)


class FinnishSoundex(Soundex):
    """
    Soundex for Finnish language
    """
    __sh_replacement = re.compile(r'sh', re.I)
    __ng_replacement = re.compile(r'ng', re.I)
    __z_replacement = re.compile(r'z', re.I)
    __q_replacement = re.compile(r'q', re.I)
    __w_replacement = re.compile(r'w', re.I)
    __x_replacement = re.compile(r'x', re.I)

    _vowels = FI_VOWELS
    _vowels_table = str.maketrans(_vowels, 'AAABBBCC')
    _table = str.maketrans('bpfvcszkgqdtlmnrj', '11223334445567789')

    def transform(self, word):
        word = self._cyrillic2latin(word)
        word = self.__sh_replacement.sub('s', word)
        word = self.__ng_replacement.sub('n', word)
        word = self.__z_replacement.sub('ts', word)
        word = self.__q_replacement.sub('kv', word)
        word = self.__w_replacement.sub('v', word)
        word = self.__x_replacement.sub('ks', word)
        return self._apply_soundex_algorithm(word)


class EstonianSoundex(Soundex):
    """
    Soundex for Estonian language
    """
    __z_replacement = re.compile(r'z', re.I)
    __x_replacement = re.compile(r'x', re.I)

    _vowels = EE_VOWELS
    _vowels_table = str.maketrans(_vowels, 'AAABBBBCC')
    _table = str.maketrans('bpfvcszkgqdtlmnrj', '11223334445567789')

    def transform(self, word):
        word = self._cyrillic2latin(word)
        word = self.__z_replacement.sub('ts', word)
        word = self.__x_replacement.sub('ks', word)
        return self._apply_soundex_algorithm(word)


class SwedenSoundex(Soundex):
    """
    Soundex for Sweden language
    """
    __replacement_map = SE_PHONEMES

    _vowels = SE_VOWELS
    _vowels_table = str.maketrans(_vowels, 'AABBBBBCC')
    _table = str.maketrans('bpfvcszkgqdtlmnrj', '11223334445567789')

    def transform(self, word):
        word = self._cyrillic2latin(word)
        if word.endswith('on') and not word.endswith('hon'):
            word = word[:-2] + 'ån'
        for replace, result in self.__replacement_map:
            word = replace.sub(result, word)
        word = word.replace('sh', 'z')
        word = word.replace('hf', 'x')
        return self._apply_soundex_algorithm(word)


class RussianSoundex(Soundex):
    """
    Soundex for Russian language
    """
    __ego_ogo_endings = re.compile(r'([ео])(г)(о$)', re.I)
    __ia_ending = re.compile(r'[еи][ая]', re.I)
    __ii_ending = re.compile(r'и[еио]', re.I)

    __replacement_j_map = RU_REPLACEMENT_J_MAP
    __replacement_vowel_map = RU_REPLACEMENT_VOWEL_MAP
    __remove_map = RU_REMOVE_MAP
    __replacement_phoneme_map = RU_PHONEMES

    _vowels = RU_VOWELS
    _vowels_table = str.maketrans(_vowels, 'AAAABBBBCC')
    _table = str.maketrans('бпвфгкхдтжшчщзсцлмнр', '11223334455556667889')

    SPEC_ENDING_POSTAGS = {'ADJF', 'NUMB', 'NPRO'}

    def __init__(self, delete_first_letter=False, delete_first_coded_letter=False, reduce_word=True,
                 delete_zeros=False, cut_result=False, seq_cutted_len=4,
                 code_vowels=False, reduce_phonemes=True, replace_ego_ogo_endings=False, use_morph_analysis=False):
        """
        Initialization of Russian Soundex object
        :param delete_first_letter:
        :param delete_first_coded_letter:
        :param reduce_word:
        :param delete_zeros:
        :param code_vowels:
        :param cut_result:
        :param seq_cutted_len:
        :param code_vowels: group and code vowels as ABC letters
        :param reduce_phonemes: simplify sequences of Russian consonants
        :param replace_ego_ogo_endings: replace "-его/-ого" endings with "-ево/-ово"
        :param use_morph_analysis: use morphological analysis for "-его/-ого" replacement
        """
        super(RussianSoundex, self).__init__(delete_first_letter, delete_first_coded_letter, reduce_word,
                                             delete_zeros, code_vowels, cut_result, seq_cutted_len)

        self.reduce_phonemes = reduce_phonemes
        self.use_morph_analysis = use_morph_analysis
        self.replace_ego_ogo_endings = True if self.use_morph_analysis else replace_ego_ogo_endings
        if self.use_morph_analysis:
            self.__moprh = pymorphy2.MorphAnalyzer()

    def __replace_ego_ogo_endings(self, word):
        is_applicable = True
        if self.use_morph_analysis:
            parse = self.__moprh.parse(word)
            is_applicable = parse and any(pos_tag in parse[0].tag for pos_tag in self.SPEC_ENDING_POSTAGS)
        return self.__ego_ogo_endings.sub(r'\1в\3', word) if is_applicable else word

    def _replace_vowels_seq(self, word):
        word = self.__ii_ending.sub('и', word)
        word = self.__ia_ending.sub('я', word)
        return word

    def _reduce_phonemes(self, word):
        for replace, result in self.__replacement_j_map + \
                               self.__replacement_vowel_map + \
                               self.__replacement_phoneme_map:
            word = replace.sub(result, word)
        return word

    def _replace_j_and_signs(self, word):
        for replace, result in self.__remove_map:
            word = replace.sub(result, word)
        return word

    def transform(self, word):
        """
        Transforms a word into a sequence with coded phonemes
        :param word: string
        :return: Soundex string code
        """
        word = self._latin2cyrillic(word)
        if self.replace_ego_ogo_endings:
            word = self.__replace_ego_ogo_endings(word)
        if self.reduce_phonemes:
            word = self._reduce_phonemes(word)
        if self._code_vowels:
            word = self._replace_vowels_seq(word)
        word = self._replace_j_and_signs(word)
        return self._apply_soundex_algorithm(word)
