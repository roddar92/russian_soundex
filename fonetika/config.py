import re

EN_VOWELS = 'aoeiyu'
EE_VOWELS = 'aäoeöõiüu'
SE_VOWELS = 'aoåäeöiuy'
FI_VOWELS = 'aäoeöiyu'
RU_VOWELS = 'аяоыиеёэюу'


EE_DEAF_CONSONANTS = 'bvdg'
FI_DEAF_CONSONANTS = 'bvdg'
SE_DEAF_CONSONANTS = 'bvdg'
RU_DEAF_CONSONANTS = 'бздвг'

J_VOWEL_SEQ_RU = r'^|ъ|ь|' + r'|'.join(RU_VOWELS)

RU_PHONEMES = {
    re.compile(r'(с?т|с)ч', re.I): r'щ',
    re.compile(r'([тсзжцчшщ])([жцчшщ])', re.I): r'\2',
    re.compile(r'(с)(т)([лнц])', re.I): r'\1\3',
    re.compile(r'(н)([тд])(ств)', re.I): r'\1\3',
    re.compile(r'([нс])([тдк])(ск)', re.I): r'\1\3',
    re.compile(r'(р)([гк])(ск)', re.I): r'\1\3',
    re.compile(r'(р)(д)([чц])', re.I): r'\1\3',
    re.compile(r'(з)(д)([нц])', re.I): r'\1\3',
    re.compile(r'(ль|н)(д)(ш)', re.I): r'\1\3',
    re.compile(r'(н)(т)(г)', re.I): r'\1\3',
    re.compile(r'(в)(ств)', re.I): r'\2',
    re.compile(r'(л)(нц)', re.I): r'\2',
    re.compile(r'([дт][сц])', re.I): 'ц'
}

SE_PHONEMES = {
    re.compile(r'(rs|sch|ssj|stj|skj|sj|ch)', re.I): 'sh',
    re.compile(r'(sk)([eiyöäj])', re.I): r'sh\2',
    re.compile(r'(k)([eiyöäj])', re.I): r'sh\2',
    re.compile(r'(c)([eiy])', re.I): r's\2',
    re.compile(r'(g)([eiyöäj])', re.I): r'j\2',
    re.compile(r'([dghl])(j)', re.I): r'\2',
    re.compile(r'(r)([ntl])', re.I): r'\2',
    re.compile(r'(i)(g)($)', re.I): r'\1\3',
    re.compile(r'([cq]|ck)', re.I): 'k',
    re.compile(r'[st]ion', re.I): 'shn',
    re.compile(r'w', re.I): 'v',
    re.compile(r'x', re.I): 'ks',
    re.compile(r'z', re.I): 's',
    re.compile(r'tj', re.I): 'sh'
}

RU_REPLACEMENT_VOWEL_MAP = {
    re.compile(r'(' + J_VOWEL_SEQ_RU + r')(я)', re.I): 'jа',
    re.compile(r'(' + J_VOWEL_SEQ_RU + r')(ю)', re.I): 'jу',
    re.compile(r'(' + J_VOWEL_SEQ_RU + r')(е)', re.I): 'jэ',
    re.compile(r'(' + J_VOWEL_SEQ_RU + r')(ё)', re.I): 'jо'
}
