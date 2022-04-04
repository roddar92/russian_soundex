import re

EN_VOWELS = 'aoeiyu'
EE_VOWELS = 'aäoeöõiüu'
SE_VOWELS = 'aåäeöiyou'
FI_VOWELS = 'aäoeöiyu'
RU_VOWELS = 'аяоыиеёэюу'


EE_FI_DEAF_CONSONANTS = 'bvdg'
SE_DEAF_CONSONANTS = 'bvdg'
RU_DEAF_CONSONANTS = 'бздвг'

SE_VOWL = 'eiyöäj'

J_SEQ_RU = r'^|ъ|ь'
J_VOWEL_SEQ_RU = r'|'.join(RU_VOWELS)

RU_EGO_OGO_ENDING = re.compile(r'([ео])(г)(о$)', re.I)
RU_IA_ENDING = re.compile(r'[еи][ая]', re.I)
RU_II_ENDING = re.compile(r'и[еио]', re.I)

EN_REMOVE_MAP = [
    (re.compile(r'[hw]', re.I), '')
]

EN_PHONEMES = [
    (re.compile(r'^ye', re.I), 'je'),
    (re.compile(r'au', re.I), 'o'),
    (re.compile(r'e[ae]', re.I), 'e'),
    (re.compile(r'(ew|ue|oo)', re.I), 'u'),
    (re.compile(r'([ie]y|ai)', re.I), 'ei'),
    (re.compile(r'([iy]e|[iy]re)$', re.I), 'ai'),
    (re.compile(r'(e[ae]r|ere)$', re.I), 'ie')
]

EE_PHONEMES = [
    (re.compile(r'[cz]', re.I), 'ts'),
    (re.compile(r'q', re.I), 'kv'),
    (re.compile(r'w', re.I), 'v'),
    (re.compile(r'x', re.I), 'ks'),
    (re.compile(r'y', re.I), 'i')
]

FI_PHONEMES = [
    (re.compile(r'sh', re.I), 's'),
    (re.compile(r'ng', re.I), 'n'),
    (re.compile(r'z', re.I), 'ts'),
    (re.compile(r'q', re.I), 'kv'),
    (re.compile(r'w', re.I), 'v'),
    (re.compile(r'x', re.I), 'ks')
]

RU_PHONEMES = [
    (re.compile(r'(ст|[сзж])(ч)', re.I), r'щ'),  # Подписчик, заказчик, мужчина, жёстче.
    (re.compile(r'([сжт])(ш)', re.I), r'\2'),  # Обветшалый, выросший.
    (re.compile(r'([зс])(ж)', re.I), r'\2'),  # Визжать, обезжиренный.
    (re.compile(r'(с)(щ)', re.I), r'\2'),  # Бесщадный, расщепить.
    (re.compile(r'(т)([чщ])', re.I), r'ч'),  # Тщательно.
    (re.compile(r'(с)(т)([глнц])', re.I), r'\1\3'),  # Устлан, местный, бюстгальтер.
    (re.compile(r'(н)([тд])(ств)', re.I), r'\1\3'),  # Агентство, президентство.
    (re.compile(r'([нс])([тдк])(ск)', re.I), r'\1\3'),  # Баскский.
    (re.compile(r'(р)([гк])(ск)', re.I), r'\1\3'),  # Выборгский.
    (re.compile(r'(р)(д)([чц])', re.I), r'\1\3'),  # Сердце.
    (re.compile(r'(з)(д)([нц])', re.I), r'\1\3'),  # Уздцы, праздный, поздно.
    (re.compile(r'(ль|н)(д)([шц])', re.I), r'\1\3'),  # Голландцы, эндшпиль.
    (re.compile(r'(н)(т)(г)', re.I), r'\1\3'),  # Рентген.
    (re.compile(r'(в)(ств)', re.I), r'\2'),  # Здравствуй, чувствовать.
    (re.compile(r'(л)(нц)', re.I), r'\2'),  # Солнце.
    (re.compile(r'([дт][сц])', re.I), 'ц'),  # Солдатский, детство.
    (re.compile(f'(х)(г)', re.I), r'\2')  # Бухгалтер.
]

SE_PHONEMES = [
    (re.compile(r'^och$', re.I), 'å'),
    (re.compile(r'(rs|sch|ssj)', re.I), 'sh'),
    (re.compile(r'(stj|skj|sj|ch)', re.I), 'hf'),
    (re.compile(rf'(sk)([{SE_VOWL}])', re.I), r'sh\2'),
    (re.compile(rf'(k)([{SE_VOWL}])', re.I), r'sh\2'),
    (re.compile(rf'(c)([{SE_VOWL}])', re.I), r's\2'),
    (re.compile(rf'(g)([{SE_VOWL}])', re.I), r'j\2'),
    (re.compile(r'([dghl])(j)', re.I), r'\2'),
    (re.compile(r'(r)([ntl])', re.I), r'\2'),
    (re.compile(r'(i)(g)($)', re.I), r'\1\3'),
    (re.compile(r'(n)(g)', re.I), r'\1'),
    (re.compile(r'([cq]|ck)', re.I), 'k'),
    (re.compile(r'[st]ion', re.I), 'shn'),
    (re.compile(r'w', re.I), 'v'),
    (re.compile(r'x', re.I), 'ks'),
    (re.compile(r'z', re.I), 's'),
    (re.compile(r'tj', re.I), 'sh')
]

RU_REPLACEMENT_J_MAP = [
    (re.compile(r'(' + J_SEQ_RU + r')(я)', re.I), 'jа'),
    (re.compile(r'(' + J_SEQ_RU + r')(ю)', re.I), 'jу'),
    (re.compile(r'(' + J_SEQ_RU + r')(е)', re.I), 'jэ'),
    (re.compile(r'(' + J_SEQ_RU + r')(ё)', re.I), 'jо')
]

RU_REPLACEMENT_VOWEL_MAP = [
    (re.compile(r'(' + J_VOWEL_SEQ_RU + r')(я)', re.I), r'\1jа'),
    (re.compile(r'(' + J_VOWEL_SEQ_RU + r')(ю)', re.I), r'\1jу'),
    (re.compile(r'(' + J_VOWEL_SEQ_RU + r')(е)', re.I), r'\1jэ'),
    (re.compile(r'(' + J_VOWEL_SEQ_RU + r')(ё)', re.I), r'\1jо')
]

RU_REMOVE_MAP = [
    (re.compile(r'й', re.I), 'j'),
    (re.compile(r'[ъь]', re.I), '')
]
