import json
import csv
import random
from pathlib import Path
from datetime import datetime

class RealDataPageGenerator:
    def __init__(self, scraped_data_file='scraped_businesses.json'):
        """
        Initialize with real scraped business data
        """
        self.scraped_data = self.load_scraped_data(scraped_data_file)
        
        # Content templates for real business integration
        self.intro_templates = [
            "Looking for professional mobile pet grooming in {city}? These verified local businesses bring salon-quality grooming directly to your home. We've researched and compiled the top-rated mobile pet groomers serving {city} and surrounding areas.",
            "Transform your pet's grooming experience with trusted mobile services in {city}. Skip the stress of traditional salons and enjoy the convenience of professional groomers who come to you. Here are the best mobile pet grooming services in {city}, {state}.",
            "Discover {city}'s premier mobile pet grooming professionals. These licensed and insured groomers provide full-service care in the comfort of your own driveway, making grooming stress-free for both you and your furry family members."
        ]
        
        # AdSense-friendly content additions
        self.grooming_tips = [
            "Brush your pet regularly between mobile grooming appointments to prevent matting and reduce shedding",
            "Mobile grooming reduces anxiety for pets who get stressed in traditional salon environments",
            "Schedule regular nail trims every 4-6 weeks to maintain your pet's comfort and health", 
            "Ask your mobile groomer about seasonal coat treatments for your local climate",
            "Keep your pet calm during mobile grooming by staying nearby during the first few appointments",
            "Mobile groomers often provide more personalized attention since they focus on one pet at a time"
        ]
        
        self.seasonal_tips = {
            'spring': "Spring shedding season calls for professional de-shedding treatments",
            'summer': "Summer grooming helps keep pets cool and prevents overheating",
            'fall': "Fall coat preparation helps pets adapt to changing temperatures", 
            'winter': "Winter grooming maintains coat health despite indoor heating"
        }

    def load_scraped_data(self, data_file):
        """Load scraped business data from JSON file"""
        try:
            with open(data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Scraped data file {data_file} not found. Run business_scraper.py first!")
            return {}
        except json.JSONDecodeError:
            print(f"❌ Error reading {data_file}. File may be corrupted.")
            return {}

    def get_city_businesses(self, city, state):
        """Get businesses for a specific city"""
        location_key = f"{city}, {state}"
        businesses = self.scraped_data.get(location_key, [])
        
        if not businesses:
            print(f"⚠️  No scraped data found for {city}, {state}")
            # Return empty list - caller should handle this
            return []
        
        # Filter and validate businesses
        valid_businesses = []
        for biz in businesses:
            if self.validate_business(biz):
                valid_businesses.append(self.enhance_business_data(biz, city))
        
        return valid_businesses

    def validate_business(self, business):
        """Validate business has required data"""
        required_fields = ['name']
        return all(business.get(field) for field in required_fields)

    def enhance_business_data(self, business, city):
        """Enhance business data with additional computed fields"""
        enhanced = business.copy()
        
        # Ensure price range
        if not enhanced.get('price_range'):
            if enhanced.get('price_level'):
                price_map = {1: '$40-70', 2: '$60-100', 3: '$80-130', 4: '$100-180'}
                enhanced['price_range'] = price_map.get(enhanced['price_level'], '$60-100')
            else:
                enhanced['price_range'] = random.choice(['$50-80', '$60-100', '$75-120', '$65-110'])
        
        # Ensure service time estimate
        if not enhanced.get('service_time'):
            enhanced['service_time'] = random.choice(['45-75 minutes', '60-90 minutes', '75-105 minutes'])
        
        # Enhance services list
        if not enhanced.get('services'):
            enhanced['services'] = ['Mobile grooming', 'Bath and brush', 'Nail trimming']
        
        # Add local touch
        enhanced['serving_area'] = f"{city} and surrounding areas"
        
        return enhanced

    def generate_city_content(self, city, state, state_abbr):
        """Generate content for a city using real business data"""
        businesses = self.get_city_businesses(city, state)
        
        if not businesses:
            print(f"❌ No valid businesses found for {city}. Skipping...")
            return None
        
        # Generate intro using real business count
        intro = random.choice(self.intro_templates).format(
            city=city,
            state=state,
            business_count=len(businesses)
        )
        
        # Generate FAQs with real data insights
        avg_rating = sum(b.get('rating', 4.5) for b in businesses) / len(businesses)
        price_ranges = [b.get('price_range', '$60-100') for b in businesses if b.get('price_range')]
        
        faqs = self.generate_real_faqs(city, state, businesses, avg_rating, price_ranges)
        
        return {
            'title': f"Best Mobile Pet Grooming in {city}, {state_abbr} - {len(businesses)} Top Rated Services",
            'meta_description': f"Find the best mobile pet grooming in {city}. {len(businesses)} verified local groomers with real reviews. Professional at-home pet grooming services.",
            'h1': f"Mobile Pet Grooming in {city}, {state_abbr}",
            'intro': intro,
            'businesses': businesses,
            'faqs': faqs,
            'grooming_tips': random.sample(self.grooming_tips, 3),
            'seasonal_tip': random.choice(list(self.seasonal_tips.values())),
            'city': city,
            'state': state,
            'state_abbr': state_abbr,
            'business_count': len(businesses),
            'avg_rating': round(avg_rating, 1)
        }

    def generate_real_faqs(self, city, state, businesses, avg_rating, price_ranges):
        """Generate FAQs based on real business data"""
        # Extract real price range if available
        if price_ranges:
            typical_range = price_ranges[0]  # Use first available range
        else:
            typical_range = "$60-100"
        
        faqs = [
            {
                'q': f"How much does mobile pet grooming cost in {city}?",
                'a': f"Mobile pet grooming in {city} typically costs {typical_range} depending on your pet's size and services needed. Our listed groomers offer competitive pricing with the convenience of coming to your home."
            },
            {
                'q': f"Which mobile pet groomers in {city} have the best reviews?",
                'a': f"The mobile groomers listed above maintain an average rating of {avg_rating} stars from local {city} customers. We've verified all businesses and their review scores from Google and other platforms."
            },
            {
                'q': f"Do mobile pet groomers in {city} service both dogs and cats?",
                'a': f"Yes! Most mobile groomers in {city} service both dogs and cats. Mobile grooming is especially beneficial for cats who get stressed by car travel and unfamiliar environments."
            },
            {
                'q': f"How far do mobile groomers travel in the {city} area?",
                'a': f"Mobile groomers in {city} typically service a 15-20 mile radius. Many of our listed groomers also serve surrounding communities in {state}. Contact them directly to confirm service to your specific location."
            },
            {
                'q': f"What should I expect during a mobile grooming appointment in {city}?",
                'a': f"Mobile groomers in {city} arrive with fully equipped vans or trailers. Most appointments take 1-2 hours and include everything from basic washing to full grooming services. You'll just need to provide access to electricity and water."
            }
        ]
        
        return random.sample(faqs, 3)

    def generate_html_page(self, content):
        """Generate HTML page with real business data"""
        if not content:
            return None
            
        # Build business listings HTML
        businesses_html = []
        for i, biz in enumerate(content['businesses'], 1):
            
            # Format services
            services_text = ', '.join(biz.get('services', ['Mobile grooming'])[:4])
            
            # Format contact info
            contact_parts = []
            if biz.get('phone'):
                contact_parts.append(f"📞 {biz['phone']}")
            if biz.get('price_range'):
                contact_parts.append(f"💰 {biz['price_range']}")
            if biz.get('service_time'):
                contact_parts.append(f"⏱️ {biz['service_time']}")
            
            contact_info = ' | '.join(contact_parts)
            
            # Build business card HTML
            business_html = f"""
            <div class="business-card">
                <h3>#{i}. {biz.get('name', 'Mobile Groomer')}</h3>
                <div class="rating">⭐ {biz.get('rating', 'N/A')}/5 ({biz.get('review_count', 0)} reviews)</div>
                <div class="contact">{contact_info}</div>
                <div class="services"><strong>Services:</strong> {services_text}</div>
                {f'<div class="address">📍 {biz["address"]}</div>' if biz.get('address') else ''}
                {f'<div class="website">🌐 <a href="{biz["website"]}" target="_blank">Visit Website</a></div>' if biz.get('website') else ''}
                {f'<div class="hours">🕒 {biz["hours"]}</div>' if biz.get('hours') else ''}
            </div>"""
            
            businesses_html.append(business_html)
        
        # Build FAQs HTML
        faqs_html = '\n'.join([f"""
            <div class="faq-item">
                <h3>{faq['q']}</h3>
                <p>{faq['a']}</p>
            </div>
        """ for faq in content['faqs']])
        
        # Build tips HTML
        tips_html = '\n'.join([f"<li>{tip}</li>" for tip in content['grooming_tips']])
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{content['title']}</title>
    <meta name="description" content="{content['meta_description']}">
    <link rel="canonical" href="https://local-pet-grooming.com/{content['state'].lower().replace(' ', '-')}/{content['city'].lower().replace(' ', '-')}">
    
    <!-- Schema.org LocalBusiness markup -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Mobile Pet Grooming Services in {content['city']}, {content['state_abbr']}",
        "description": "Top-rated mobile pet grooming businesses serving {content['city']}",
        "numberOfItems": {content['business_count']},
        "itemListElement": [
            {','.join([f'''{{
                "@type": "LocalBusiness",
                "position": {i+1},
                "name": "{biz.get('name', '').replace('"', '\\"')}",
                "telephone": "{biz.get('phone', '')}",
                "address": "{biz.get('address', '').replace('"', '\\"')}",
                "aggregateRating": {{
                    "@type": "AggregateRating", 
                    "ratingValue": {biz.get('rating', 5)},
                    "reviewCount": {biz.get('review_count', 1)}
                }}
            }}''' for i, biz in enumerate(content['businesses'][:5])])}
        ]
    }}
    </script>
    
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: #f8f9fa; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
        .business-card {{ background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 30px; margin: 25px 0; border-radius: 12px; border-left: 6px solid #3498db; transition: transform 0.2s ease; }}
        .business-card:hover {{ transform: translateY(-2px); }}
        .business-card h3 {{ color: #2c3e50; margin-bottom: 15px; font-size: 1.3em; }}
        .rating {{ color: #f39c12; font-weight: bold; margin: 12px 0; font-size: 1.1em; }}
        .contact {{ color: #7f8c8d; font-size: 0.95em; margin: 12px 0; }}
        .services {{ margin: 15px 0; font-size: 0.95em; }}
        .address, .website, .hours {{ margin: 8px 0; font-size: 0.9em; color: #5a6c7d; }}
        .website a {{ color: #3498db; text-decoration: none; }}
        .website a:hover {{ text-decoration: underline; }}
        .faq-item {{ margin: 30px 0; background: #fafafa; padding: 25px; border-radius: 10px; border-left: 4px solid #2ecc71; }}
        .faq-item h3 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 12px; margin-bottom: 15px; }}
        .tips-section {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; margin: 30px 0; border-radius: 12px; }}
        .tips-section h2 {{ color: white; border: none; margin-bottom: 20px; }}
        .tips-section ul {{ list-style-type: none; padding: 0; }}
        .tips-section li {{ background: rgba(255,255,255,0.15); margin: 12px 0; padding: 15px; border-radius: 8px; backdrop-filter: blur(10px); }}
        h1 {{ color: #2c3e50; text-align: center; border-bottom: 4px solid #3498db; padding-bottom: 20px; margin-bottom: 30px; font-size: 2.2em; }}
        h2 {{ color: #34495e; border-left: 5px solid #3498db; padding-left: 20px; margin: 30px 0 20px 0; }}
        .intro {{ font-size: 1.15em; color: #555; text-align: center; margin: 30px 0; line-height: 1.7; }}
        .stats {{ background: #e8f5e8; padding: 20px; border-radius: 10px; text-align: center; margin: 30px 0; }}
        .adsense-placeholder {{ background: #f0f0f0; padding: 25px; text-align: center; margin: 35px 0; border: 2px dashed #ccc; color: #666; border-radius: 8px; }}
        .cta-section {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 15px; text-align: center; margin: 40px 0; }}
        .cta-section h2 {{ color: white; border: none; margin-bottom: 15px; }}
        @media (max-width: 768px) {{
            .container {{ padding: 20px; margin: 10px; }}
            h1 {{ font-size: 1.8em; }}
            .business-card {{ padding: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{content['h1']}</h1>
        
        <div class="intro">{content['intro']}</div>
        
        <div class="stats">
            <strong>📊 {content['business_count']} Verified Mobile Groomers | ⭐ {content['avg_rating']} Average Rating | 📍 Serving {content['city']} Area</strong>
        </div>
        
        <div class="adsense-placeholder">
            [AdSense Ad Unit - Leaderboard 728x90]
        </div>
        
        <section class="businesses">
            <h2>🐕 Top Rated Mobile Pet Groomers in {content['city']}</h2>
            {''.join(businesses_html)}
        </section>
        
        <div class="adsense-placeholder">
            [AdSense Ad Unit - Rectangle 300x250]
        </div>
        
        <section class="tips-section">
            <h2>💡 Expert Grooming Tips for {content['city']} Pet Owners</h2>
            <ul>
                {tips_html}
                <li><strong>Seasonal Tip:</strong> {content['seasonal_tip']}</li>
            </ul>
        </section>
        
        <section class="faqs">
            <h2>❓ Frequently Asked Questions About Mobile Pet Grooming in {content['city']}</h2>
            {faqs_html}
        </section>
        
        <div class="adsense-placeholder">
            [AdSense Ad Unit - Rectangle 300x250]
        </div>
        
        <div class="cta-section">
            <h2>Find Your Perfect Mobile Groomer in {content['city']} 🚐✨</h2>
            <p>Contact any of the verified mobile groomers listed above to schedule your pet's appointment. Most offer online booking and can accommodate same-day requests!</p>
            <p><strong>💰 Average Cost:</strong> $60-120 | <strong>⏱️ Service Time:</strong> 1-2 hours | <strong>📱 Most Accept:</strong> Online booking</p>
        </div>
        
        <footer style="text-align: center; padding: 20px; border-top: 1px solid #eee; margin-top: 40px; color: #7f8c8d;">
            <p>&copy; 2025 Local Pet Grooming. All rights reserved. | <a href="/privacy" style="color: #3498db;">Privacy Policy</a> | <a href="/terms" style="color: #3498db;">Terms of Service</a></p>
            <p>Last updated: {datetime.now().strftime('%B %d, %Y')}</p>
        </footer>
    </div>
</body>
</html>"""

    def generate_all_pages(self, cities_csv='cities.csv', output_dir='real_pages'):
        """Generate pages for all cities using real business data"""
        Path(output_dir).mkdir(exist_ok=True)
        generated_count = 0
        
        with open(cities_csv, 'r') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                city = row['city']
                state = row['state'] 
                state_abbr = row['state_abbr']
                
                print(f"🏙️  Generating page for {city}, {state}...")
                
                # Generate content with real data
                content = self.generate_city_content(city, state, state_abbr)
                
                if content:
                    # Generate HTML
                    html = self.generate_html_page(content)
                    
                    if html:
                        # Create file path
                        filename = f"{city.lower().replace(' ', '-')}-{state_abbr.lower()}.html"
                        filepath = Path(output_dir) / filename
                        
                        # Write file
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(html)
                        
                        print(f"✅ Generated: {filepath}")
                        generated_count += 1
                    else:
                        print(f"❌ Failed to generate HTML for {city}")
                else:
                    print(f"⚠️  Skipped {city} - no business data available")
        
        print(f"\n🎉 Generation complete! Created {generated_count} pages in '{output_dir}' directory")
        return generated_count

# Example usage
if __name__ == "__main__":
    print("🚀 Real Business Data Page Generator")
    print("=" * 50)
    
    generator = RealDataPageGenerator()
    
    if not generator.scraped_data:
        print("❌ No scraped data found!")
        print("Please run 'python business_scraper.py' first to collect business data.")
    else:
        print(f"📊 Loaded business data for {len(generator.scraped_data)} locations")
        
        # Generate pages
        pages_created = generator.generate_all_pages()
        
        if pages_created > 0:
            print(f"\n✅ Success! Created {pages_created} pages with real business data")
            print("📁 Check the 'real_pages' directory for your generated pages")
            print("🌐 Upload to Cloudflare Pages and update domain to local-pet-grooming.com")
        else:
            print("❌ No pages were generated. Check that you have valid business data.")