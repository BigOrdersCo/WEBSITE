import requests

def get_lat_long(address, api_key):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(geocode_url)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            location = results[0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None

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
    address = '30 Tank St, Brisbane, QLD, Australia 4006'  # e.g., '1600 Amphitheatre Parkway, Mountain View, CA'
    
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
    main()
