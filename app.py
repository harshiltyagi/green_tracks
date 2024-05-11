import random

from flask import Flask, render_template, request, jsonify
import requests
import heapq

app = Flask(__name__)

# Define your OpenWeatherMap API key
OPENWEATHERMAP_API_KEY = 'a67fde0f4fadd987750a9420d6843d77'

# Define your Google Maps API key for Directions API
GOOGLE_MAPS_API_KEY = 'AIzaSyDacJhpqXKa3lEVLNGMIHG0UcYMgrJY-fI'


def get_aqi_data(location_name):
    base_url = "http://api.openweathermap.org/data/2.5/air_pollution"

    params = {
        'q': location_name,
        'appid': OPENWEATHERMAP_API_KEY,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'list' in data:
        # Get the AQI value from the response (assuming it's the first entry)
        aqi = data['list'][0]['main']['aqi']
        return aqi
    else:
        return None


def get_location_coordinates(location_name):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        'address': location_name,
        'key': GOOGLE_MAPS_API_KEY,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data.get('status') == 'OK':
        # Get the coordinates (latitude and longitude) for the location
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return None


def calculate_best_path(start_location, end_location):
    class Node:
        def __init__(self, location, cost, path=[]):
            self.location = location
            self.cost = cost
            self.path = path

    def dijkstra(graph, start, end):
        visited = set()
        priority_queue = [Node(start, 0)]

        while priority_queue:
            node = heapq.heappop(priority_queue)
            current_location = node.location
            current_cost = node.cost
            current_path = node.path

            if current_location in visited:
                continue

            visited.add(current_location)
            current_path.append(current_location)

            if current_location == end:
                return current_path

            for neighbor, cost in graph[current_location].items():
                if neighbor not in visited:
                    heapq.heappush(priority_queue, Node(neighbor, current_cost + cost, current_path.copy()))

        return []

    start_coordinates = get_location_coordinates(start_location)
    end_coordinates = get_location_coordinates(end_location)

    # Mimic AQI data with random values for individual road segments
    # For simplicity, we consider a single road segment between start and end locations
    road_segment_aqi = random.randint(1, 100)

    # Initialize the graph with the random AQI value for the road segment
    graph = {
        start_location: {end_location: road_segment_aqi},
        end_location: {start_location: road_segment_aqi}
    }

    best_path = dijkstra(graph, start_location, end_location)
    return best_path


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate_best_path', methods=['POST'])
def calculate_path():
    start_location = request.form['start_location']
    end_location = request.form['end_location']

    best_path = calculate_best_path(start_location, end_location)

    if best_path:
        return jsonify({'best_path': best_path})
    else:
        return jsonify({'error': 'Path calculation failed'})


if __name__ == '__main__':
    app.run(debug=True)
