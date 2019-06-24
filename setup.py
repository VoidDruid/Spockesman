from os.path import dirname, join

from setuptools import find_packages, setup

import spockesman

setup(
    name='Spockesman',
    version=spockesman.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=[
        'redis>=3.2',
        'PyYAML>=4.2b1'
    ]
)
