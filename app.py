from flask import Flask, render_template
import folium
import geopandas as gpd
from sqlalchemy import create_engine

app = Flask(__name)

# Azure PostgreSQL connection string
connection_string = "postgresql+psycopg2://AdminDB:Aa1234567Aa1234567@isilgeodbdev.postgres.database.azure.com:5432/postgres"
engine = create_engine(connection_string, timeout=60)

@app.route('/')
def map_view():
    # Create a connection to the Azure PostgreSQL database using SQLAlchemy
    engine = create_engine(connection_string)

    # Read the "polygons_table" as a GeoDataFrame
    query = "SELECT * FROM polygons_data"
    gdf = gpd.read_postgis(query, con=engine)

    # Create a map with Folium
    m = folium.Map(location=[0, 0], zoom_start=2)

    # Create a GeoJSON layer and add it to the map
    feature_group = folium.FeatureGroup(name="Polygons")

    for idx, row in gdf.iterrows():
        # Access the geometry column
        geometry = row['geometry']

        # Create a GeoJSON layer for each polygon
        polygon_layer = folium.GeoJson(data=geometry.__geo_interface__)
        polygon_layer.add_to(feature_group)

    feature_group.add_to(m)
    folium.LayerControl().add_to(m)

    # Save the map to an HTML file
    m.save('templates/map.html')

    return render_template('map.html')

if __name__ == '__main__':
    app.run()
