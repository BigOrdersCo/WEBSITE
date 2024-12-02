from flask import Flask, request, jsonify, render_template, send_from_directory

import requests
import re
import os

app = Flask(__name__)

# Get the parent directory of the current script
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
print(f"PARENT_DIR: {os.path.abspath(PARENT_DIR)}")
# Route for the home page
@app.route("/")
def home():
    return render_template("index.html") 
@app.route("/<filename>")
def serve_html(filename):
    full_filename = f"{filename}.html"
    return render_template(full_filename)

# @app.route("/")
# def home():
#     return send_from_directory(PARENT_DIR, "index.html")
# Route to serve the about.html file
# @app.route("/find_restaurant")
# def about():
#     return send_from_directory(PARENT_DIR, "find_restaurant.html")
# Dynamic route to serve any HTML file in the parent directory
# @app.route("/<filename>")
# def serve_html(filename):
#     print("PARENT", PARENT_DIR)
#     full_filename = f"{filename}.html"
#     return send_from_directory(PARENT_DIR, full_filename)


def get_lat_long(address, api_key):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(geocode_url)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            location = results[0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None

def find_local_restaurants(lat, lng, api_key, radius=5000, minprice=0, maxprice=2):
    query = "small local restaurants"
    places_url = (
        f"https://maps.googleapis.com/maps/api/place/textsearch/json?"
        f"query={query}&location={lat},{lng}&radius={radius}&"
        f"minprice={minprice}&maxprice={maxprice}&key={api_key}"
    )
    response = requests.get(places_url)
    if response.status_code == 200:
        results = response.json().get('results', [])
        restaurants = []
        for place in results:
            place_id = place.get('place_id')
            details = get_place_details(place_id, api_key)
            if details:
                # Check if the restaurant is a chain by analyzing the name or other criteria
                if not is_chain_restaurant(details['name']):
                    restaurants.append(details)
            if len(restaurants) >= 10:
                break
        return restaurants
    return []

def get_place_details(place_id, api_key):
    fields = (
        "name,formatted_address,website,opening_hours,"
        "price_level,rating,delivery,takeout,dine_in"
    )
    details_url = (
        f"https://maps.googleapis.com/maps/api/place/details/json?"
        f"place_id={place_id}&fields={fields}&key={api_key}"
    )
    response = requests.get(details_url)
    if response.status_code == 200:
        result = response.json().get('result', {})
        # Extract relevant details
        return {
            'name': result.get('name'),
            'address': result.get('formatted_address'),
            'website': result.get('website'),
            'opening_hours': result.get('opening_hours', {}).get('weekday_text'),
            'price_level': result.get('price_level'),
            'rating': result.get('rating'),
            'delivery': result.get('delivery'),
            'takeout': result.get('takeout'),
            'dine_in': result.get('dine_in')
        }
    return {}

def is_chain_restaurant(name):
    # Implement logic to determine if a restaurant is part of a chain
    # This can be based on the restaurant's name, website, or other criteria

    MAJOR_CHAINS = {
    "McDonald's", "Subway", "Starbucks", "KFC", "Burger King", "Pizza Hut",
    "Domino's", "Dunkin'", "Taco Bell", "Wendy's", "Chick-fil-A", "Popeyes",
    "Chipotle", "Sonic Drive-In", "Panera Bread", "Arby's", "Little Caesars",
    "Jack in the Box", "Panda Express", "Five Guys", "Dairy Queen", "Hardee's",
    "Carl's Jr.", "Papa John's", "Wingstop", "Jimmy John's", "Jollibee",
    "Tim Hortons", "In-N-Out Burger", "Shake Shack", "Raising Cane's",
    "Zaxby's", "El Pollo Loco", "Qdoba", "Del Taco", "Boston Market",
    "Church's Chicken", "Bojangles", "Whataburger", "White Castle",
    "Hungry Jack's", "Red Rooster", "Nando's", "Oporto", "Grill'd",
    "Guzman y Gomez", "Boost Juice", "Donut King", "Michel's Patisserie",
    "Noodle Box", "Sumo Salad", "Zambrero", "Pizza Capers", "Crust Pizza",
    "Mad Mex", "Salsa's Fresh Mex Grill", "Muffin Break", "The Coffee Club",
    "Gloria Jean's Coffees", "Chatime", "Top Juice", "Oliver's Real Food",
    "Soul Origin", "Roll'd", "Sushi Train", "Sushi Hub", "Sushi Sushi",
    "Hero Sushi", "Sushi Izu", "Sushi Bay", "Sushi Hon", "Sushi World"
    # Add more chains as needed
    }   
    name_lower = name.lower()
    for chain in MAJOR_CHAINS:
        # Use regex to match whole words or names
        if re.search(rf'\b{re.escape(chain.lower())}\b', name_lower):
            print("restaruant CHAIN", name)
            return True
    return False

@app.route('/find_restaurant', methods=['POST'])
def find_restaurant():
    api_key = 'AIzaSyCPGl2jds_l8dMrrYObY24QqpIWwfRCX6Y'
    data = request.json
    address = data.get('location')  # Expecting JSON payload with 'location'
    radius = data.get('radius', 5000)

    # Get latitude and longitude of the address
    lat, lng = get_lat_long(address, api_key)
    if lat is None or lng is None:
        return jsonify({"error": "Could not get the location from the address"}), 400

    # Search for local, non-chain restaurants
    restaurants = find_local_restaurants(lat, lng, api_key, radius)
    if not restaurants:
        return jsonify({"restaurants": [], "message": "No local restaurants found."})

    return jsonify({"restaurants": restaurants})

"""def main():
    api_key = 'AIzaSyCPGl2jds_l8dMrrYObY24QqpIWwfRCX6Y'
    address = request.json.get('location')  # Expecting a JSON payload with 'location'
    #address = '120 New Scotland Ave Albany, NY 12208'
    
    # Get latitude and longitude of the address
    lat, lng = get_lat_long(address, api_key)
    
    if lat is not None and lng is not None:
        # Search for local, non-chain restaurants
        restaurants = find_local_restaurants(lat, lng, api_key)
        
        if restaurants:
            print("Local Restaurants found:")
            for restaurant in restaurants:
                print(f"- Name: {restaurant['name']}")
                print(f"  Address: {restaurant['address']}")
                print(f"  Website: {restaurant['website'] or 'N/A'}")
                print(f"  Rating: {restaurant['rating'] or 'N/A'}")
                print(f"  Price Level: {restaurant['price_level'] or 'N/A'}")
                print(f"  Delivery: {'Yes' if restaurant['delivery'] else 'No'}")
                print(f"  Takeout: {'Yes' if restaurant['takeout'] else 'No'}")
                print(f"  Dine-in: {'Yes' if restaurant['dine_in'] else 'No'}")
                print(f"  Opening Hours: {restaurant['opening_hours'] or 'N/A'}")
                print()
        else:
            print("No local restaurants found.")
    else:
        print("Could not get the location from the address.")"""

if __name__ == "__main__":
    #main()
    app.run(debug=True)


"""
def find_takeaway_restaurants(lat, lng, api_key, radius=500):
    # Use the 'UniqueRestaurantName' filter in the text search query
    places_url = (
        f"https://maps.googleapis.com/maps/api/place/textsearch/json?"
        f"query=takeaway+restaurants+in+the+area&location={lat},{lng}&"
        f"radius={radius}&key={api_key}&unique=true"
    )
    #places_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=takeaway&location={lat},{lng}&radius={radius}&key={api_key}"
    response = requests.get(places_url)
    if response.status_code == 200:
        results = response.json().get('results', [])
        restaurants = []
        for place in results:
            name = place.get('name')
            address = place.get('formatted_address')
            # Fetch place details to get the website
            place_id = place.get('place_id')
            details = get_place_details(place_id, api_key)
            website = details.get('website') if details else None
            restaurants.append({
                'name': name,
                'address': address,
                'website': website
            })
        return restaurants
    return []

def get_place_details(place_id, api_key):
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    response = requests.get(details_url)
    if response.status_code == 200:
        return response.json().get('result', {})
    return {}

def main():
    api_key = 'AIzaSyCPGl2jds_l8dMrrYObY24QqpIWwfRCX6Y'
    address = '120 New Scotland Ave Albany, NY 12208'  # e.g., '1600 Amphitheatre Parkway, Mountain View, CA'
    
    # Get latitude and longitude of the address
    lat, lng = get_lat_long(address, api_key)
    
    if lat is not None and lng is not None:
        # Search for takeaway restaurants
        restaurants = find_takeaway_restaurants(lat, lng, api_key)
        
        if restaurants:
            print("Takeaway Restaurants found:")
            for restaurant in restaurants:
                print(f"- Name: {restaurant['name']}, Address: {restaurant['address']}, Website: {restaurant['website'] or 'N/A'}")
        else:
            print("No takeaway restaurants found.")
    else:
        print("Could not get the location from the address.")

if __name__ == "__main__":
    main()"""

