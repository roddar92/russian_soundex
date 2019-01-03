from fonetika.soundex import RussianSoundex
from fonetika.metaphone import RussianMetaphone


metaphone_params = [
    ('шварцнегер', 'ШВАРЦНИГИР'),
    ('Швардснеггер', 'ШВАРЦНИГИР'),
    ('Шворцнегир', 'ШВАРЦНИГИР')
]

soundex_params = [
    ('йолочка', 'JA7A53A'),
    ('ёлочка', 'JA7A53A')
]


def test_metaphone():
    metaphone = RussianMetaphone(reduce_phonemes=True)
    for data, expected in metaphone_params:
        assert metaphone.transform(data) == expected


def test_soundex():
    soundex = RussianSoundex(delete_first_coded_letter=True, code_vowels=True)
    for data, expected in soundex_params:
        assert soundex.transform(data) == expected
