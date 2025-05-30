import requests
import json
import csv
import time
import random
from pathlib import Path
import re

class BusinessDataScraper:
    def __init__(self, google_api_key=None):
        """
        Initialize the business scraper with Google Places API
        Get your API key from: https://console.cloud.google.com/apis/credentials
        """
        self.google_api_key = google_api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
        # Search terms for mobile pet grooming
        self.search_terms = [
            "mobile pet grooming",
            "mobile dog grooming", 
            "mobile cat grooming",
            "traveling pet groomer",
            "at home pet grooming",
            "mobile dog washing"
        ]
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def search_google_places(self, query, location, radius=50000):
        """
        Search Google Places API for businesses
        
        Args:
            query: Search query (e.g., "mobile pet grooming")
            location: City name or coordinates
            radius: Search radius in meters (default 50km)
        """
        if not self.google_api_key:
            print("⚠️  Google API key not provided. Using demo data structure...")
            return self._generate_demo_data(location)
        
        # New Places API endpoint
        search_url = f"{self.base_url}/textsearch/json"
        
        params = {
            'query': f"{query} {location}",
            'key': self.google_api_key,
            'type': 'establishment',
            'fields': 'place_id,name,rating,user_ratings_total,formatted_address,formatted_phone_number,website,opening_hours,price_level'
        }
        
        try:
            response = self.session.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'OK':
                return self._process_places_results(data.get('results', []))
            else:
                print(f"❌ Google Places API error: {data.get('status')} - {data.get('error_message', '')}")
                return []
                
        except requests.RequestException as e:
            print(f"❌ Request failed: {e}")
            return []

    def get_place_details(self, place_id):
        """Get detailed information for a specific place"""
        if not self.google_api_key:
            return {}
            
        details_url = f"{self.base_url}/details/json"
        
        params = {
            'place_id': place_id,
            'key': self.google_api_key,
            'fields': 'name,rating,user_ratings_total,formatted_address,formatted_phone_number,website,opening_hours,price_level,reviews,photos,business_status'
        }
        
        try:
            response = self.session.get(details_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'OK':
                return data.get('result', {})
            else:
                print(f"❌ Place details error: {data.get('status')}")
                return {}
                
        except requests.RequestException as e:
            print(f"❌ Details request failed: {e}")
            return {}

    def _process_places_results(self, results):
        """Process and clean Google Places results"""
        businesses = []
        
        for place in results:
            # Filter for mobile grooming businesses
            name = place.get('name', '').lower()
            if any(term in name for term in ['mobile', 'traveling', 'home', 'door']):
                
                business = {
                    'name': place.get('name'),
                    'rating': place.get('rating', 0),
                    'review_count': place.get('user_ratings_total', 0),
                    'address': place.get('formatted_address'),
                    'phone': place.get('formatted_phone_number'),
                    'website': place.get('website'),
                    'place_id': place.get('place_id'),
                    'price_level': place.get('price_level'),
                    'business_status': place.get('business_status', 'OPERATIONAL')
                }
                
                # Get additional details if place_id exists
                if place.get('place_id'):
                    details = self.get_place_details(place['place_id'])
                    if details:
                        business.update({
                            'hours': self._format_hours(details.get('opening_hours')),
                            'reviews': self._extract_reviews(details.get('reviews', [])),
                            'services': self._extract_services(details.get('name', '') + ' ' + ' '.join([r.get('text', '') for r in details.get('reviews', [])[:3]]))
                        })
                
                businesses.append(business)
                
                # Add delay to respect API limits
                time.sleep(0.1)
        
        return businesses

    def _format_hours(self, opening_hours):
        """Format opening hours data"""
        if not opening_hours or not opening_hours.get('weekday_text'):
            return "Hours vary - call for availability"
        
        return opening_hours['weekday_text'][0] if opening_hours['weekday_text'] else "Call for hours"

    def _extract_reviews(self, reviews):
        """Extract relevant review snippets"""
        if not reviews:
            return []
        
        review_texts = []
        for review in reviews[:3]:  # Top 3 reviews
            text = review.get('text', '')
            if len(text) > 50:  # Only meaningful reviews
                review_texts.append({
                    'text': text[:200] + '...' if len(text) > 200 else text,
                    'rating': review.get('rating', 5),
                    'author': review.get('author_name', 'Customer')
                })
        
        return review_texts

    def _extract_services(self, text):
        """Extract services from business name and reviews"""
        services = []
        text_lower = text.lower()
        
        service_keywords = {
            'Full-service grooming': ['full service', 'complete grooming', 'full grooming'],
            'Bath and brush': ['bath', 'wash', 'shampoo'],
            'Nail trimming': ['nail', 'nails', 'claw'],
            'Ear cleaning': ['ear', 'ears'],
            'Teeth cleaning': ['teeth', 'dental'],
            'De-shedding': ['shedding', 'deshed', 'undercoat'],
            'Flea treatment': ['flea', 'tick', 'parasite'],
            'De-matting': ['mat', 'matting', 'tangle']
        }
        
        for service, keywords in service_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                services.append(service)
        
        # Default services if none detected
        if not services:
            services = ['Full-service grooming', 'Bath and brush', 'Nail trimming']
        
        return services[:4]  # Limit to 4 services

    def _generate_demo_data(self, location):
        """Generate demo data structure when API is not available"""
        print(f"📋 Generating demo data structure for {location}...")
        
        demo_businesses = [
            {
                'name': f'{location} Mobile Pet Spa',
                'rating': 4.7,
                'review_count': 156,
                'address': f'{location}, {location.split()[-1]}',
                'phone': f'({random.randint(200, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}',
                'website': f'https://{location.lower().replace(" ", "")}mobilepetspa.com',
                'hours': 'Mon-Sat 8AM-6PM',
                'services': ['Full-service grooming', 'Bath and brush', 'Nail trimming', 'Ear cleaning'],
                'price_range': '$60-120',
                'reviews': [
                    {'text': 'Amazing service! My dog loves the mobile grooming experience.', 'rating': 5, 'author': 'Sarah M.'},
                    {'text': 'Professional and convenient. Highly recommend!', 'rating': 5, 'author': 'Mike R.'}
                ]
            }
        ]
        
        return demo_businesses

    def scrape_city_businesses(self, city, state):
        """Scrape all mobile pet grooming businesses for a city"""
        print(f"🔍 Searching for mobile pet groomers in {city}, {state}...")
        
        all_businesses = []
        location = f"{city}, {state}"
        
        # Search with different terms to get comprehensive results
        for term in self.search_terms:
            print(f"   Searching: {term}")
            businesses = self.search_google_places(term, location)
            all_businesses.extend(businesses)
            
            # Add delay between searches
            time.sleep(1)
        
        # Remove duplicates based on name and phone
        unique_businesses = []
        seen = set()
        
        for business in all_businesses:
            identifier = (business.get('name', ''), business.get('phone', ''))
            if identifier not in seen:
                seen.add(identifier)
                unique_businesses.append(business)
        
        print(f"✅ Found {len(unique_businesses)} unique mobile groomers in {city}")
        return unique_businesses

    def scrape_multiple_cities(self, cities_csv, output_file='scraped_businesses.json'):
        """Scrape businesses for multiple cities from CSV"""
        all_data = {}
        
        with open(cities_csv, 'r') as f:
            reader = csv.DictReader(f)
            cities = list(reader)
        
        for city_data in cities:
            city = city_data['city']
            state = city_data['state']
            
            businesses = self.scrape_city_businesses(city, state)
            all_data[f"{city}, {state}"] = businesses
            
            # Save progress after each city
            with open(output_file, 'w') as f:
                json.dump(all_data, f, indent=2)
            
            print(f"💾 Saved data for {city}")
            
            # Rate limiting - respect API quotas
            time.sleep(2)
        
        print(f"🎉 Scraping complete! Data saved to {output_file}")
        return all_data

    def validate_business_data(self, business):
        """Validate and clean business data"""
        # Required fields
        if not business.get('name') or not business.get('phone'):
            return False
        
        # Clean phone number
        if business.get('phone'):
            phone = re.sub(r'[^\d\(\)\-\s\+]', '', business['phone'])
            business['phone'] = phone
        
        # Ensure rating is reasonable
        if business.get('rating'):
            business['rating'] = max(0, min(5, float(business['rating'])))
        
        # Ensure services list
        if not business.get('services'):
            business['services'] = ['Mobile grooming', 'Bath and brush', 'Nail trimming']
        
        return True

# Example usage
if __name__ == "__main__":
    print("🚀 Mobile Pet Grooming Business Scraper")
    print("=" * 50)
    
    # Use provided API key
    api_key = "AIzaSyCQOSRXIO51fs9Gc-qtNd9GQcTGecmPX2Q"
    print(f"✅ Using provided Google Places API key")
    
    scraper = BusinessDataScraper(api_key)
    
    # Create sample cities file if it doesn't exist
    cities_file = 'cities.csv'
    if not Path(cities_file).exists():
        sample_cities = """city,state,state_abbr
Princeton,Texas,TX
Plano,Texas,TX
Scottsdale,Arizona,AZ
Raleigh,North Carolina,NC
Austin,Texas,TX
Denver,Colorado,CO
Tampa,Florida,FL
Nashville,Tennessee,TN
Phoenix,Arizona,AZ
Portland,Oregon,OR
Charlotte,North Carolina,NC
San Diego,California,CA
Las Vegas,Nevada,NV
Miami,Florida,FL
Seattle,Washington,WA
Atlanta,Georgia,GA
Minneapolis,Minnesota,MN
Orlando,Florida,FL
San Antonio,Texas,TX
Jacksonville,Florida,FL
Fort Worth,Texas,TX
Oklahoma City,Oklahoma,OK
Louisville,Kentucky,KY
Memphis,Tennessee,TN
Richmond,Virginia,VA"""
        
        with open(cities_file, 'w') as f:
            f.write(sample_cities)
        print(f"📄 Created {cities_file} with sample cities")
    
    # Start scraping
    data = scraper.scrape_multiple_cities(cities_file)
    print(f"\n✅ Scraping complete! Found businesses in {len(data)} cities")
    
    # Show sample of what we found
    for location, businesses in list(data.items())[:2]:
        print(f"\n📍 {location}: {len(businesses)} businesses")
        for biz in businesses[:2]:
            print(f"   - {biz.get('name')} ({biz.get('rating', 'N/A')}⭐)")