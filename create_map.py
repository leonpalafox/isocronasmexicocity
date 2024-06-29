# Import necessary libraries
import folium  # For creating interactive maps
import json  # For working with JSON data
import requests  # For making HTTP requests
import time  # For adding delays between API calls

# OpenRouteService API key
# Replace this with your actual API key from OpenRouteService
ORS_API_KEY = 'YOUR_API_KEY_HERE'

def get_isochrone(lat, lng, time_range):
    """
    Fetch isochrone data from OpenRouteService API.

    Args:
    lat (float): Latitude of the center point.
    lng (float): Longitude of the center point.
    time_range (int): Time range for the isochrone in minutes.

    Returns:
    dict: JSON response from the API, or None if the request failed.
    """
    # API endpoint for isochrones
    url = "https://api.openrouteservice.org/v2/isochrones/foot-walking"
    
    # Set up the headers for the API request
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': ORS_API_KEY,
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    # Prepare the data for the API request
    data = {
        "locations": [[lng, lat]],  # Note: API expects [longitude, latitude]
        "range": [time_range * 60],  # Convert minutes to seconds
        "attributes": ["area"],
        "units": "km"
    }
    
    # Make the POST request to the API
    response = requests.post(url, json=data, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching isochrone: {response.status_code}, {response.text}")
        return None

def get_station_color(station_type):
    """
    Determine the color for a station marker based on its type.

    Args:
    station_type (str): The type of the station.

    Returns:
    str: Color name for the station marker.
    """
    color_map = {
        'Terminal / Transbordo': 'orange',
        'Terminal': 'red',
        'Transbordo': 'blue',
        'Intermedia': 'green'
    }
    # Return the color for the station type, or gray if type is not in the map
    return color_map.get(station_type, 'gray')

def create_map():
    """
    Create an interactive map of Mexico City's metro system with stations and isochrones.

    Returns:
    folium.Map: The created map object.
    """
    # Load the GeoJSON file containing metro station data
    with open('mexico_city_subway_stations.geojson', 'r') as f:
        metro_stations = json.load(f)

    # Create a map centered on Mexico City
    m = folium.Map(location=[19.4326, -99.1332], zoom_start=11)

    # Iterate through each station in the GeoJSON data
    for feature in metro_stations['features']:
        properties = feature['properties']
        coordinates = feature['geometry']['coordinates']
        lng, lat = coordinates[0], coordinates[1]
        
        # Add a circular marker for each station
        folium.CircleMarker(
            location=[lat, lng],
            radius=8,
            popup=folium.Popup(f"<b>{properties['NOMBRE']}</b><br>Line: {properties['LINEA']}<br>Type: {properties['TIPO']}<br>Borough: {properties['ALCALDIAS']}<br>Year: {properties['AÑO']}", max_width=300),
            color='black',
            fill=True,
            fillColor=get_station_color(properties['TIPO']),
            fillOpacity=0.7
        ).add_to(m)
        
        # Get and add 15-minute isochrone for each station
        isochrone = get_isochrone(lat, lng, 15)
        if isochrone:
            folium.GeoJson(
                isochrone,
                style_function=lambda x: {'fillColor': 'green', 'color': 'green', 'weight': 2, 'fillOpacity': 0.3}
            ).add_to(m)
        
        # Add a small delay to avoid hitting API rate limits
        time.sleep(1)

    # Save the map as an HTML file
    m.save("mexico_city_metro_map.html")
    print("Map has been generated and saved as mexico_city_metro_map.html")
    
    # Return the map object
    return m

if __name__ == "__main__":
    create_map()
