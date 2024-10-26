import requests


# latitude = 19.1334
# longitude = 72.9133
# place_type = "hospital"

# Your Google Places API Key
api_key = "AIzaSyChyTUIAlaNqY5QK8tvcmlPMY6WqvF3E4c"
radius = 5000  # Radius in meters (5 km)
# Define the endpoint
def get_help(latitude, longitude, place_type):

    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={latitude},{longitude}"
        f"&radius={radius}"
        f"&type={place_type}"
        f"&key={api_key}"
    )

    # Make the request to Google Places API
    response = requests.get(url)
    results = response.json().get("results", [])

    print("Response Status:", response.status_code)
    if response.status_code != 200:
        print("Error:", response.text)
    else:
        # Parse JSON response
        results = response.json().get("results", [])
        print("Number of results:", len(results))

    places_info = []
    # Parse and display the names and locations of nearby hospitals
    for place in results:
        name = place.get("name")
        address = place.get("vicinity")
        place_lat = place["geometry"]["location"]["lat"]
        place_lng = place["geometry"]["location"]["lng"]
        place_id = place.get("place_id")
    
        if place_id:
                details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
                details_response = requests.get(details_url)
                details_data = details_response.json().get("result", {})
                
                # Extract phone number if available
                phone_number = details_data.get("formatted_phone_number", "Phone number not available")

                # Display place information
                print(f"Name: {name}")
                print(f"Address: {address}")
                print(f"Location: ({place_lat}, {place_lng})")
                print(f"Phone: {phone_number}")
                print("-" * 40)

                places_info.append({
                        "Name": name,
                        "Address": address,
                        "Location": {"latitude": place_lat, 
                                     "longitude": place_lng
                                     },
                        "Phone": phone_number,
                    })

    # Return the list of places as a JSON response
    return places_info
