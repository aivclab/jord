import shapely

from jord.shapely_utilities import dilate
from jord.shapely_utilities.sliverin import desliver2


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


def test_desliver():
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

    print(shapely.MultiPolygon(buffered_exterior).wkt)

    res = desliver2(buffered_exterior, buffer_size=0.2)

    print(shapely.MultiPolygon(list(res.values())).wkt)
