from setuptools import setup, find_packages
from os.path import join, dirname

import src

setup(
    name='Spockesman',
    version=src.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=[
        'redis==3.0.1'
    ]
)
