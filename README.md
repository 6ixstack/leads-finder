# Business Lead Generator

This tool identifies potential business leads in a specified geographic area by finding businesses with lower ratings (≤ 4.0) or fewer reviews (<100) using the Google Places API.

## What This Tool Does

- Searches for businesses in a specified location (default: Toronto) within a defined radius
- Filters for businesses with ratings of 4.0 or lower OR less than 100 reviews
- Searches across multiple business types and keywords to maximize results
- Avoids duplicates by tracking unique place IDs
- Exports results to a CSV file with business details including:
  - Business name
  - Rating
  - Number of reviews
  - Address
  - Website URL
  - Business types
  - Geographic coordinates

## Getting a Google Places API Key

To use this script, you need a Google Places API key:

1. **Create a Google Cloud Account**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Sign in with your Google account or create one

2. **Create a New Project**
   - Click on the project dropdown at the top of the page
   - Click "New Project"
   - Enter a project name and click "Create"

3. **Enable the Places API**
   - From the dashboard, navigate to "APIs & Services" > "Library"
   - Search for "Places API"
   - Select "Places API" from the results
   - Click "Enable"

4. **Create an API Key**
   - Navigate to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API key"
   - Your new API key will be displayed

5. **Restrict Your API Key** (Recommended)
   - In the credentials page, find your key and click "Edit"
   - Under "Application restrictions," choose "HTTP referrers" or "IP addresses" as appropriate
   - Under "API restrictions," restrict the key to only the `Places API` (The default will be `Places API (New)`, ensure `Places API` is also selected)
   - Click "Save"

## Setup and Usage

1. **Install Requirements**
   ```bash
    pip install -r requirements.txt
   ```

2. **Configure the Script**
   - Replace the API_KEY value with your Google Places API key
   - Optionally modify:
     - LOCATION (default: Toronto)
     - RADIUS (default: 50,000 meters)
     - BUSINESS_TYPES list to target specific business categories
     - KEYWORDS list to add search terms

3. **Create a .env file**
   - Create a file called .env and put the api key like - 
   GOOGLE_MAPS_API_KEY={API KEY HERE}

4. **Run the Script**
   ```bash
   python leads.py
   ```

5. **Results**
   - The script will display progress as it searches
   - Results will be saved to `leads.csv` in the same directory
   - The CSV can be opened in Excel, Google Sheets, or any spreadsheet software

## Notes

- The Google Places API has usage limits and may incur costs beyond the free tier
- If you hit rate limits, the script may fail - consider adding longer delays between requests
- The maximum radius for the Places API is 50,000 meters (50 km)

## Usage Cost Considerations

Google Places API is not free beyond a certain usage threshold:
- You get $200 equivalent credit per month (as of time of writing)
- Nearby Search requests cost $0.032 per request (first 1000 free per month)
- Place Details requests cost $0.017 per request (first 1000 free per month)

Monitor your usage in the Google Cloud Console to avoid unexpected charges.
