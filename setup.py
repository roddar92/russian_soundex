from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='ru_soundex',
    version='1.0',
    url='https://github.com/roddar92/ru_soundex',
    author='Daria Rodionova',
    author_email='drodionova86@gmail.com',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(), install_requires=['pymorphy2', 'editdistance'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: Russian',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing :: Linguistic'
    ]
)
