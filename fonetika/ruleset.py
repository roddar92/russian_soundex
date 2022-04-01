from abc import ABC, abstractmethod

from .config import EN_REMOVE_MAP, RU_PHONEMES, RU_REMOVE_MAP, \
    RU_REPLACEMENT_J_MAP, RU_REPLACEMENT_VOWEL_MAP, \
    EN_PHONEMES, FI_PHONEMES, SE_PHONEMES, \
    RU_EGO_OGO_ENDING, RU_IA_ENDING, RU_II_ENDING


class RuleSet(ABC):
    @abstractmethod
    def reduce_phonemes(self, word):
        """
        Transcripts a given word into phonological sequence by language rules
        :param word: string
        :return: modified string
        """
        return None


class RussianRuleSet(RuleSet):
    """
    Transcription rules for Russian language
    """
    __replacement_j_map = RU_REPLACEMENT_J_MAP
    __replacement_vowel_map = RU_REPLACEMENT_VOWEL_MAP
    __remove_map = RU_REMOVE_MAP
    __replacement_phoneme_map = RU_PHONEMES
    __ia_ending = RU_IA_ENDING
    __ii_ending = RU_II_ENDING
    __ego_ogo_endings = RU_EGO_OGO_ENDING

    def replace_j_vowel_phonemes(self, word):
        for replace, result in self.__replacement_j_map + \
                               self.__replacement_vowel_map:
            word = replace.sub(result, word)
        return word

    def replace_ego_ogo_ending(self, word):
        return self.__ego_ogo_endings.sub(r'\1в\3', word)

    def replace_ia_ending(self, word):
        return self.__ia_ending.sub('я', word)

    def replace_ii_ending(self, word):
        return self.__ii_ending.sub('и', word)

    def replace_j_and_signs(self, word):
        for replace, result in self.__remove_map:
            word = replace.sub(result, word)
        return word

    def reduce_phonemes(self, word):
        for replace, result in self.__replacement_phoneme_map:
            word = replace.sub(result, word)
        return word


class SwedenRuleSet(RuleSet):
    """
    Transcription rules for Swedish language
    """
    __replacement_phoneme_map = SE_PHONEMES

    def reduce_phonemes(self, word):
        for replace, result in self.__replacement_phoneme_map:
            word = replace.sub(result, word)
        return word


class FinnishRuleSet(RuleSet):
    """
    Transcription rules for Finnish language
    """
    __replacement_phoneme_map = FI_PHONEMES

    def reduce_phonemes(self, word):
        for replace, result in self.__replacement_phoneme_map:
            word = replace.sub(result, word)
        return word


class EnglishRuleSet(RuleSet):
    """
    Transcription rules for English language
    """
    __replacement_phoneme_map = EN_PHONEMES
    __remove_map = EN_REMOVE_MAP

    def remove_empty_sounds(self, word):
        for replace, result in self.__remove_map:
            word = replace.sub(result, word)
        return word

    def reduce_phonemes(self, word):
        for replace, result in self.__replacement_phoneme_map:
            word = replace.sub(result, word)
        return word
