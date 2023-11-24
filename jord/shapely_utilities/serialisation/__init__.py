#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 1/23/23
           """

from pathlib import Path

with open(Path(__file__).parent / "README.md", "r") as this_init_file:
    __doc__ += this_init_file.read()


from .well_known_binary import *
from .well_known_text import *
