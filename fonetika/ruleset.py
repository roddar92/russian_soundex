from abc import ABC, abstractmethod

from .config import EN_REMOVE_MAP, RU_PHONEMES, RU_REMOVE_MAP, \
    RU_REPLACEMENT_J_MAP, RU_REPLACEMENT_VOWEL_MAP, \
    EN_PHONEMES, EE_PHONEMES, FI_PHONEMES, SE_PHONEMES, \
    RU_EGO_OGO_ENDING, RU_IA_ENDING, RU_II_ENDING


class RuleSet(ABC):
    @abstractmethod
    def _replacement_phoneme_map(self):
        """
        :return: list of substitution rules
        """
        return []

    def reduce_phonemes(self, word):
        """
        Transcripts a given word into phonological sequence by language rules
        :param word: string
        :return: modified string
        """
        for replace, result in self._replacement_phoneme_map():
            word = replace.sub(result, word)
        return word


class RussianRuleSet(RuleSet):
    """
    Transcription rules for Russian language
    """
    __replacement_j_map = RU_REPLACEMENT_J_MAP
    __replacement_vowel_map = RU_REPLACEMENT_VOWEL_MAP
    __remove_map = RU_REMOVE_MAP
    __ia_ending = RU_IA_ENDING
    __ii_ending = RU_II_ENDING
    __ego_ogo_endings = RU_EGO_OGO_ENDING

    def _replacement_phoneme_map(self):
        return RU_PHONEMES

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


class SwedenRuleSet(RuleSet):
    """
    Transcription rules for Swedish language
    """
    def _replacement_phoneme_map(self):
        return SE_PHONEMES


class EstonianRuleSet(RuleSet):
    """
    Transcription rules for Estonian language
    """
    def _replacement_phoneme_map(self):
        return EE_PHONEMES


class FinnishRuleSet(RuleSet):
    """
    Transcription rules for Finnish language
    """
    def _replacement_phoneme_map(self):
        return FI_PHONEMES


class EnglishRuleSet(RuleSet):
    """
    Transcription rules for English language
    """
    def _replacement_phoneme_map(self):
        return EN_PHONEMES

    __remove_map = EN_REMOVE_MAP

    def remove_empty_sounds(self, word):
        for replace, result in self.__remove_map:
            word = replace.sub(result, word)
        return word
