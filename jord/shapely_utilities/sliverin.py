from collections import defaultdict
from copy import copy
from typing import Collection, Dict, List, Sequence, Union

import shapely
from shapely.constructive import simplify
from shapely.geometry.base import GeometrySequence
from tqdm import tqdm

from jord.geometric_analysis import construct_centerline
from jord.shapely_utilities import dilate, extend_line, is_multi, iter_polygons
from jord.shapely_utilities.desliver_wkt import a_wkt
from jord.shapely_utilities.lines import (
    ExtensionDirectionEnum,
    find_isolated_endpoints,
    linemerge,
    snap_endings_to_points,
)
from jord.shapely_utilities.morphology import closing, erode, pro_opening
from jord.shapely_utilities.subdivision import subdivide

__all__ = ["desliver"]

from jord.shapely_utilities.projection import (
    get_min_max_projected_line,
    project_point_to_object,
)


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


def cut_polygon(
    polygon: shapely.Polygon, line_split_collection: List[shapely.LineString]
) -> GeometrySequence:
    line_split_collection.append(
        polygon.boundary
    )  # collection of individual linestrings for splitting in a list and add the polygon lines to it.
    merged_lines = linemerge(line_split_collection)
    border_lines = shapely.ops.unary_union(merged_lines)
    return shapely.ops.polygonize(border_lines)


def multi_line_extend(
    multi_line_string: Union[shapely.LineString, shapely.MultiLineString],
    distance: float,
) -> shapely.MultiLineString:
    isolated_endpoints = find_isolated_endpoints(multi_line_string)

    lines = []

    if isinstance(multi_line_string, shapely.LineString):
        ls = [multi_line_string]
    else:
        ls = multi_line_string.geoms

    for line in ls:
        start_point, end_point = shapely.Point(line.coords[0]), shapely.Point(
            line.coords[-1]
        )

        endpoint_in_isolated_points = end_point in isolated_endpoints

        direction = None
        if start_point in isolated_endpoints:
            if endpoint_in_isolated_points:
                direction = ExtensionDirectionEnum.both
            else:
                direction = ExtensionDirectionEnum.start
        elif endpoint_in_isolated_points:
            direction = ExtensionDirectionEnum.end

        if direction is not None:
            line = extend_line(line, offset=distance, simplify=False, side=direction)

        lines.append(line)

    return shapely.MultiLineString(lines)


def desliver_center_divide(
    polygons: Collection[shapely.Polygon], buffer_size: float = 0.2
) -> List[shapely.geometry.Polygon]:
    buffered_exterior = []

    if isinstance(polygons, Sequence):
        polygons = list(polygons)

    for polygon in polygons:
        polygon: shapely.Polygon
        buffered_exterior.append(dilate(polygon, distance=buffer_size) - polygon)

    augmented_polygons = []

    intersections = []
    for ith in range(len(buffered_exterior)):
        a = buffered_exterior.copy()
        b = a.pop(ith)
        intersections.append(shapely.unary_union(a) & b)

    for ith, intersection in tqdm(enumerate(intersections)):
        some_distance = intersection.minimum_clearance / 4.0

        center_line = construct_centerline(
            intersection, interpolation_distance=some_distance
        )

        center_line = simplify(
            center_line, preserve_topology=False, tolerance=some_distance
        )

        center_line = simplify(
            center_line, preserve_topology=True, tolerance=some_distance
        )

        center_line = multi_line_extend(center_line, distance=some_distance)

        if isinstance(intersection, shapely.Polygon):
            snapping_points = [
                shapely.Point(c) for c in subdivide(intersection).exterior.coords
            ]
        else:
            snapping_points = [
                shapely.Point(c)
                for inter in intersection.geoms
                for c in subdivide(inter).exterior.coords
            ]

        snapped_center_line = snap_endings_to_points(
            center_line, snapping_points=snapping_points, max_distance=some_distance
        )

        poly = polygons[ith]

        if True:
            for line in snapped_center_line.copy():
                projected_line = get_min_max_projected_line(line, poly)

                start, end = shapely.Point(projected_line.coords[0]), shapely.Point(
                    projected_line.coords[-1]
                )

                start_line, end_line = (
                    extend_line(
                        shapely.LineString(
                            (start, project_point_to_object(start, poly))
                        ),
                        offset=some_distance,
                    ),
                    extend_line(
                        shapely.LineString((end, project_point_to_object(end, poly))),
                        offset=some_distance,
                    ),
                )

                snapped_center_line.extend((start_line, end_line))

        res = cut_polygon(intersection, snapped_center_line)

        augmented = copy(poly)
        for r in res:
            un = r | poly
            re = erode(dilate(un, distance=1e-10), distance=1e-9)
            if is_multi(re):
                continue

            f = closing(un)

            if True:
                augmented |= f
            else:
                k = r & poly
                if k:
                    if isinstance(k, shapely.LineString):
                        if k.length >= some_distance:
                            augmented |= r

        augmented = pro_opening(augmented, distance=some_distance)
        augmented_polygons.append(augmented)

    return augmented_polygons


def desliver_least_intersectors_first(
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
        once = desliver_least_intersectors_first(polygons)
        out = desliver_least_intersectors_first(list(once.values()))

        c = shapely.MultiPolygon(iter_polygons(out.values()))
        ...

    def sauihd():
        polygons = list(shapely.from_wkt(a_wkt).geoms)
        once = desliver(polygons)
        out = desliver(list(once.values()))

        c = shapely.MultiPolygon(iter_polygons(out.values()))
        ...

    def sauihd3():
        polygons = list(shapely.from_wkt(a_wkt).geoms)
        once = desliver_center_divide(polygons)
        out = desliver_center_divide(list(once.values()))

        c = shapely.MultiPolygon(iter_polygons(out.values()))
        print(c.wkt)
        ...

    sauihd3()
