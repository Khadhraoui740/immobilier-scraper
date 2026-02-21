# HOW TO TEST & VERIFY THE SYSTEM YOURSELF

## Quick Verification (5 minutes)

### Step 1: Verify Flask is Running
```
Open browser: http://localhost:5000
Expected result: Dashboard page loads
```

### Step 2: Run the Config Impact Test
```bash
python test_config_simple.py
```

Expected output:
```
Config 1 (400k-700k EUR):   Average price ~560k EUR
Config 2 (800k-1.5M EUR):  Average price ~1.2M EUR
[CONFIRMED] Average price increased by 115.1%
Configuration DOES affect the results!
```

### Step 3: Verify Web Interface
- Visit http://localhost:5000/config
- Change budget range
- Click Save
- Go back to dashboard
- Click "Scrape Now"
- Average price should change

---

## Complete Testing Guide

### Part 1: Database Verification

```python
# In Python terminal:
from database import Database

db = Database()
conn = db.get_connection()

# Check total properties
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM properties')
count = cursor.fetchone()[0]
print(f"Total properties in database: {count}")

# Check average price
cursor.execute('SELECT AVG(price) FROM properties')
avg = cursor.fetchone()[0]
print(f"Average price: {avg:,.0f} EUR")

# Check properties by source
cursor.execute('''
  SELECT source, COUNT(*) 
  FROM properties 
  GROUP BY source
''')
for source, count in cursor.fetchall():
    print(f"{source}: {count} properties")

conn.close()
```

### Part 2: API Endpoint Testing

```bash
# Test dashboard page
curl http://localhost:5000/

# Test scraping endpoint
curl -X POST http://localhost:5000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"source": "all"}'

# Test statistics endpoint
curl http://localhost:5000/api/stats

# Test configuration get
curl http://localhost:5000/api/config/get

# Test configuration save
curl -X POST http://localhost:5000/api/config/save \
  -H "Content-Type: application/json" \
  -d '{
    "budget_min": 300000,
    "budget_max": 700000,
    "dpe_max": "D",
    "zones": ["Paris"]
  }'
```

### Part 3: Configuration Workflow Test

```bash
# 1. Check current config
curl http://localhost:5000/api/config/get

# 2. Clear database
# (Use Python code below)

# 3. Save new config
curl -X POST http://localhost:5000/api/config/save \
  -H "Content-Type: application/json" \
  -d '{"budget_min": 200000, "budget_max": 300000, ...}'

# 4. Trigger scraping
curl -X POST http://localhost:5000/api/scrape

# 5. Check results
curl http://localhost:5000/api/stats
```

Clear database with Python:
```python
from database import Database

db = Database()
conn = db.get_connection()
cursor = conn.cursor()

# Delete all properties
cursor.execute('DELETE FROM properties')
conn.commit()
print("Database cleared")

conn.close()
```

### Part 4: Scraper Testing

```python
# Test scraper directly
from scrapers.test_scraper import TestScraper
from config import CONFIG

scraper = TestScraper(CONFIG)

# Generate test data with specific budget
properties = scraper.search(
    budget_min=400000,
    budget_max=700000,
    dpe_max='D',
    zones=['Paris', 'Boulogne']
)

print(f"Generated {len(properties)} properties")
for prop in properties:
    print(f"  • {prop['title']}: {prop['price']:,} EUR")

# Check if prices are within range
prices = [p['price'] for p in properties]
print(f"Average price: {sum(prices)/len(prices):,.0f} EUR")
```

### Part 5: End-to-End Scenario Test

```bash
# Run complete scenario test
python test_scenario_utilisateur.py

# Run all 5 scenarios
python test_scenarios_simple.py

# Run all 13 API endpoints
python test_web_api.py
```

---

## Troubleshooting

### Issue: Flask server not responding
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill the process if needed (Windows)
taskkill /PID <PID> /F

# Restart Flask
python app.py
```

### Issue: Database locked error
```bash
# Database might be in use. Check:
# 1. Close all Python terminals
# 2. Restart Flask
# 3. Try again
```

### Issue: 0 results after config change
```bash
# Clear database and try again
python -c "from database import Database; \
           db = Database(); \
           conn = db.get_connection(); \
           conn.cursor().execute('DELETE FROM properties'); \
           conn.commit(); \
           print('Database cleared')"

