#!/usr/bin/env python3
"""Test SeLoger Selenium Scraper"""

from scrapers.seloger_selenium import SeLogerSeleniumScraper
from config import SCRAPERS_CONFIG

print("\n" + "="*70)
print("Testing SeLoger Selenium Scraper")
print("="*70)

scraper = SeLogerSeleniumScraper(SCRAPERS_CONFIG['seloger'])

print("\nSearching for properties 200k-500k in Paris...")
print("(This will take 15-20 seconds with Selenium)")

try:
    results = scraper.search(200000, 500000, 'D', ['Paris'])
    
    print(f"\n✓ Results: {len(results)} properties found")
    
    if results:
        print("\nFirst 5 properties:")
        for i, prop in enumerate(results[:5], 1):
            print(f"  {i}. {prop['title']}")
            print(f"     Price: {prop['price']:,} EUR")
            print(f"     Location: {prop['location']}")
            print()
    else:
        print("⚠ No properties found - check logs for errors")
        
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("="*70)
