from fonetika.soundex import RussianSoundex
from fonetika.metaphone import RussianMetaphone, FinnishMetaphone, EstonianMetaphone
from fonetika.distance import PhoneticsInnerLanguageDistance, PhoneticsBetweenLanguagesDistance

metaphone_params = [
    (('шварцнегер', 'Швардснеггер'), 0),
    (('Швардснеггер', 'Шворцинегир'), 1),
    (('Шворцнегир', 'шварцнегер'), 0),
    (('блеснуть', 'блестнуть'), 0),
    (('зуд', 'суд'), 1),
    (('ненасный', 'ненастный'), 0)
]

soundex_params = [
    (('йолочка', 'ёлочка'), 0),
    (('ёлочка', 'йилочка'), 1),
    (('булочная', 'булошная'), 0),
    (('зуд', 'суд'), 0),
    (('щастье', 'счастье'), 0),
]


finest_params = [
    (('yö', 'öö'), 1)
]


def test_metaphone():
    metaphone = RussianMetaphone(reduce_phonemes=True)
    distancer = PhoneticsInnerLanguageDistance(metaphone)
    for data, expected in metaphone_params:
        assert distancer.distance(*data) == expected


def test_soundex():
    soundex = RussianSoundex(delete_first_letter=True, code_vowels=True)
    distancer = PhoneticsInnerLanguageDistance(soundex, metric_name='hamming')
    for data, expected in soundex_params:
        assert distancer.distance(*data) == expected


def test_metaphone_between_languages():
    meta1 = FinnishMetaphone(reduce_word=False)
    meta2 = EstonianMetaphone(reduce_word=False)
    distancer = PhoneticsBetweenLanguagesDistance(meta1, meta2, metric_name='hamming')
    for data, expected in finest_params:
        assert distancer.distance(*data) == expected
