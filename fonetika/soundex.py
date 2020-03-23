import pymorphy2
import re

from .base.base import BasePhoneticsAlgorithm
from .config import RU_PHONEMES, RU_VOWELS, EN_VOWELS, FI_VOWELS, EE_VOWELS, RU_REPLACEMENT_VOWEL_MAP, SE_VOWELS


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
        self.__delete_first_letter = delete_first_letter
        self.__delete_first_coded_letter = delete_first_coded_letter
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
        word = self.__hw_replacement.sub('', word)
        if self._code_vowels:
            word = self._replace_vowels_seq(word)
        return self._apply_soundex_algorithm(word)


class FinnishSoundex(Soundex):
    """
    Soundex for Finnish language
    """
    __z_replacement = re.compile(r'z', re.I)
    __x_replacement = re.compile(r'x', re.I)

    _vowels = FI_VOWELS
    _vowels_table = str.maketrans(_vowels, 'AAABBBCC')
    _table = str.maketrans('bpfvcszkgqdtlmnrj', '11223334445567789')

    def transform(self, word):
        word = self.__z_replacement.sub('ts', word)
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
        word = self.__z_replacement.sub('ts', word)
        word = self.__x_replacement.sub('ks', word)
        return self._apply_soundex_algorithm(word)


class SwedenMetaphone(Soundex):
    """
    Soundex for Sweden language
    """
    _vowels = SE_VOWELS
    _vowels_table = str.maketrans(_vowels, 'ÄÄÄÄOOOII')
    _table = str.maketrans('bpfvcszkgqdtlmnrj', '11223334445567789')

    __cz_replacement = re.compile(r'[cz]', re.I)
    __c_replacement = re.compile(r'(c)([eiy])', re.I)
    __q_replacement = re.compile(r'[cq]', re.I)
    __w_replacement = re.compile(r'w', re.I)
    __x_replacement = re.compile(r'x', re.I)
    __z_replacement = re.compile(r'x', re.I)
    __j_replacement = re.compile(r'([dghl])(j)', re.I)
    __tj_replacement = re.compile(r'tj', re.I)
    __ig_replacement = re.compile(r'(i)(g)($)', re.I)
    __rs_replacement = re.compile(r'(rs|sch|ssj|stj|skj|sj|ch)', re.I)
    __sk_replacement = re.compile(r'(sk)([eiyöäj])', re.I)
    __stion_replacement = re.compile(r'[st]ion', re.I)
    __k_replacement = re.compile(r'(k)([eiyöäj])', re.I)

    def transform(self, word):
        word = self.__cz_replacement.sub('ts', word)
        word = self.__c_replacement.sub(r's\2', word)
        word = self.__q_replacement.sub('k', word)
        word = self.__j_replacement.sub(r'\2', word)
        word = self.__w_replacement.sub('v', word)
        word = self.__x_replacement.sub('ks', word)
        word = self.__z_replacement.sub('s', word)
        word = self.__sk_replacement.sub(r'sh\2', word)
        word = self.__k_replacement.sub(r'sh\2', word)
        word = self.__tj_replacement.sub('sh', word)
        word = self.__ig_replacement.sub(r'\1\3', word)
        word = self.__rs_replacement.sub('sh', word)
        word = self.__stion_replacement.sub('shn', word)
        return self._apply_soundex_algorithm(word)


class RussianSoundex(Soundex):
    _vowels = RU_VOWELS
    _vowels_table = str.maketrans(_vowels, 'AAAABBBBCC')
    _table = str.maketrans('бпвфгкхдтжшчщзсцлмнр', '11223334455556667889')
    _ego_ogo_endings = re.compile(r'([ео])(г)(о$)', re.I)
    __ia_ending = re.compile(r'[еи][ая]', re.I)
    __ii_ending = re.compile(r'и[еио]', re.I)

    _replacement_map = RU_REPLACEMENT_VOWEL_MAP
    _replacement_map.update({
        re.compile(r'й', re.I): 'j'
    })
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
        word = self.__ii_ending.sub('и', word)
        word = self.__ia_ending.sub('я', word)
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
        if self._code_vowels:
            word = self._replace_vowels_seq(word)
        return self._apply_soundex_algorithm(word)
