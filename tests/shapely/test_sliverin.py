import shapely

from jord.shapely_utilities import dilate
from jord.shapely_utilities.sliverin import (
    desliver_center_divide,
    desliver_least_intersectors_first,
)


def test_union_buf():
    buffered_exterior = [
        dilate(
            shapely.Point((0, 0)), cap_style=shapely.BufferCapStyle.square, distance=1.2
        ),
        dilate(
            shapely.Point((2, 0)), cap_style=shapely.BufferCapStyle.square, distance=1.2
        ),
        dilate(
            shapely.Point((4, 0)), cap_style=shapely.BufferCapStyle.square, distance=1.2
        ),
    ]

    for ith in range(len(buffered_exterior)):
        a = buffered_exterior.copy()
        b = a.pop(ith)
        res = shapely.unary_union(a) & b

        print(res.wkt)


def test_desliver_least_intersectors():
    buffered_exterior = [
        dilate(
            shapely.Point((0, 0)), cap_style=shapely.BufferCapStyle.square, distance=0.9
        ),
        dilate(
            shapely.Point((2, 0)), cap_style=shapely.BufferCapStyle.square, distance=0.9
        ),
        dilate(
            shapely.Point((4, 0)), cap_style=shapely.BufferCapStyle.square, distance=0.9
        ),
    ]

    res = desliver_least_intersectors_first(buffered_exterior, buffer_size=0.2)

    print(shapely.MultiPolygon(list(res.values())).wkt)


def test_desliver_intersection_center_distribute():
    buffered_exterior = [
        dilate(
            shapely.Point((0, 0)), cap_style=shapely.BufferCapStyle.square, distance=0.9
        ),
        dilate(
            shapely.Point((2, 0)), cap_style=shapely.BufferCapStyle.square, distance=0.9
        ),
        dilate(
            shapely.Point((4, 0)), cap_style=shapely.BufferCapStyle.square, distance=0.9
        ),
    ]

    res = desliver_center_divide(buffered_exterior, buffer_size=0.2)

    print(shapely.GeometryCollection(list(res)).wkt)


def test_desliver_intersection_center_distribute_circle():
    buffered_exterior = [
        dilate(
            shapely.Point((0, 0)), cap_style=shapely.BufferCapStyle.round, distance=0.9
        ),
        dilate(
            shapely.Point((2, 0)), cap_style=shapely.BufferCapStyle.round, distance=0.9
        ),
        dilate(
            shapely.Point((4, 0)), cap_style=shapely.BufferCapStyle.round, distance=0.9
        ),
    ]

    res = desliver_center_divide(buffered_exterior, buffer_size=0.3)

    print(shapely.GeometryCollection(list(res)).wkt)
