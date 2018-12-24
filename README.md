# Soundex for Russian
Russian Phonetic algorithm based on Soundex.

Package has both implemented phoneme transformation into letter-number sequence and similarity engine for comparison of Soundex sequences (based on Levenstein distance).

### Quick start
1. Install this package via ```pip```

```python
pip install ru_soundex
```

2. Import Soundex algorithm. Package supports a lot of opportunities, it's possible to cut a result sequence (like in the original Soundex version) or code vowels too.

```python
from ru_soundex.soundex import Soundex

soundex = Soundex(delete_first_letter=True)
soundex.transform('ёлочка')
...

J070530

soundex = Soundex(delete_first_letter=True, code_vowels=True)
soundex.transform('ёлочка')
...

JA7A53A
```

3. Import Soundex Similarity for usage of string comparision

```python
from ru_soundex.similarity import SoundexSimilarity

soundex = Soundex(delete_first_letter=True)
similarity = SoundexSimilarity(soundex)
similarity.similarity('ёлочка', 'йолочка')
...

0
```