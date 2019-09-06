import setuptools
from os.path import dirname, join

import spockesman

setuptools.setup(
    name='Spockesman',
    packages=['spockesman'],
    version=spockesman.__version__,
    author='Igor Beschastnov',
    description='Declarative state-machine, mainly for chat-bots',
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=[
        'redis>=3.2',
        'PyYAML>=4.2b1'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent'
    ],
)
