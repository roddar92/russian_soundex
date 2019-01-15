from fonetika.soundex import RussianSoundex
from fonetika.metaphone import RussianMetaphone
from fonetika.distance import PhoneticsDistance


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


def test_metaphone():
    metaphone = RussianMetaphone(reduce_phonemes=True)
    distancer = PhoneticsDistance(metaphone)
    for data, expected in metaphone_params:
        assert distancer.distance(*data) == expected


def test_soundex():
    soundex = RussianSoundex(delete_first_letter=True, code_vowels=True)
    distancer = PhoneticsDistance(soundex, metric_name='hamming')
    for data, expected in soundex_params:
        assert distancer.distance(*data) == expected
