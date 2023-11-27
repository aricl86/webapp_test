from flask import Flask, render_template
import folium
import geopandas as gpd
from sqlalchemy import create_engine

app = Flask(__name__)

# Azure PostgreSQL connection string
connection_string = "postgresql+psycopg2://AdminDB@isilgeodbdev:Aa1234567Aa1234567@isilgeodbdev.postgres.database.azure.com:5432/postgres"

@app.route('/test_db_connection')
def test_db_connection():
    try:
        engine = create_engine(connection_string)
        conn = engine.connect()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Database connection successful'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Database connection failed: {str(e)}'})


@app.route('/')
def map_view():
    try:
        # Create a connection to the Azure PostgreSQL database using SQLAlchemy
        engine = create_engine(connection_string)
    
        # Read the "polygons_table" as a GeoDataFrame
        query = "SELECT * FROM polygons_data"
        gdf = gpd.read_postgis(query, con=engine)
    
        # Get the bounds of all geometries in the GeoDataFrame
        bounds = gdf.total_bounds
    
        # Calculate the center of the bounding box
        center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    
        # Create a map with Folium centered on the bounding box
        m = folium.Map(location=center, zoom_start=16)  # You can adjust the initial zoom level
    
    
        # Create a GeoJSON layer and add it to the map
        feature_group = folium.FeatureGroup(name="Polygons")
    
        for idx, row in gdf.iterrows():
            # Access the geometry column
            geometry = row['geom']
    
            # Create a GeoJSON layer for each polygon
            polygon_layer = folium.GeoJson(data=geometry.__geo_interface__)
            polygon_layer.add_to(feature_group)
    
        feature_group.add_to(m)
        folium.LayerControl().add_to(m)
    
        # Save the map to an HTML file
        m.save('map.html')
    
        return render_template('map.html')
    except Exception as e:
        # Log the exception
        app.logger.error(f"An error occurred: {str(e)}")
        # You can also print the exception for debugging purposes
        print(f"An error occurred: {str(e)}")
        # Return a custom error page
        abort(500)

if __name__ == '__main__':
    app.run(debug=True)
