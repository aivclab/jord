#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 5/5/22
           """

from pathlib import Path

with open(Path(__file__).parent / "README.md", "r") as this_init_file:
    __doc__ += this_init_file.read()

try:
    from .importing import *
    from .configuration import *
    from .helpers import *
    from .numpy_utilities import *
    from .data_provider import *
    from .geometry_types import *
    from .shapely_utilities import *
    from .qlive_utilities import *
    from .conversion import *
    from .categorisation import *
    from .styling import *
except ImportError as ix:
    this_package_name = Path(__file__).parent.name
    print(f"Make sure qgis module is available for {this_package_name}")
    raise ix
