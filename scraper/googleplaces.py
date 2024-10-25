import requests
from datetime import datetime

# Replace with your own API keys
GOOGLE_API_KEY = 'AIzaSyCPGl2jds_l8dMrrYObY24QqpIWwfRCX6Y'

def get_lat_lng(location):
    """Convert address to latitude and longitude using Google Geocoding API."""
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_API_KEY}"
    response = requests.get(geocode_url).json()
    if response['status'] == 'OK':
        lat = response['results'][0]['geometry']['location']['lat']
        lng = response['results'][0]['geometry']['location']['lng']
        return lat, lng
    else:
        raise Exception("Geocoding API error: " + response['status'])

def find_restaurants(lat, lng, date_time):
    """Find restaurants near given location and filter by open hours."""
    places_url = (f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
                  f"location={lat},{lng}&radius=5000&type=restaurant&key={GOOGLE_API_KEY}")
    
    response = requests.get(places_url).json()
    restaurants = response.get('results', [])

    open_restaurants = []
    current_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S')

    for restaurant in restaurants:
        place_id = restaurant.get('place_id')
        details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={GOOGLE_API_KEY}"
        details_response = requests.get(details_url).json()
        details = details_response.get('result', {})

        opening_hours = details.get('opening_hours', {})
        if 'periods' in opening_hours:
            periods = opening_hours['periods']
            is_open = False

            for period in periods:
                if 'open' in period and 'close' in period:
                    open_time = period['open']['time']
                    close_time = period['close']['time']
                    # Check if current time is within open hours
                    # Simplified for example purposes, assuming the restaurant opens and closes daily at the same time
                    if open_time <= current_time.strftime('%H%M') <= close_time:
                        is_open = True
                        break

            if is_open:
                restaurant_info = {
                    'name': details.get('name'),
                    'rating': details.get('rating'),
                    'distance': restaurant.get('vicinity'),  # Simplified, actual distance calculation can be added
                    'delivery': 'Available' if 'delivery' in details.get('types', []) else 'Not Available',
                    'menu': restaurant.get('menu'),
                    # 'menu': 'Menu details not available through Google Places API',  # Placeholder
                    'website': details.get('website')
                }
                open_restaurants.append(restaurant_info)

    return open_restaurants

def main():
    location = 'Bowen Hills, QLD 4006 Australia'
    date_time = '2024-09-06T12:00:00'

    try:
        lat, lng = get_lat_lng(location)
        restaurants = find_restaurants(lat, lng, date_time)

        print(f"Restaurants open at {date_time} near {location}:")
        print(f"Total: {len(restaurants)} restaurants")

        for restaurant in restaurants:
            print(f"Name: {restaurant['name']}")
            print(f"Rating: {restaurant['rating']}")
            print(f"Distance: {restaurant['distance']}")
            print(f"Delivery: {restaurant['delivery']}")
            print(f"Menu: {restaurant['menu']}")
            print(f"Website: {restaurant['website']}")
            print()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
