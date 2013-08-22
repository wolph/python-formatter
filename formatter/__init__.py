__package_name__ = 'formatter'
__version__ = '1.0.1'
__author__ = 'Rick van Hattem'
__author_email__ = 'Rick.van.Hattem@Fawo.nl'
__description__ = '''A Python source formatter that uses the tokenize library
to ensure correctness'''
__url__ = 'https://github.com/WoLpH/formatter'

from .formatter import Formatter
from .tokens import Token, Tokens
from .offsets import (TokenOffsets, TokenOffset, DefaultTokenOffset,
                      TOKEN_OFFSETS)
from .types import TOKEN_TYPES
from . import main

__all__ = [
    'main',
    'Formatter',
    'Token',
    'Tokens',
    'TokenOffsets',
    'TokenOffset',
    'DefaultTokenOffset',
    'TOKEN_OFFSETS',
    'TOKEN_TYPES',
]
