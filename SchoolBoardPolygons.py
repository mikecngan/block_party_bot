import geopandas as gpd
import os
from shapely.geometry import MultiPolygon, Polygon

def convert_to_multipolygon(geometry):
    if geometry.geom_type == 'MultiPolygon':
        return geometry
    elif geometry.geom_type == 'Polygon':
        return MultiPolygon([geometry])
    elif geometry.geom_type == 'GeometryCollection':
        polygons = [geom for geom in geometry.geoms if geom.geom_type in ['Polygon', 'MultiPolygon']]
        return MultiPolygon(polygons)
    else:
        return geometry  # or return None, or raise an error

def get_district_2():
    # Convert KML to GeoJSON
    kml_file = 'SchoolBoardDistricts.kml'
    geojson_file = 'SchoolBoardDistricts.geojson'

    ogr2ogr = '/opt/homebrew/opt/gdal/bin/ogr2ogr'  # path to ogr2ogr
    command = f'{ogr2ogr} -f GeoJSON {geojson_file} {kml_file}'

    os.system(command)

    # Read GeoJSON file
    gdf = gpd.read_file(geojson_file)

    # Convert to multipolygon
    gdf['geometry'] = gdf['geometry'].apply(lambda x: x if x.is_valid else x.buffer(0))
    gdf['geometry'] = gdf['geometry'].apply(convert_to_multipolygon)

    # Filter the GeoDataFrame and select only 'Name' and 'geometry' columns
    gdf = gdf[gdf['Name'].isin(["District G\n", "District D\n"])][['Name', 'geometry']]

    # Strip whitespace from 'Name' column
    gdf['Name'] = gdf['Name'].str.strip()

    return gdf

#made for Paul Rosenfeld
def get_district_4():
    # Convert KML to GeoJSON
    kml_file = 'SchoolBoardDistricts.kml'
    geojson_file = 'SchoolBoardDistricts.geojson'

    ogr2ogr = '/opt/homebrew/opt/gdal/bin/ogr2ogr'  # path to ogr2ogr
    command = f'{ogr2ogr} -f GeoJSON {geojson_file} {kml_file}'

    os.system(command)

    # Read GeoJSON file
    gdf = gpd.read_file(geojson_file)

    # Convert to multipolygon
    gdf['geometry'] = gdf['geometry'].apply(lambda x: x if x.is_valid else x.buffer(0))
    gdf['geometry'] = gdf['geometry'].apply(convert_to_multipolygon)

    # Filter the GeoDataFrame and select only 'Name' and 'geometry' columns
    gdf = gdf[gdf['Name'].isin(["District H\n", "District A\n"])][['Name', 'geometry']]

    # Strip whitespace from 'Name' column
    gdf['Name'] = gdf['Name'].str.strip()

    return gdf


