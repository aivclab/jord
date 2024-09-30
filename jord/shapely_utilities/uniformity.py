import logging
from typing import Optional

import shapely
from shapely import Polygon
from shapely.geometry.base import BaseGeometry
from shapely.validation import make_valid

from .morphology import dilate
from .rings import ensure_ccw_ring, ensure_cw_ring

logger = logging.getLogger(__name__)

__all__ = [
    "clean_shape",
    "ensure_cw_poly",
    "ensure_ccw_poly",
    "zero_buffer",
    "BecameEmptyException",
]


class BecameEmptyException(Exception): ...


def clean_shape(
    shape: shapely.geometry.base.BaseGeometry,
    grid_size: Optional[float] = None,
    raise_on_becoming_empty: bool = False,
) -> shapely.geometry.base.BaseGeometry:
    """
    removes self-intersections and duplicate points

    :param raise_on_becoming_empty:
    :param grid_size:
    :param shape: The shape to cleaned
    :return: the cleaned shape
    """

    original_shape = shape

    if isinstance(shape, shapely.Polygon):
        shape = ensure_cw_poly(shape)

    if grid_size is not None:
        if not shape.is_valid:
            try:
                shape = make_valid(shape)
            except shapely.errors.GEOSException as e:
                logger.error(e)

        shape = shapely.set_precision(
            shape,
            grid_size,
            mode="keep_collapsed",
        )

    shape = zero_buffer(shape).simplify(0)

    if not shape.is_valid:
        try:
            shape = make_valid(shape)
        except shapely.errors.GEOSException as e:
            logger.error(e)

    if not original_shape.is_empty:
        if shape.is_empty:
            if raise_on_becoming_empty:
                raise BecameEmptyException(
                    f"{original_shape=} was not empty, became {shape=}"
                )
            else:
                shape = original_shape.representative_point()

    if isinstance(shape, shapely.GeometryCollection):
        if len(shape.geoms) == 1:
            shape = shape.geoms[0]

    return shape


def ensure_ccw_poly(polygon: Polygon) -> Polygon:
    """
    This function checks if the polygon is counter-clockwise if not it is reversed


    :param polygon: The polygon to check
    :return: Returns the polygon turned clockwise
    """

    return Polygon(
        shell=ensure_ccw_ring(polygon.exterior),
        holes=[ensure_ccw_ring(hole) for hole in polygon.interiors],
    )


def ensure_cw_poly(polygon: Polygon) -> Polygon:
    """
    This function checks if the polygon is clockwise if not it is reversed


    :param polygon: The polygon to check
    :return: Returns the polygon turned clockwise
    """

    return Polygon(
        shell=ensure_cw_ring(polygon.exterior),
        holes=[ensure_cw_ring(hole) for hole in polygon.interiors],
    )


def zero_buffer(
    geom: BaseGeometry,
) -> BaseGeometry:
    return dilate(geom, distance=0)
