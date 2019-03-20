from fonetika.soundex import RussianSoundex
from fonetika.metaphone import RussianMetaphone


metaphone_params = [
    ('шварцнегер', 'ШВАРЦНИГИР'),
    ('Швардснеггер', 'ШВАРЦНИГИР'),
    ('Шворцнегир', 'ШВАРЦНИГИР'),
    ('ландшафт', 'ЛАНШАФТ'),
    ('рентген', 'РИНГИН'),
    ('выборгский', 'ВАБАРСКИЙ'),
    ('фельдшер', 'ФИЛШИР')
]

soundex_with_vowels_params = [
    ('йолочка', 'JA7A53A'),
    ('ёлочка', 'JA7A53A'),
    ('рентген', 'РB83B8'),
    ('выборгский', 'ВA1A963BJ'),
    ('щастье', 'ЩA64JB'),
    ('счастье', 'ЩA64JB')
]

soundex_params = [
    ('йолочка', 'J070530'),
    ('ёлочка', 'J070530'),
    ('рентген', 'Р08308'),
    ('выборгский', 'В0109630J'),
    ('щастье', 'Щ064J0'),
    ('счастье', 'Щ064J0')
]


def test_metaphone():
    metaphone = RussianMetaphone(reduce_phonemes=True)
    for data, expected in metaphone_params:
        assert metaphone.transform(data) == expected


def test_soundex_with_vowels():
    soundex = RussianSoundex(delete_first_coded_letter=True, code_vowels=True)
    for data, expected in soundex_with_vowels_params:
        assert soundex.transform(data) == expected


def test_soundex_without_vowels():
    soundex = RussianSoundex(delete_first_coded_letter=True)
    for data, expected in soundex_params:
        assert soundex.transform(data) == expected
