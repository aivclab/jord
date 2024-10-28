from collections import defaultdict
from typing import Collection, Dict, List, Sequence

import shapely

from jord.shapely_utilities import dilate, iter_polygons
from jord.shapely_utilities.desliver_wkt import a_wkt
from jord.shapely_utilities.morphology import pro_opening

__all__ = ["desliver"]


def desliver(
    polygons: Collection[shapely.Polygon], buffer_size: float = 0.2
) -> List[shapely.geometry.Polygon]:
    buffered_exterior = []

    if isinstance(polygons, Sequence):
        polygons = list(polygons)

    for polygon in polygons:
        polygon: shapely.Polygon
        buffered_exterior.append(dilate(polygon, distance=buffer_size) - polygon)

    return buffered_exterior


def desliver2(
    polygons: Collection[shapely.Polygon], buffer_size: float = 0.2
) -> Dict[int, shapely.geometry.Polygon]:
    buffered_exterior = []

    if isinstance(polygons, Sequence):
        polygons = list(polygons)

    for polygon in polygons:
        polygon: shapely.Polygon
        buffered_exterior.append(dilate(polygon, distance=buffer_size) - polygon)

    intersections = []
    for ith in range(len(buffered_exterior)):
        a = buffered_exterior.copy()
        b = a.pop(ith)
        intersections.append(shapely.unary_union(a) & b)

    inter_intersections = defaultdict(dict)
    num_intersections = len(intersections)
    for ith in range(num_intersections):
        for jth in range(num_intersections):
            if ith == jth:
                continue

            if (
                False
            ):  # TODO: OPTIMISATION when picking least intersectors to get intersection?
                if ith in inter_intersections[jth]:
                    continue

            c = intersections[ith] & intersections[jth]

            if not c.is_empty:
                inter_intersections[ith][jth] = c

    already_assigned = defaultdict(list)
    out = {}
    for ith_poly, intersectors in sorted(
        inter_intersections.items(), key=lambda d: len(d[-1].values()), reverse=False
    ):
        p = polygons[ith_poly]

        if intersectors:
            for ith_intersector, intersection in intersectors.items():
                already_assigned[ith_poly].append(ith_intersector)

                if ith_poly in already_assigned[ith_intersector]:
                    continue

                p |= intersection - polygons[ith_intersector]

            out[ith_poly] = pro_opening(p, distance=buffer_size)
        else:
            out[ith_poly] = p

    assert len(out) == len(polygons)

    return out


if __name__ == "__main__":

    def sauihd2():
        polygons = list(shapely.from_wkt(a_wkt).geoms)
        once = desliver2(polygons)
        out = desliver2(list(once.values()))

        c = shapely.MultiPolygon(iter_polygons(out.values()))
        ...

    def sauihd():
        polygons = list(shapely.from_wkt(a_wkt).geoms)
        once = desliver(polygons)
        out = desliver(list(once.values()))

        c = shapely.MultiPolygon(iter_polygons(out.values()))
        ...

    sauihd()
