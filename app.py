from flask import Flask, render_template
import folium

app = Flask(__name__)

@app.route('/')
def map():
    # Create a Folium map
    m = folium.Map(location=[37.7749, -122.4194], zoom_start=10)

    # Add a marker to the map
    folium.Marker([37.7749, -122.4194], popup='San Francisco').add_to(m)

    # Save the map to an HTML file
    m.save('templates/map.html')

    # Render the HTML file
    return render_template('map.html')

if __name__ == '__main__':
    app.run()
