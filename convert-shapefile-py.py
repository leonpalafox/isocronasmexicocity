# Import the geopandas library, which provides geospatial functionality
import geopandas as gpd

def convert_shp_to_geojson(input_shp, output_geojson):
    """
    Convert a shapefile to GeoJSON format.

    Args:
    input_shp (str): Path to the input shapefile.
    output_geojson (str): Path where the output GeoJSON file will be saved.

    Returns:
    GeoDataFrame: The converted geodataframe.
    """
    # Read the shapefile into a GeoDataFrame
    # GeoDataFrame is a pandas DataFrame with a special column for geometry
    gdf = gpd.read_file(input_shp)
    
    # Convert the GeoDataFrame to a GeoJSON file
    # The 'driver' parameter specifies the output format
    gdf.to_file(output_geojson, driver='GeoJSON')
    
    # Print a success message
    print(f"Conversion complete. GeoJSON file saved as {output_geojson}")
    
    # Return the GeoDataFrame for potential further use
    return gdf

# This block only runs if the script is executed directly (not imported)
if __name__ == "__main__":
    # Specify the input shapefile name (assumed to be in the current directory)
    input_shp = 'STC_Metro_estaciones_utm14n.shp'

    # Specify the output GeoJSON file name
    output_geojson = 'mexico_city_subway_stations.geojson'

    # Run the conversion function
    gdf = convert_shp_to_geojson(input_shp, output_geojson)
