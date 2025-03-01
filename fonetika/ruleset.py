from abc import ABC, abstractmethod

from .config import EN_REMOVE_MAP, RU_PHONEMES, RU_REMOVE_MAP, \
    RU_REPLACEMENT_J_MAP, RU_REPLACEMENT_VOWEL_MAP, RU_REPLACEMENT_CONSONANT_MAP, \
    EN_PHONEMES, EE_PHONEMES, FI_PHONEMES, SE_PHONEMES, \
    RU_EGO_OGO_ENDING, RU_IA_ENDING, RU_II_ENDING, EN_METAPHONE_PHONEMES, EN_VOWELS_TO_REMOVE, RU_VOWELS_TO_REMOVE


class RuleSet(ABC):
    @abstractmethod
    def _replacement_phoneme_map(self):
        """
        :return: list of substitution rules
        """
        return []

    def _replace_rules(self, word, rules):
        for replace, result in rules:
            word = replace.sub(result, word)
        return word

    def reduce_phonemes(self, word):
        """
        Transcripts a given word into phonological sequence by language rules
        :param word: string
        :return: modified string
        """
        return self._replace_rules(word, self._replacement_phoneme_map())


class RussianRuleSet(RuleSet):
    """
    Transcription rules for Russian language
    """
    __replacement_j_map = RU_REPLACEMENT_J_MAP
    __replacement_vowel_map = RU_REPLACEMENT_VOWEL_MAP
    __replacement_consonant_map = RU_REPLACEMENT_CONSONANT_MAP
    __remove_map = RU_REMOVE_MAP
    __remove_vowels = RU_VOWELS_TO_REMOVE
    __ia_ending = RU_IA_ENDING
    __ii_ending = RU_II_ENDING
    __ego_ogo_endings = RU_EGO_OGO_ENDING

    def _replacement_phoneme_map(self):
        return RU_PHONEMES

    def replace_consonant_vowels(self, word):
        return self._replace_rules(word, self.__replacement_consonant_map)

    def replace_ego_ogo_ending(self, word):
        return self.__ego_ogo_endings.sub(r'\1в\3', word)

    def replace_ia_ending(self, word):
        return self.__ia_ending.sub('я', word)

    def replace_ii_ending(self, word):
        return self.__ii_ending.sub('и', word)

    def replace_j_and_signs(self, word):
        return self._replace_rules(word, self.__remove_map)

    def replace_j_vowel_phonemes(self, word):
        return self._replace_rules(word, self.__replacement_j_map + self.__replacement_vowel_map)

    def reduce_vowels(self, word):
        return self._replace_rules(word, self.__remove_vowels)


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
        return self._replace_rules(word, self.__remove_map)


class EnglishMetaphoneRuleSet(RuleSet):
    """
    Transcription rules for English language
    """
    def _replacement_phoneme_map(self):
        return EN_METAPHONE_PHONEMES

    __remove_map = EN_REMOVE_MAP
    __remove_vowels = EN_VOWELS_TO_REMOVE

    def remove_empty_sounds(self, word):
        return self._replace_rules(word, self.__remove_map)

    def reduce_vowels(self, word):
        return self._replace_rules(word, self.__remove_vowels)
