# Soundex for Russian
Russian, English and Finnish Phonetic algorithm based on Soundex.

Package has both implemented phoneme transformation into letter-number sequence and similarity engine for comparison of Soundex sequences (based on Levenstein distance).

### Quick start
1. Install this package via ```pip```

```python
pip install ru-soundex
```

2. Import Soundex algorithm.

Package supports a lot of opportunities, it's possible to cut a result sequence (like in the original Soundex version) or also code vowels.

```python
from russian_soundex.soundex import RussianSoundex

soundex = RussianSoundex(delete_first_letter=True)
soundex.transform('ёлочка')
...

J070530

soundex = Soundex(delete_first_letter=True, code_vowels=True)
soundex.transform('ёлочка')
...

JA7A53A
```

> A structure of the library is scalable, `RussianSoundex` class inherits basic class `Soundex` (original for English language). In order to extend our algorithm, you need just inherit own class from `Soundex` and override methods.

3. Import Soundex Similarity for usage of string comparision

```python
from russian_soundex.similarity import SoundexSimilarity

soundex = RussianSoundex(delete_first_letter=True)
similarity = SoundexSimilarity(soundex)
similarity.similarity('ёлочка', 'йолочка')
...

0
```