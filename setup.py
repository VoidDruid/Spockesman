from os.path import dirname, join

import setuptools
from setuptools import find_packages

import spockesman

setuptools.setup(
    name='Spockesman',
    packages=find_packages(exclude=['tests.*', 'tests', 'example', 'example.*']),
    version=spockesman.__version__,
    author='Igor Beschastnov',
    description='Declarative state-machine, mainly for chat-bots',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=[
        'PyYAML>=5.1'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent'
    ],
)
