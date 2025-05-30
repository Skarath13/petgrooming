import csv
import os
import json
from datetime import datetime
import random
from pathlib import Path

class LocalServicePageGenerator:
    def __init__(self):
        self.services = {
            'mobile-pet-grooming': {
                'title': 'Mobile Pet Grooming',
                'keywords': ['mobile dog groomer', 'pet grooming at home', 'traveling pet groomer', 'mobile cat grooming'],
                'problems': ['stressed pets at salons', 'transportation hassles', 'busy schedules', 'elderly or anxious pets'],
                'specialties': ['Full-service grooming', 'Nail trimming', 'Bath and brush', 'De-shedding treatment', 'Flea and tick treatment', 'Teeth cleaning'],
                'services': ['Mobile dog grooming', 'Mobile cat grooming', 'Nail clipping', 'Ear cleaning', 'Sanitary trimming', 'De-matting'],
                'price_ranges': ['$50-80', '$60-100', '$75-120', '$40-70'],
                'service_times': ['60-90 minutes', '45-75 minutes', '30-60 minutes', '90-120 minutes']
            }
        }
        
        self.intro_templates = [
            "Looking for convenient {service} in {city}? Skip the stress of salon visits and bring professional grooming directly to your home. Our vetted {keyword} professionals specialize in {specialty1} and {specialty2} right in your driveway.",
            "Transform your pet's grooming experience with {service} in {city}. Say goodbye to {problem} - these trusted mobile groomers provide full-service care in a calm, familiar environment for your furry family members.",
            "Discover the best {service} companies serving {city}, {state}. From {specialty1} to {specialty2}, these licensed mobile professionals deliver salon-quality results with the ultimate convenience of coming to you."
        ]
        
        self.business_prefixes = ['Mobile', 'Pampered', 'Premier', 'Luxury', 'VIP', 'Elite', 'Gentle', 'Happy']
        self.business_suffixes = ['Pet Spa', 'Mobile Grooming', 'Pet Services', 'Grooming Co', 'Pet Care', 'Mobile Salon']
        
        # AdSense-friendly content additions
        self.grooming_tips = [
            "Brush your pet regularly between grooming appointments to prevent matting",
            "Introduce your pet to grooming tools gradually to reduce anxiety",
            "Keep your pet's nails trimmed to prevent injury and discomfort",
            "Regular ear cleaning helps prevent infections and odor",
            "Professional grooming every 6-8 weeks maintains coat health"
        ]
        
        self.affiliate_products = [
            "Professional pet brushes and combs",
            "High-quality pet shampoos and conditioners", 
            "Nail trimming tools for at-home maintenance",
            "Pet-safe ear cleaning solutions",
            "Calming treats for anxious pets"
        ]

    def generate_business_name(self, service, city):
        """Generate realistic business names"""
        templates = [
            f"{city} {service['title']}",
            f"{random.choice(self.business_prefixes)} {service['title']}",
            f"{service['title']} {random.choice(self.business_suffixes)}",
            f"{city[:3].upper()} {service['title']} {random.choice(self.business_suffixes)}"
        ]
        return random.choice(templates)

    def generate_faq(self, service, city, state):
        """Generate unique FAQs for each page"""
        price_range = random.choice(service['price_ranges'])
        service_time = random.choice(service['service_times'])
        
        base_faqs = [
            {
                'q': f"How much does {service['title'].lower()} cost in {city}?",
                'a': f"Mobile pet grooming in {city} typically ranges from {price_range} depending on your pet's size, coat condition, and services needed. Large dogs or pets requiring de-matting may cost more. Many groomers offer package deals for regular customers."
            },
            {
                'q': f"How long does mobile pet grooming take in {city}?",
                'a': f"Most mobile grooming appointments in {city} take {service_time} from start to finish. The groomer brings everything needed and works right outside your home, so there's no travel time for you or stress for your pet."
            },
            {
                'q': f"Do mobile groomers in {city} service cats too?",
                'a': f"Yes! Many mobile groomers in {city} specialize in both dogs and cats. Mobile grooming is especially beneficial for cats who get stressed by car rides and unfamiliar environments."
            },
            {
                'q': f"What should I do to prepare for mobile grooming in {city}?",
                'a': f"Simply provide access to water and electricity near your driveway. Most {city} mobile groomers are fully self-contained but may need to hook up to your home's power and water for optimal service."
            },
            {
                'q': f"Is mobile pet grooming worth the extra cost in {city}?",
                'a': f"Many {city} pet owners find mobile grooming saves time and reduces pet stress. You avoid transport, waiting rooms, and your pet stays in a familiar environment. For anxious pets or busy schedules, the convenience often justifies the premium."
            }
        ]
        return random.sample(base_faqs, 3)

    def generate_page_content(self, service_key, city, state, state_abbr):
        """Generate complete page content"""
        service = self.services[service_key]
        
        # Generate intro paragraph
        intro = random.choice(self.intro_templates).format(
            service=service['title'].lower(),
            city=city,
            state=state,
            keyword=random.choice(service['keywords']),
            specialty1=random.choice(service['specialties']).lower(),
            specialty2=random.choice(service['specialties']).lower(),
            problem=random.choice(service['problems'])
        )
        
        # Generate businesses
        businesses = []
        for i in range(random.randint(4, 6)):
            businesses.append({
                'name': self.generate_business_name(service, city),
                'rating': round(random.uniform(4.4, 4.9), 1),
                'reviews': random.randint(75, 350),
                'phone': f"({random.randint(200, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
                'services': random.sample(service['services'], 3),
                'price_range': random.choice(service['price_ranges']),
                'service_time': random.choice(service['service_times']),
                'special': random.choice([
                    'First-time customer discount',
                    'Package deals for regular clients', 
                    'Same-day appointments available',
                    'Anxiety-friendly techniques',
                    'Fully equipped mobile salon',
                    'Eco-friendly products',
                    'Senior pet specialists'
                ])
            })
        
        # Generate FAQs
        faqs = self.generate_faq(service, city, state)
        
        return {
            'title': f"Best {service['title']} in {city}, {state_abbr} - Mobile Pet Groomers Near You",
            'meta_description': f"Find top-rated {service['title'].lower()} in {city}. Professional mobile groomers come to you. Compare prices, read reviews, and book convenient at-home pet grooming today.",
            'h1': f"Best {service['title']} in {city}, {state_abbr}",
            'intro': intro,
            'businesses': businesses,
            'faqs': faqs,
            'grooming_tips': random.sample(self.grooming_tips, 3),
            'affiliate_products': random.sample(self.affiliate_products, 2),
            'service': service['title'],
            'city': city,
            'state': state,
            'state_abbr': state_abbr
        }

    def generate_html_page(self, content):
        """Generate HTML page from content"""
        businesses_html = '\n'.join([f"""
            <div class="business-card">
                <h3>{biz['name']}</h3>
                <div class="rating">⭐ {biz['rating']}/5 ({biz['reviews']} reviews)</div>
                <div class="contact">📞 {biz['phone']} | 💰 {biz['price_range']} | ⏱️ {biz['service_time']}</div>
                <div class="services"><strong>Services:</strong> {', '.join(biz['services'])}</div>
                <div class="special">✨ {biz['special']}</div>
            </div>
        """ for biz in content['businesses']])
        
        faqs_html = '\n'.join([f"""
            <div class="faq-item">
                <h3>{faq['q']}</h3>
                <p>{faq['a']}</p>
            </div>
        """ for faq in content['faqs']])
        
        tips_html = '\n'.join([f"<li>{tip}</li>" for tip in content['grooming_tips']])
        products_html = '\n'.join([f"<li>{product}</li>" for product in content['affiliate_products']])
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{content['title']}</title>
    <meta name="description" content="{content['meta_description']}">
    <link rel="canonical" href="https://yoursite.com/{content['service'].lower().replace(' ', '-')}/{content['state'].lower().replace(' ', '-')}/{content['city'].lower().replace(' ', '-')}">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: #f9f9f9; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .business-card {{ background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 25px; margin: 20px 0; border-radius: 10px; border-left: 5px solid #3498db; }}
        .business-card h3 {{ color: #2c3e50; margin-bottom: 15px; }}
        .rating {{ color: #f39c12; font-weight: bold; margin: 10px 0; }}
        .contact {{ color: #7f8c8d; font-size: 0.9em; margin: 10px 0; }}
        .services {{ margin: 15px 0; }}
        .special {{ background: #e8f5e8; padding: 10px; border-radius: 5px; margin-top: 15px; color: #27ae60; font-weight: bold; }}
        .cta {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; display: inline-block; border-radius: 25px; margin: 20px 0; font-weight: bold; }}
        .faq-item {{ margin: 25px 0; background: #fafafa; padding: 20px; border-radius: 8px; }}
        .faq-item h3 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .tips-section, .products-section {{ background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #17a2b8; }}
        .tips-section ul, .products-section ul {{ list-style-type: none; padding: 0; }}
        .tips-section li, .products-section li {{ background: white; margin: 10px 0; padding: 15px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 15px; }}
        h2 {{ color: #34495e; border-left: 4px solid #3498db; padding-left: 15px; }}
        .adsense-placeholder {{ background: #f0f0f0; padding: 20px; text-align: center; margin: 30px 0; border: 2px dashed #ccc; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{content['h1']}</h1>
        <p style="font-size: 1.1em; color: #555; text-align: center; margin-bottom: 30px;">{content['intro']}</p>
        
        <div class="adsense-placeholder">
            [AdSense Ad Unit - Leaderboard 728x90]
        </div>
        
        <section class="businesses">
            <h2>🐕 Top Rated Mobile Pet Groomers in {content['city']}</h2>
            {businesses_html}
        </section>
        
        <div class="adsense-placeholder">
            [AdSense Ad Unit - Rectangle 300x250]
        </div>
        
        <section class="tips-section">
            <h2>🎯 Pet Grooming Tips for {content['city']} Pet Owners</h2>
            <ul>
                {tips_html}
            </ul>
        </section>
        
        <section class="products-section">
            <h2>🛒 Recommended Grooming Products</h2>
            <p>Keep your pet looking great between mobile grooming appointments:</p>
            <ul>
                {products_html}
            </ul>
        </section>
        
        <section class="faqs">
            <h2>❓ Frequently Asked Questions About Mobile Pet Grooming in {content['city']}</h2>
            {faqs_html}
        </section>
        
        <div class="adsense-placeholder">
            [AdSense Ad Unit - Rectangle 300x250]
        </div>
        
        <section style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin: 30px 0;">
            <h2 style="color: white; border: none; padding: 0;">Ready to Book Mobile Pet Grooming in {content['city']}? 🚐✨</h2>
            <p>Contact any of the mobile groomers listed above to schedule your pet's spa day. Most offer online booking and same-day appointments!</p>
        </section>
    </div>
</body>
</html>"""

    def generate_from_csv(self, csv_file, output_dir='output'):
        """Generate pages from CSV file with cities"""
        Path(output_dir).mkdir(exist_ok=True)
        
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                city = row['city']
                state = row['state']
                state_abbr = row['state_abbr']
                
                for service_key in self.services.keys():
                    # Generate content
                    content = self.generate_page_content(service_key, city, state, state_abbr)
                    
                    # Generate HTML
                    html = self.generate_html_page(content)
                    
                    # Create directory structure
                    service_dir = Path(output_dir) / service_key / state.lower().replace(' ', '-')
                    service_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Write file
                    filename = f"{city.lower().replace(' ', '-')}.html"
                    filepath = service_dir / filename
                    
                    with open(filepath, 'w') as f:
                        f.write(html)
                    
                    print(f"Generated: {filepath}")

    def create_sitemap(self, output_dir='output'):
        """Generate XML sitemap for all pages"""
        urls = []
        base_url = "https://yoursite.com"
        
        for service_path in Path(output_dir).iterdir():
            if service_path.is_dir():
                for state_path in service_path.iterdir():
                    if state_path.is_dir():
                        for city_file in state_path.glob('*.html'):
                            url = f"{base_url}/{service_path.name}/{state_path.name}/{city_file.stem}"
                            urls.append(url)
        
        sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join([f'''
    <url>
        <loc>{url}</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>''' for url in urls])}
</urlset>"""
        
        with open(Path(output_dir) / 'sitemap.xml', 'w') as f:
            f.write(sitemap)
        
        print(f"Generated sitemap with {len(urls)} URLs")

# Example usage
if __name__ == "__main__":
    # Create sample cities CSV with researched best cities for mobile pet grooming
    sample_cities = """city,state,state_abbr
Princeton,Texas,TX
Plano,Texas,TX
Scottsdale,Arizona,AZ
Raleigh,North Carolina,NC
Austin,Texas,TX
Kansas City,Missouri,MO
Asheville,North Carolina,NC
Santa Fe,New Mexico,NM
Tampa,Florida,FL
Colorado Springs,Colorado,CO"""
    
    with open('cities.csv', 'w') as f:
        f.write(sample_cities)
    
    # Generate pages
    generator = LocalServicePageGenerator()
    generator.generate_from_csv('cities.csv')
    generator.create_sitemap()
    
    print("\nGeneration complete! Check the 'output' directory for your pages.")