import datetime
import requests
import csv
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
if not API_KEY:
    raise ValueError("GOOGLE_MAPS_API_KEY not found in .env file. Please add it to your .env file.")

LOCATION = '43.6532,-79.3832'  # Toronto
RADIUS = 50000  # Maximum allowed radius in meters

# API endpoints
SEARCH_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

# Business types to search for
BUSINESS_TYPES = [
    "restaurant", "cafe", "bar", "store", "shop", "bakery", "beauty_salon", 
    "hair_care", "gym", "spa", "clothing_store", "shoe_store", "jewelry_store", 
    "furniture_store", "home_goods_store", "hardware_store", "electronics_store",
    "food", "grocery_or_supermarket", "supermarket", "convenience_store",
    "accounting", "lawyer", "dentist", "doctor", "physiotherapist", "insurance_agency",
    "car_dealer", "car_repair", "gas_station", "lodging", "real_estate_agency"
]

# Keywords for additional searches
KEYWORDS = ["business", "service", "shop", "store", "repair", "local"]

def search_places(location, radius, type=None, keyword=None):
    """Search for places with optional type and keyword parameters"""
    unique_places = {}
    params = {
        "location": location,
        "radius": radius,
        "key": API_KEY
    }
    
    if type:
        params["type"] = type
    
    if keyword:
        params["keyword"] = keyword

    page_count = 0
    total_added = 0
    
    while True:
        response = requests.get(SEARCH_URL, params=params).json()
        places = response.get("results", [])
        
        page_count += 1
        print(f"Processing page {page_count} with {len(places)} places found")
        
        for place in places:
            place_id = place["place_id"]
            
            # Skip if we've already processed this place
            if place_id in unique_places:
                continue
                
            rating = place.get("rating", 0)
            reviews = place.get("user_ratings_total", 0)

            # Filter businesses with rating ≤ 4.0 OR reviews < 100
            if rating <= 4.0 or reviews < 100:
                details = get_place_details(place_id)
                time.sleep(0.2)  # avoid rate limiting
                
                unique_places[place_id] = {
                    "name": details.get("name"),
                    "rating": details.get("rating"),
                    "reviews": details.get("user_ratings_total"),
                    "address": details.get("formatted_address"),
                    "website": details.get("website", ""),
                    "type": ", ".join(details.get("types", [])),
                    "lat": details.get("geometry", {}).get("location", {}).get("lat"),
                    "lng": details.get("geometry", {}).get("location", {}).get("lng"),
                }
                total_added += 1
                
                if total_added % 10 == 0:
                    print(f"Added {total_added} places to results")

        if "next_page_token" in response:
            time.sleep(2)  # Google requires a delay before using the token
            params["pagetoken"] = response["next_page_token"]
        else:
            break
            
    return unique_places

def get_place_details(place_id):
    """Get extra info like website and formatted address"""
    detail_params = {
        "place_id": place_id,
        "fields": "name,rating,user_ratings_total,website,formatted_address,types,geometry",
        "key": API_KEY
    }
    response = requests.get(DETAILS_URL, params=detail_params).json()
    return response.get("result", {})

# Collect all unique places
all_places = {}

# Search by business type
for business_type in BUSINESS_TYPES:
    print(f"\nSearching for business type: {business_type}")
    places = search_places(LOCATION, RADIUS, type=business_type)
    all_places.update(places)
    print(f"Total unique places so far: {len(all_places)}")
    time.sleep(1)  # Avoid hitting rate limits

# Search by keywords for additional coverage
for keyword in KEYWORDS:
    print(f"\nSearching with keyword: {keyword}")
    places = search_places(LOCATION, RADIUS, keyword=keyword)
    all_places.update(places)
    print(f"Total unique places so far: {len(all_places)}")
    time.sleep(1)  # Avoid hitting rate limits

# Convert dictionary to list for CSV export
results = list(all_places.values())

# Export to CSV
filename = f"leads.csv"
with open(filename, "w", newline='', encoding="utf-8") as f:
    if results:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

print(f"Saved {len(results)} leads to leads.csv")
