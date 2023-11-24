#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy


def convert_raster_to_numpy_array(lyr) -> numpy.ndarray:
    """

    # Input: QgsRasterLayer

       :param lyr:
       :return:
       :rtype: numpy.ndarray
    """
    values = []
    provider = lyr.dataProvider()
    block = provider.block(1, lyr.extent(), lyr.width(), lyr.height())
    for i in range(lyr.height()):
        for j in range(lyr.width()):
            values.append(block.value(i, j))
    return numpy.array(values)
