from fonetika.soundex import RussianSoundex, FinnishSoundex, SwedenSoundex
from fonetika.metaphone import RussianMetaphone, FinnishMetaphone, SwedenMetaphone

metaphone_params = [
    ('шварцнегер', 'ШВАРЦНИГИР'),
    ('Швардснеггер', 'ШВАРЦНИГИР'),
    ('Шворцнегир', 'ШВАРЦНИГИР'),
    ('ландшафт', 'ЛАНШАФТ'),
    ('рентген', 'РИНГИН'),
    ('выборгский', 'ВАБАРСКИJ'),
    ('хельсинкский', 'ХИЛСИНСКИJ'),
    ('финляндский', 'ФИНЛАНСКИJ'),
    ('фельдшер', 'ФИЛШИР'),
    ('бильярд', 'БИЛJАРТ')
]

metaphone_finnish_params = [
    ('yö', 'IO')
]

metaphone_sweden_params = [
    ('kött', 'SHIT'),
    ('sju', 'SHU'),
    ('djur', 'JUR'),
    ('clown', 'KLAVN'),
    ('lycklig', 'LUKLI'),
    ('dålig', 'DALI'),
    ('barn', 'BAN'),
    ('skina', 'SHINA'),
    ('hjälm', 'JILM'),
    ('skola', 'SKALA'),
    ('genom', 'JINAM'),
    ('flicka', 'FLIKA')
]

soundex_with_vowels_params = [
    ('йолочка', 'JA7A53A'),
    ('ёлочка', 'JA7A53A'),
    ('рентген', 'РB83B8'),
    ('выборгский', 'ВA1A963BJ'),
    ('хельсинкский', 'ХB76B863BJ'),
    ('финляндский', 'ФB87A863BJ'),
    ('щастье', 'ЩA64JB'),
    ('счастье', 'ЩA64JB'),
    ('бильярд', 'БB7JA94')
]

soundex_params = [
    ('йолочка', 'J070530'),
    ('ёлочка', 'J070530'),
    ('рентген', 'Р08308'),
    ('выборгский', 'В0109630J'),
    ('хельсинкский', 'Х07608630J'),
    ('финляндский', 'Ф08708630J'),
    ('щастье', 'Щ064J0'),
    ('счастье', 'Щ064J0')
]

soundex_finnish_params = [
    ('yö', 'YB')
]

soundex_sweden_params = [
    ('kött', 'ZO5'),
    ('sju', 'ZI'),
    ('djur', 'JI8'),
    ('clown', 'K6Ä27'),
    ('lycklig', 'LI46O'),
    ('dålig', 'DÄ6O'),
    ('barn', 'BÄ7'),
    ('skina', 'ZO7Ä'),
    ('hjälm', 'JÄ67'),
    ('skola', 'S4Ä6Ä'),
    ('genom', 'JO7Ä7'),
    ('flicka', 'F6O4Ä')
]


def test_metaphone():
    metaphone = RussianMetaphone(reduce_phonemes=True)
    for data, expected in metaphone_params:
        assert metaphone.transform(data) == expected


def test_finnish_metaphone():
    metaphone = FinnishMetaphone()
    for data, expected in metaphone_finnish_params:
        assert metaphone.transform(data) == expected


def test_sweden_metaphone():
    metaphone = SwedenMetaphone()
    for data, expected in metaphone_sweden_params:
        assert metaphone.transform(data) == expected


def test_soundex_with_vowels():
    soundex = RussianSoundex(delete_first_coded_letter=True, code_vowels=True)
    for data, expected in soundex_with_vowels_params:
        assert soundex.transform(data) == expected


def test_soundex_without_vowels():
    soundex = RussianSoundex(delete_first_coded_letter=True)
    for data, expected in soundex_params:
        assert soundex.transform(data) == expected


def test_finnish_soundex():
    soundex = FinnishSoundex(delete_first_coded_letter=True, code_vowels=True)
    for data, expected in soundex_finnish_params:
        assert soundex.transform(data) == expected


def test_sweden_soundex():
    soundex = SwedenSoundex(delete_first_coded_letter=True, code_vowels=True)
    for data, expected in soundex_sweden_params:
        assert soundex.transform(data) == expected