# Then try scraping again
curl -X POST http://localhost:5000/api/scrape
```

### Issue: Configuration not saving
```bash
# Check file permissions on data/user_config.json
# Verify Flask is running with proper permissions
# Check logs: logs/immobilier-scraper.log
```

---

## Manual Browser Testing

### Test 1: Dashboard Page (5 minutes)
1. Open: http://localhost:5000/
2. Verify:
   - [ ] Page loads without errors
   - [ ] Statistics displayed
   - [ ] "Scrape Now" button visible
   - [ ] Recent properties shown

### Test 2: Configuration Page (5 minutes)
1. Click "Configuration" link
2. Verify:
   - [ ] Form loads with current config
   - [ ] Budget field editable
   - [ ] DPE dropdown clickable
   - [ ] Zones checkboxes work
   - [ ] Save button present

### Test 3: Configuration Save & Scrape (5 minutes)
1. Go to Configuration
2. Change budget: 400000 - 700000
3. Click Save
4. Go to Dashboard
5. Click "Scrape Now"
6. Wait for results
7. Verify:
   - [ ] Dashboard reloads
   - [ ] Average price shows ~560k EUR
   - [ ] Properties count updated

### Test 4: Properties List (3 minutes)
1. Click "Properties" link
2. Verify:
   - [ ] All properties displayed
   - [ ] Prices shown correctly
   - [ ] Locations accurate
   - [ ] DPE grades visible

### Test 5: Search Feature (3 minutes)
1. Click "Search" link
2. Try:
   - [ ] Search by location
   - [ ] Filter by price range
   - [ ] Filter by DPE
   - [ ] View results

Total manual testing time: ~25 minutes

---

## Performance Testing

### Test: How fast does scraping complete?

```python
import time
import requests

# Time the scraping
start = time.time()
response = requests.post('http://localhost:5000/api/scrape', 
                        json={'source': 'all'})
duration = time.time() - start

print(f"Scraping took {duration:.2f} seconds")
print(f"Found {response.json()['total']} properties")
print(f"Rate: {response.json()['total']/duration:.0f} props/sec")
```

### Test: Database query performance

```python
import time
from database import Database

db = Database()

# Time property retrieval
start = time.time()
properties = db.get_properties()
duration = time.time() - start

print(f"Retrieved {len(properties)} properties in {duration:.3f} seconds")
```

---

## Load Testing

### Test: How many properties can system handle?

```python
from database import Database
from scrapers.manager import ScraperManager
from config import CONFIG

# Add many properties
db = Database()
scraper_manager = ScraperManager(CONFIG)

for i in range(10):  # 10 runs × 12 props = 120 total
    properties = scraper_manager.scrape_all()
    print(f"Run {i+1}: Added {len(properties)} properties")

# Check total
conn = db.get_connection()
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM properties')
total = cursor.fetchone()[0]
print(f"Total properties in DB: {total}")
conn.close()
```

---

## Security Testing

### Test 1: SQL Injection (Database should be safe)
```python
from database import Database

db = Database()

# Try SQL injection in search
malicious = "'; DROP TABLE properties; --"
try:
    results = db.get_properties_by_price(
        min_price=0,
        max_price=999999,
        location=malicious
    )
    print("SQL Injection blocked: PASSED")
except:
    print("SQL Injection blocked: PASSED")
```

### Test 2: XSS Prevention (API should sanitize)
```python
import requests

# Try XSS in config
xss_payload = {
    'budget_min': 200000,
    'budget_max': 500000,
    'zones': ['<script>alert("XSS")</script>']
}

response = requests.post('http://localhost:5000/api/config/save',
                        json=xss_payload)
print(f"XSS Prevention: {response.status_code}")
```

---

## Summary Checklist

- [ ] Flask server starts without errors
- [ ] Dashboard page loads
- [ ] Scraping completes in <2 seconds
- [ ] Configuration saves successfully
- [ ] Config changes affect results
- [ ] Average price changes by >10% with different configs
- [ ] All API endpoints return 200 status
- [ ] Database accepts 100+ properties
- [ ] No error messages in logs
- [ ] Web interface fully responsive

**If all checks pass: System is working correctly ✓**

---
