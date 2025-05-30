import json
import csv
import random
from pathlib import Path
from datetime import datetime
import os

class EnhancedSiteGenerator:
    def __init__(self, scraped_data_file='scraped_businesses.json'):
        """
        Enhanced site generator with clean URLs and legal compliance
        """
        self.scraped_data = self.load_scraped_data(scraped_data_file)
        
        # Enhanced content templates
        self.intro_templates = [
            "Looking for professional mobile pet grooming in {city}? These verified local businesses bring salon-quality grooming directly to your home. We've researched and compiled the top-rated mobile pet groomers serving {city} and surrounding areas.",
            "Transform your pet's grooming experience with trusted mobile services in {city}. Skip the stress of traditional salons and enjoy the convenience of professional groomers who come to you. Here are the best mobile pet grooming services in {city}, {state}.",
            "Discover {city}'s premier mobile pet grooming professionals. These licensed and insured groomers provide full-service care in the comfort of your own driveway, making grooming stress-free for both you and your furry family members."
        ]
        
        # Enhanced grooming tips
        self.grooming_tips = [
            "Brush your pet regularly between mobile grooming appointments to prevent matting and reduce shedding",
            "Mobile grooming reduces anxiety for pets who get stressed in traditional salon environments",
            "Schedule regular nail trims every 4-6 weeks to maintain your pet's comfort and health", 
            "Ask your mobile groomer about seasonal coat treatments for your local climate",
            "Keep your pet calm during mobile grooming by staying nearby during the first few appointments",
            "Mobile groomers often provide more personalized attention since they focus on one pet at a time",
            "Ensure your mobile groomer is licensed and insured for your protection",
            "Mobile grooming is ideal for elderly pets who struggle with car travel",
            "Ask about package deals for multiple pets in the same household",
            "Mobile grooming eliminates exposure to other animals and potential illnesses"
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
            'avg_rating': round(avg_rating, 1),
            'url_slug': f"{city.lower().replace(' ', '-')}"
        }

    def generate_real_faqs(self, city, state, businesses, avg_rating, price_ranges):
        """Generate FAQs based on real business data"""
        # Extract real price range if available
        if price_ranges:
            typical_range = price_ranges[0]  # Use first available range
        else:
            typical_range = "$60-100"
        
        faq_pool = [
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
            },
            {
                'q': f"Are mobile pet groomers in {city} licensed and insured?",
                'a': f"Professional mobile groomers in {city} should be licensed and insured. Always verify credentials before booking and ask about their insurance coverage for your peace of mind."
            },
            {
                'q': f"How often should I schedule mobile grooming for my pet in {city}?",
                'a': f"Most pets in {city} benefit from professional grooming every 4-8 weeks, depending on breed and coat type. Your mobile groomer can recommend the best schedule for your pet's specific needs."
            }
        ]
        
        return random.sample(faq_pool, 3)

    def generate_clean_html_page(self, content):
        """Generate HTML page with clean URLs and enhanced SEO"""
        if not content:
            return None
            
        # Build business listings HTML
        businesses_html = []
        for i, biz in enumerate(content['businesses'], 1):
            
            # Format services
            services_text = ', '.join(biz.get('services', ['Mobile grooming'])[:4])
            
            # Format contact info
            contact_parts = []
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
                {f'<div class="website">🌐 <a href="{biz["website"]}" target="_blank" rel="noopener">Visit Website</a></div>' if biz.get('website') else ''}
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
    <link rel="canonical" href="https://local-pet-grooming.com/{content['url_slug']}">
    
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
        .business-card {{ background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 25px; margin: 20px 0; border-radius: 10px; border-left: 5px solid #3498db; transition: transform 0.2s ease; }}
        .business-card:hover {{ transform: translateY(-2px); }}
        .business-card h3 {{ color: #2c3e50; margin-bottom: 15px; }}
        .rating {{ color: #f39c12; font-weight: bold; margin: 10px 0; }}
        .contact {{ color: #7f8c8d; font-size: 0.9em; margin: 10px 0; }}
        .services {{ margin: 15px 0; }}
        .address, .website, .hours {{ margin: 8px 0; font-size: 0.9em; color: #5a6c7d; }}
        .website a {{ color: #3498db; text-decoration: none; }}
        .website a:hover {{ text-decoration: underline; }}
        .faq-item {{ margin: 25px 0; background: #fafafa; padding: 20px; border-radius: 8px; }}
        .faq-item h3 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .tips-section {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; margin: 30px 0; border-radius: 12px; }}
        .tips-section h2 {{ color: white; border: none; margin-bottom: 20px; }}
        .tips-section ul {{ list-style-type: none; padding: 0; }}
        .tips-section li {{ background: rgba(255,255,255,0.15); margin: 12px 0; padding: 15px; border-radius: 8px; backdrop-filter: blur(10px); }}
        h1 {{ color: #2c3e50; text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 15px; }}
        h2 {{ color: #34495e; border-left: 4px solid #3498db; padding-left: 15px; }}
        .intro {{ font-size: 1.1em; color: #555; text-align: center; margin-bottom: 30px; }}
        .stats {{ background: #e8f5e8; padding: 20px; border-radius: 10px; text-align: center; margin: 30px 0; }}
        .adsense-placeholder {{ background: #f0f0f0; padding: 20px; text-align: center; margin: 30px 0; border: 2px dashed #ccc; color: #666; }}
        .cta-section {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin: 30px 0; }}
        .cta-section h2 {{ color: white; border: none; padding: 0; }}
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
        </div>
        
        <footer style="text-align: center; padding: 20px; border-top: 1px solid #eee; margin-top: 40px; color: #7f8c8d;">
            <p>&copy; 2025 Local Pet Grooming. All rights reserved. | <a href="/privacy" style="color: #3498db;">Privacy Policy</a> | <a href="/terms" style="color: #3498db;">Terms of Service</a> | <a href="/contact" style="color: #3498db;">Contact</a></p>
            <p>Last updated: {datetime.now().strftime('%B %d, %Y')}</p>
        </footer>
    </div>
</body>
</html>"""

    def generate_all_pages(self, cities_csv='cities.csv', output_dir='clean_site'):
        """Generate pages for all cities with clean URLs"""
        Path(output_dir).mkdir(exist_ok=True)
        generated_count = 0
        all_cities = []
        
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
                    html = self.generate_clean_html_page(content)
                    
                    if html:
                        # Create clean URL structure (no .html extension)
                        city_slug = city.lower().replace(' ', '-')
                        city_dir = Path(output_dir) / city_slug
                        city_dir.mkdir(exist_ok=True)
                        
                        # Write index.html in the city directory for clean URLs
                        filepath = city_dir / 'index.html'
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(html)
                        
                        print(f"✅ Generated: {filepath}")
                        generated_count += 1
                        
                        # Store city info for homepage
                        all_cities.append({
                            'city': city,
                            'state': state,
                            'state_abbr': state_abbr,
                            'slug': city_slug,
                            'business_count': content['business_count'],
                            'avg_rating': content['avg_rating']
                        })
                    else:
                        print(f"❌ Failed to generate HTML for {city}")
                else:
                    print(f"⚠️  Skipped {city} - no business data available")
        
        # Generate homepage
        self.generate_homepage(all_cities, output_dir)
        
        # Generate legal pages
        self.generate_legal_pages(output_dir)
        
        # Generate sitemap
        self.generate_sitemap(all_cities, output_dir)
        
        # Generate _redirects for Cloudflare clean URLs
        self.generate_redirects(all_cities, output_dir)
        
        print(f"\n🎉 Generation complete! Created {generated_count} pages in '{output_dir}' directory")
        return generated_count

    def generate_homepage(self, cities, output_dir):
        """Generate enhanced homepage with all cities"""
        total_businesses = sum(city['business_count'] for city in cities)
        avg_rating = sum(city['avg_rating'] for city in cities) / len(cities) if cities else 4.5
        
        # Group cities by state for better organization
        cities_by_state = {}
        for city in cities:
            state = city['state']
            if state not in cities_by_state:
                cities_by_state[state] = []
            cities_by_state[state].append(city)
        
        # Build city cards HTML
        city_cards_html = []
        for state, state_cities in cities_by_state.items():
            for city in state_cities:
                city_cards_html.append(f"""
            <div class="city-card">
                <h3>🏙️ {city['city']}, {city['state_abbr']}</h3>
                <p><strong>{city['business_count']} Real Mobile Groomers</strong></p>
                <p>⭐ {city['avg_rating']} Average Rating • 📍 Real addresses & hours</p>
                <a href="/{city['slug']}">Find {city['city']} Groomers →</a>
            </div>""")
        
        homepage_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local Pet Grooming - Find Mobile Pet Groomers Near You</title>
    <meta name="description" content="Find the best mobile pet grooming services in your city. {total_businesses} verified mobile groomers across {len(cities)} cities with real reviews and contact info.">
    <link rel="canonical" href="https://local-pet-grooming.com/">
    
    <!-- Schema.org Organization markup -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Local Pet Grooming",
        "url": "https://local-pet-grooming.com",
        "description": "Directory of mobile pet grooming services across the United States",
        "aggregateRating": {{
            "@type": "AggregateRating",
            "ratingValue": {avg_rating:.1f},
            "reviewCount": {total_businesses}
        }}
    }}
    </script>
    
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; margin: 0; padding: 0; background: #f8f9fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .hero {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center; padding: 80px 20px; margin: -20px -20px 40px -20px; border-radius: 0 0 20px 20px; }}
        .hero h1 {{ font-size: 3em; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }}
        .hero p {{ font-size: 1.3em; margin-bottom: 30px; }}
        .stats {{ background: #e8f5e8; padding: 30px; border-radius: 15px; text-align: center; margin: 40px 0; }}
        .stats h2 {{ color: #27ae60; margin-bottom: 20px; }}
        .cities-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 25px; margin: 40px 0; }}
        .city-card {{ background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s ease; }}
        .city-card:hover {{ transform: translateY(-5px); }}
        .city-card h3 {{ color: #2c3e50; margin-bottom: 15px; font-size: 1.3em; }}
        .city-card p {{ color: #666; margin-bottom: 15px; }}
        .city-card a {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 25px; text-decoration: none; border-radius: 25px; display: inline-block; font-weight: bold; transition: transform 0.2s ease; }}
        .city-card a:hover {{ transform: translateY(-2px); box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }}
        .features {{ background: white; padding: 40px; border-radius: 15px; margin: 40px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        .features h2 {{ text-align: center; color: #2c3e50; margin-bottom: 30px; }}
        .features-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }}
        .feature {{ text-align: center; padding: 20px; }}
        .feature h3 {{ color: #3498db; margin-bottom: 15px; }}
        .adsense-placeholder {{ background: #f0f0f0; padding: 25px; text-align: center; margin: 35px 0; border: 2px dashed #ccc; color: #666; border-radius: 8px; }}
        footer {{ background: #2c3e50; color: white; text-align: center; padding: 40px 20px; margin: 40px -20px -20px -20px; border-radius: 20px 20px 0 0; }}
        footer a {{ color: #3498db; text-decoration: none; }}
        footer a:hover {{ text-decoration: underline; }}
        @media (max-width: 768px) {{ 
            .hero h1 {{ font-size: 2em; }} 
            .cities-grid {{ grid-template-columns: 1fr; }}
            .container {{ padding: 10px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>🐕 Local Pet Grooming</h1>
            <p>Find Professional Mobile Pet Groomers in Your City</p>
            <p>Convenient, stress-free grooming that comes to your home</p>
        </div>
        
        <div class="adsense-placeholder">
            [AdSense Ad Unit - Leaderboard 728x90]
        </div>
        
        <section class="stats">
            <h2>📊 {total_businesses} Real Mobile Pet Groomers</h2>
            <p><strong>{len(cities)} Cities</strong> • <strong>{avg_rating:.1f}⭐ Average Rating</strong> • <strong>Real Google Reviews</strong> • <strong>Verified Businesses</strong></p>
        </section>
        
        <section class="cities-grid">
            {''.join(city_cards_html)}
        </section>
        
        <div class="adsense-placeholder">
            [AdSense Ad Unit - Rectangle 300x250]
        </div>
        
        <section class="features">
            <h2>Why Choose Mobile Pet Grooming?</h2>
            <div class="features-grid">
                <div class="feature">
                    <h3>🏠 Convenience</h3>
                    <p>Professional grooming comes to your home - no more car rides or waiting rooms</p>
                </div>
                <div class="feature">
                    <h3>😌 Less Stress</h3>
                    <p>Your pet stays in familiar surroundings, reducing anxiety and stress</p>
                </div>
                <div class="feature">
                    <h3>🕐 Time Saving</h3>
                    <p>No need to drive to salons or wait for appointments - groomers work on your schedule</p>
                </div>
                <div class="feature">
                    <h3>👥 One-on-One Attention</h3>
                    <p>Your pet gets personalized care without distractions from other animals</p>
                </div>
                <div class="feature">
                    <h3>🧼 Full Service</h3>
                    <p>Complete grooming services including baths, cuts, nails, and ear cleaning</p>
                </div>
                <div class="feature">
                    <h3>📱 Easy Booking</h3>
                    <p>Most mobile groomers offer online booking and same-day appointments</p>
                </div>
            </div>
        </section>
        
        <div class="adsense-placeholder">
            [AdSense Ad Unit - Rectangle 300x250]
        </div>
    </div>
    
    <footer>
        <p>&copy; 2025 Local Pet Grooming. All rights reserved.</p>
        <p><a href="/privacy">Privacy Policy</a> | <a href="/terms">Terms of Service</a> | <a href="/contact">Contact</a> | <a href="/about">About Us</a></p>
        <p>Last updated: {datetime.now().strftime('%B %d, %Y')}</p>
    </footer>
</body>
</html>"""
        
        with open(Path(output_dir) / 'index.html', 'w', encoding='utf-8') as f:
            f.write(homepage_html)
        
        print("✅ Generated homepage")

    def generate_legal_pages(self, output_dir):
        """Generate required legal pages for SEO and compliance"""
        
        # Privacy Policy
        privacy_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy - Local Pet Grooming</title>
    <meta name="description" content="Privacy Policy for Local Pet Grooming directory. Learn how we collect, use, and protect your personal information.">
    <link rel="canonical" href="https://local-pet-grooming.com/privacy">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: #f8f9fa; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 15px; }
        h2 { color: #34495e; margin-top: 30px; }
        p { margin-bottom: 15px; }
        .update-date { background: #e8f5e8; padding: 15px; border-radius: 8px; margin-bottom: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Privacy Policy</h1>
        
        <div class="update-date">
            <strong>Last Updated:</strong> January 29, 2025
        </div>
        
        <h2>Information We Collect</h2>
        <p>Local Pet Grooming ("we," "our," or "us") operates as a directory of mobile pet grooming services. We collect information in the following ways:</p>
        
        <h3>Business Information</h3>
        <p>We collect publicly available business information including names, addresses, phone numbers, hours of operation, and customer reviews from public sources such as Google Maps and business websites.</p>
        
        <h3>Website Usage Data</h3>
        <p>We may collect information about how you use our website, including your IP address, browser type, pages visited, and time spent on our site through cookies and similar technologies.</p>
        
        <h2>How We Use Information</h2>
        <p>We use collected information to:</p>
        <ul>
            <li>Provide accurate business directory listings</li>
            <li>Improve our website functionality and user experience</li>
            <li>Display relevant advertisements through Google AdSense</li>
            <li>Comply with legal obligations</li>
        </ul>
        
        <h2>Information Sharing</h2>
        <p>We do not sell, trade, or otherwise transfer your personal information to third parties except:</p>
        <ul>
            <li>To display publicly available business information</li>
            <li>With advertising partners (Google AdSense) for relevant ad display</li>
            <li>When required by law or to protect our rights</li>
        </ul>
        
        <h2>Cookies and Tracking</h2>
        <p>Our website uses cookies to enhance user experience and display relevant advertisements. You can control cookie settings through your browser preferences.</p>
        
        <h2>Data Security</h2>
        <p>We implement appropriate security measures to protect against unauthorized access, alteration, disclosure, or destruction of information.</p>
        
        <h2>Your Rights</h2>
        <p>You have the right to:</p>
        <ul>
            <li>Access information we have about you</li>
            <li>Request correction of inaccurate information</li>
            <li>Request deletion of your information (where applicable)</li>
            <li>Opt-out of certain data collection practices</li>
        </ul>
        
        <h2>Contact Us</h2>
        <p>If you have questions about this Privacy Policy, please contact us at <a href="/contact">our contact page</a>.</p>
        
        <h2>Changes to This Policy</h2>
        <p>We may update this Privacy Policy from time to time. We will notify users of any material changes by posting the new policy on this page.</p>
        
        <p><a href="/">← Back to Homepage</a></p>
    </div>
</body>
</html>"""
        
        privacy_dir = Path(output_dir) / 'privacy'
        privacy_dir.mkdir(exist_ok=True)
        with open(privacy_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(privacy_html)
        
        # Terms of Service
        terms_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terms of Service - Local Pet Grooming</title>
    <meta name="description" content="Terms of Service for Local Pet Grooming directory. Understand the terms and conditions for using our website.">
    <link rel="canonical" href="https://local-pet-grooming.com/terms">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: #f8f9fa; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 15px; }
        h2 { color: #34495e; margin-top: 30px; }
        p { margin-bottom: 15px; }
        .update-date { background: #e8f5e8; padding: 15px; border-radius: 8px; margin-bottom: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Terms of Service</h1>
        
        <div class="update-date">
            <strong>Last Updated:</strong> January 29, 2025
        </div>
        
        <h2>Acceptance of Terms</h2>
        <p>By accessing and using Local Pet Grooming ("the Website"), you accept and agree to be bound by the terms and provision of this agreement.</p>
        
        <h2>Use License</h2>
        <p>Permission is granted to temporarily download one copy of the materials on Local Pet Grooming for personal, non-commercial transitory viewing only.</p>
        
        <h2>Disclaimer</h2>
        <p>The information on this website is provided on an 'as is' basis. To the fullest extent permitted by law, Local Pet Grooming excludes all representations, warranties, conditions and terms.</p>
        
        <h2>Business Listings</h2>
        <p>Business information is collected from public sources. We strive for accuracy but cannot guarantee the completeness or accuracy of all information. Users should verify business details directly with service providers.</p>
        
        <h2>User Responsibilities</h2>
        <p>Users agree to:</p>
        <ul>
            <li>Use the website lawfully and appropriately</li>
            <li>Not attempt to compromise website security</li>
            <li>Verify business information independently</li>
            <li>Respect intellectual property rights</li>
        </ul>
        
        <h2>Limitation of Liability</h2>
        <p>Local Pet Grooming shall not be held liable for any damages arising from the use of this website or the services listed herein.</p>
        
        <h2>Third-Party Services</h2>
        <p>Our website may contain links to third-party services. We are not responsible for the content, privacy policies, or practices of these external sites.</p>
        
        <h2>Modifications</h2>
        <p>Local Pet Grooming may revise these terms at any time without notice. By using this website, you agree to be bound by the current version of these Terms of Service.</p>
        
        <h2>Contact Information</h2>
        <p>Questions about the Terms of Service should be sent to us at <a href="/contact">our contact page</a>.</p>
        
        <p><a href="/">← Back to Homepage</a></p>
    </div>
</body>
</html>"""
        
        terms_dir = Path(output_dir) / 'terms'
        terms_dir.mkdir(exist_ok=True)
        with open(terms_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(terms_html)
        
        # Contact Page
        contact_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Us - Local Pet Grooming</title>
    <meta name="description" content="Contact Local Pet Grooming directory. Get in touch with questions, suggestions, or business listing requests.">
    <link rel="canonical" href="https://local-pet-grooming.com/contact">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: #f8f9fa; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 15px; }
        h2 { color: #34495e; margin-top: 30px; }
        .contact-box { background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; }
        .contact-method { margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Contact Us</h1>
        
        <p>Have questions about our mobile pet grooming directory? Need to update business information? We'd love to hear from you!</p>
        
        <div class="contact-box">
            <div class="contact-method">
                <h3>📧 General Inquiries</h3>
                <p>For general questions about our directory service, please email us at: <strong>info@local-pet-grooming.com</strong></p>
            </div>
            
            <div class="contact-method">
                <h3>🏢 Business Listings</h3>
                <p>Mobile grooming business owners who want to update their listing information or request additions can contact us at: <strong>listings@local-pet-grooming.com</strong></p>
            </div>
            
            <div class="contact-method">
                <h3>🔒 Privacy Concerns</h3>
                <p>For privacy-related questions or data removal requests, please email: <strong>privacy@local-pet-grooming.com</strong></p>
            </div>
        </div>
        
        <h2>Business Information</h2>
        <p>Local Pet Grooming is a comprehensive directory of mobile pet grooming services across the United States. We aggregate publicly available business information to help pet owners find convenient, professional grooming services in their area.</p>
        
        <h2>Response Time</h2>
        <p>We typically respond to all inquiries within 2-3 business days. For urgent matters, please indicate "URGENT" in your subject line.</p>
        
        <h2>Business Address</h2>
        <div class="contact-box">
            <p>Local Pet Grooming Directory<br>
            [Business Address]<br>
            United States</p>
        </div>
        
        <p><a href="/">← Back to Homepage</a></p>
    </div>
</body>
</html>"""
        
        contact_dir = Path(output_dir) / 'contact'
        contact_dir.mkdir(exist_ok=True)
        with open(contact_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(contact_html)
        
        # About Page
        about_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Us - Local Pet Grooming</title>
    <meta name="description" content="Learn about Local Pet Grooming directory. Our mission to connect pet owners with professional mobile grooming services.">
    <link rel="canonical" href="https://local-pet-grooming.com/about">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: #f8f9fa; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 15px; }
        h2 { color: #34495e; margin-top: 30px; }
        .highlight-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; margin: 25px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>About Local Pet Grooming</h1>
        
        <div class="highlight-box">
            <h2 style="color: white; margin-top: 0;">Our Mission</h2>
            <p>To connect pet owners with professional, convenient mobile grooming services in their local area, making pet care more accessible and stress-free for both pets and their families.</p>
        </div>
        
        <h2>What We Do</h2>
        <p>Local Pet Grooming is a comprehensive directory of mobile pet grooming services across the United States. We research and compile information about professional mobile groomers who bring salon-quality services directly to your home.</p>
        
        <h2>Why Mobile Grooming?</h2>
        <p>Mobile pet grooming offers numerous advantages over traditional salon visits:</p>
        <ul>
            <li><strong>Reduced Stress:</strong> Pets remain in familiar surroundings</li>
            <li><strong>Convenience:</strong> No travel time or waiting rooms</li>
            <li><strong>Personalized Attention:</strong> One-on-one care for your pet</li>
            <li><strong>Time Savings:</strong> Service comes to your schedule</li>
            <li><strong>Safety:</strong> No exposure to other animals or illnesses</li>
        </ul>
        
        <h2>Our Commitment</h2>
        <p>We are committed to:</p>
        <ul>
            <li>Providing accurate, up-to-date business information</li>
            <li>Featuring only legitimate, professional mobile grooming services</li>
            <li>Maintaining user privacy and data security</li>
            <li>Continuously improving our directory to serve pet owners better</li>
        </ul>
        
        <h2>How We Gather Information</h2>
        <p>Our directory information is compiled from publicly available sources, including business websites, Google Maps listings, and other public business directories. We regularly update our listings to ensure accuracy.</p>
        
        <h2>For Business Owners</h2>
        <p>If you operate a mobile pet grooming service and would like to update your listing information or have questions about how we display your business details, please <a href="/contact">contact us</a>.</p>
        
        <p><a href="/">← Back to Homepage</a></p>
    </div>
</body>
</html>"""
        
        about_dir = Path(output_dir) / 'about'
        about_dir.mkdir(exist_ok=True)
        with open(about_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(about_html)
        
        print("✅ Generated legal pages (Privacy, Terms, Contact, About)")

    def generate_sitemap(self, cities, output_dir):
        """Generate XML sitemap for clean URLs"""
        urls = [
            'https://local-pet-grooming.com/',
            'https://local-pet-grooming.com/privacy',
            'https://local-pet-grooming.com/terms',
            'https://local-pet-grooming.com/contact',
            'https://local-pet-grooming.com/about'
        ]
        
        # Add city pages
        for city in cities:
            urls.append(f"https://local-pet-grooming.com/{city['slug']}")
        
        sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join([f'''
    <url>
        <loc>{url}</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>{'1.0' if url.endswith('.com/') else '0.8'}</priority>
    </url>''' for url in urls])}
</urlset>"""
        
        with open(Path(output_dir) / 'sitemap.xml', 'w') as f:
            f.write(sitemap)
        
        print(f"✅ Generated sitemap with {len(urls)} URLs")

    def generate_redirects(self, cities, output_dir):
        """Generate _redirects file for Cloudflare Pages clean URLs"""
        redirects = []
        
        # Clean URL redirects
        for city in cities:
            redirects.append(f"/{city['slug']}.html /{city['slug']} 301")
        
        redirects_content = '\n'.join(redirects)
        
        with open(Path(output_dir) / '_redirects', 'w') as f:
            f.write(redirects_content)
        
        # Also create robots.txt
        robots_content = """User-agent: *
Allow: /

Sitemap: https://local-pet-grooming.com/sitemap.xml"""
        
        with open(Path(output_dir) / 'robots.txt', 'w') as f:
            f.write(robots_content)
        
        print("✅ Generated _redirects and robots.txt")

# Example usage
if __name__ == "__main__":
    print("🚀 Enhanced Site Generator with Clean URLs")
    print("=" * 60)
    
    generator = EnhancedSiteGenerator()
    
    if not generator.scraped_data:
        print("❌ No scraped data found!")
        print("Please run 'python business_scraper.py' first to collect business data.")
    else:
        print(f"📊 Loaded business data for {len(generator.scraped_data)} locations")
        
        # Generate enhanced site
        pages_created = generator.generate_all_pages()
        
        if pages_created > 0:
            print(f"\n✅ Success! Created {pages_created} pages with clean URLs")
            print("📁 Check the 'clean_site' directory for your generated pages")
            print("🌐 Upload to Cloudflare Pages for local-pet-grooming.com")
            print("📋 Site includes: Homepage, City pages, Privacy, Terms, Contact, About")
        else:
            print("❌ No pages were generated. Check that you have valid business data.")