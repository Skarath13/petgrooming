#!/usr/bin/env python3
"""
Enhance business data with phone numbers and websites using Google Places API
"""
import json
import requests
import time
from pathlib import Path

API_KEY = "AIzaSyCQOSRXIO51fs9Gc-qtNd9GQcTGecmPX2Q"

def get_place_details(place_id):
    """Get detailed information for a place including phone and website"""
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    params = {
        'place_id': place_id,
        'fields': 'formatted_phone_number,website,url',
        'key': API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'OK':
            result = data.get('result', {})
            return {
                'phone': result.get('formatted_phone_number'),
                'website': result.get('website'),
                'google_url': result.get('url')
            }
        else:
            print(f"API Error for {place_id}: {data.get('status')}")
            return {'phone': None, 'website': None, 'google_url': None}
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {place_id}: {e}")
        return {'phone': None, 'website': None, 'google_url': None}

def enhance_businesses_data():
    """Enhance all businesses with phone and website data"""
    
    # Load existing data
    with open('scraped_businesses.json', 'r') as f:
        businesses_data = json.load(f)
    
    total_businesses = sum(len(businesses) for businesses in businesses_data.values())
    processed = 0
    enhanced = 0
    
    print(f"🚀 Enhancing {total_businesses} businesses with contact information...")
    
    for city_name, businesses in businesses_data.items():
        print(f"\n📍 Processing {city_name} ({len(businesses)} businesses)")
        
        for business in businesses:
            place_id = business.get('place_id')
            if not place_id:
                processed += 1
                continue
                
            print(f"  📞 Getting contact info for: {business['name'][:50]}...")
            
            # Get enhanced details
            details = get_place_details(place_id)
            
            # Update business with new data
            if details['phone']:
                business['phone'] = details['phone']
                print(f"    ✅ Found phone: {details['phone']}")
                enhanced += 1
            
            if details['website']:
                business['website'] = details['website']
                print(f"    ✅ Found website: {details['website'][:50]}...")
                enhanced += 1
                
            if details['google_url']:
                business['google_url'] = details['google_url']
            
            processed += 1
            
            # Rate limiting - Google allows 10 requests per second
            time.sleep(0.1)
            
            # Progress update
            if processed % 10 == 0:
                print(f"  📊 Progress: {processed}/{total_businesses} ({enhanced} enhanced)")
    
    # Save enhanced data
    with open('enhanced_businesses.json', 'w') as f:
        json.dump(businesses_data, f, indent=2)
    
    print(f"\n🎉 Enhancement complete!")
    print(f"📊 Processed: {processed}/{total_businesses} businesses")
    print(f"📞 Enhanced with contact info: {enhanced} businesses")
    print(f"💾 Saved to: enhanced_businesses.json")

def create_sample_enhanced_data():
    """Create sample data with some phone/website info for testing"""
    with open('scraped_businesses.json', 'r') as f:
        businesses_data = json.load(f)
    
    # Add sample contact info to a few businesses for testing
    sample_phones = [
        "(512) 555-0123",
        "(214) 555-0456", 
        "(469) 555-0789",
        "(972) 555-0321"
    ]
    
    sample_websites = [
        "https://luxurymobilegrooming.com",
        "https://royalspaw.com",
        "https://lakewaygrooming.com",
        "https://mobilepetcare.net"
    ]
    
    count = 0
    for city_businesses in businesses_data.values():
        for i, business in enumerate(city_businesses[:2]):  # Add to first 2 in each city
            if count < len(sample_phones):
                business['phone'] = sample_phones[count % len(sample_phones)]
            if count < len(sample_websites):
                business['website'] = sample_websites[count % len(sample_websites)]
            count += 1
    
    # Save sample data
    with open('enhanced_businesses.json', 'w') as f:
        json.dump(businesses_data, f, indent=2)
    
    print("✅ Created sample enhanced data for testing")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "sample":
        create_sample_enhanced_data()
    else:
        enhance_businesses_data()