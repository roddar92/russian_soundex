from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='fonetika',
    version='1.1.9',
    url='https://github.com/roddar92/russian_soundex',
    author='Daria Rodionova',
    author_email='drodionova86@gmail.com',
    license='MIT',
    packages=find_packages(),
    description='Phonetics algorithms (Soundex and Metaphone) for russian, english and finnish languages',
    long_description=open(join(dirname(__file__), 'README.md')).read(), install_requires=['pymorphy2', 'editdistance'],
    long_description_content_type="text/markdown",
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: Russian',
        'Natural Language :: Finnish',
        'Topic :: Text Processing :: Linguistic'
    ]
)
