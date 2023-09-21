import shapely
from geopandas import GeoDataFrame, GeoSeries

from jord.qlive_utilities.clients.auto import AutoQliveClient

with AutoQliveClient() as qlive:
    df = GeoDataFrame(
        {
            "City": ["Buenos Aires", "Brasilia", "Santiago", "Bogota", "Caracas"],
            "Country": ["Argentina", "Brazil", "Chile", "Colombia", "Venezuela"],
            "layer": ["layer1", "layer2", "layer3", "layer4", "layer5"],
            "geometry": [
                "POINT(-58.66 -34.58)",
                "POINT(-47.91 -15.78)",
                shapely.difference(
                    shapely.from_wkt("POINT(-70.66 -33.45)").buffer(1),
                    shapely.from_wkt("POINT(-70.66 -33.45)")
                    .buffer(0.5)
                    .exterior.buffer(0.1),
                ).wkt,  # Multipolygon
                shapely.from_wkt("POINT(-74.08 4.60)")
                .buffer(1)
                .exterior.wkt,  # Linestring
                shapely.from_wkt("POINT(-66.86 10.48)").buffer(1).wkt,  # Polygon
            ],
        },
        geometry="geometry",
    )

    df["geometry"] = GeoSeries.from_wkt(df["geometry"])  # Convert to shapely objects

    print(qlive.add_dataframe_layer(df))
