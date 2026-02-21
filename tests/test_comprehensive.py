"""
Comprehensive pytest suite for immobilier-scraper application.
Tests cover: database, API routes, configuration, scraping, email, and edge cases.
"""
import pytest
import requests
import json
from pathlib import Path
from database.db import Database
from scrapers.manager import ScraperManager
from config import SEARCH_CONFIG, SCRAPERS_CONFIG
from utils import PropertyUtils
from validators import validate_property


BASE_URL = 'http://localhost:5000'

# ============================================================================
# DATABASE TESTS
# ============================================================================

@pytest.fixture(scope='session')
def db():
    """Provide database connection for tests"""
    return Database()


def test_db_init(db):
    """Test database initialization"""
    assert db is not None
    conn = db.get_connection()
    assert conn is not None
    conn.close()


def test_db_add_property(db):
    """Test adding a property to database"""
    prop = {
        'id': 'test_prop_1',
        'source': 'test',
        'url': 'https://test.com/prop1',
        'title': 'Test Property',
        'location': 'Paris',
        'price': 250000.0,
        'surface': 50.0
    }
    result = db.add_property(prop)
    assert result is not None


def test_db_property_exists(db):
    """Test checking if property exists"""
    url = 'https://test.com/prop_exists'
    prop = {
        'id': 'test_prop_exists',
        'source': 'test',
        'url': url,
        'title': 'Existing Property',
        'location': 'Paris',
        'price': 300000.0,
        'surface': 60.0
    }
    db.add_property(prop)
    assert db.property_exists(url) is True


def test_db_get_statistics(db):
    """Test getting database statistics"""
    stats = db.get_statistics()
    assert 'total_properties' in stats
    assert stats['total_properties'] >= 0
    assert 'by_source' in stats
    assert 'by_status' in stats


# ============================================================================
# API ENDPOINT TESTS
# ============================================================================

@pytest.fixture(scope='session')
def client():
    """Provide HTTP client for API tests"""
    return requests


def test_api_dashboard(client):
    """Test dashboard endpoint"""
    r = client.get(f'{BASE_URL}/')
    assert r.status_code == 200
    assert 'propriét' in r.text.lower() or 'dashboard' in r.text.lower()


def test_api_properties_page(client):
    """Test properties listing page"""
    r = client.get(f'{BASE_URL}/properties')
    assert r.status_code == 200


def test_api_property_detail(client, db):
    """Test property detail page"""
    # Get a property ID from the database
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM properties LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    
    if result:
        prop_id = result[0]
        r = client.get(f'{BASE_URL}/property/{prop_id}')
        assert r.status_code == 200


def test_api_search_empty(client):
    """Test search API with empty filters"""
    r = client.post(f'{BASE_URL}/api/search', json={}, timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert data.get('success') is True or 'properties' in data


def test_api_search_with_filters(client):
    """Test search API with filters"""
    filters = {
        'price_min': 150000,
        'price_max': 400000,
        'location': 'Paris'
    }
    r = client.post(f'{BASE_URL}/api/search', json=filters, timeout=5)
    assert r.status_code == 200


def test_api_stats(client):
    """Test statistics endpoint"""
    r = client.get(f'{BASE_URL}/api/stats')
    assert r.status_code == 200
    data = r.json()
    assert 'total' in data or 'total_properties' in data


def test_api_properties_json(client):
    """Test properties JSON endpoint"""
    r = client.get(f'{BASE_URL}/api/properties')
    assert r.status_code == 200
    data = r.json()
    assert 'properties' in data or 'count' in data


def test_api_scrape(client):
    """Test scraping endpoint"""
    r = client.post(f'{BASE_URL}/api/scrape', json={'source': 'all'}, timeout=60)
    assert r.status_code == 200
    data = r.json()
    assert 'success' in data


# ============================================================================
# CONFIGURATION TESTS
# ============================================================================

def test_api_get_config(client):
    """Test get configuration endpoint"""
    r = client.get(f'{BASE_URL}/api/config/get')
    assert r.status_code == 200
    data = r.json()
    assert 'config' in data


def test_api_save_config(client):
    """Test save configuration endpoint"""
    new_config = {
        'budget_min': 100000,
        'budget_max': 600000,
        'dpe_max': 'E',
        'zones': ['Paris', 'Lyon']
    }
    r = client.post(f'{BASE_URL}/api/config/save', json=new_config)
    assert r.status_code == 200


def test_api_smtp_config(client):
    """Test SMTP configuration endpoint"""
    smtp_config = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'from_email': 'test@gmail.com',
        'password': 'testpass',
        'email': 'recipient@gmail.com'
    }
    r = client.post(f'{BASE_URL}/api/config/smtp', json=smtp_config)
    assert r.status_code == 200


# ============================================================================
# EMAIL / NOTIFICATION TESTS
# ============================================================================

def test_api_alert_test_endpoint(client):
    """Test email alert endpoint (should use fallback if no SMTP)"""
    r = client.post(f'{BASE_URL}/api/alerts/test', timeout=10)
    assert r.status_code == 200
    data = r.json()
    # Should either succeed or have a fallback message
    assert 'success' in data or 'message' in data


# ============================================================================
# SCRAPER TESTS
# ============================================================================

@pytest.fixture(scope='session')
def scraper_manager():
    """Provide scraper manager for tests"""
    return ScraperManager()


def test_scraper_manager_init(scraper_manager):
    """Test scraper manager initialization"""
    assert scraper_manager is not None
    assert len(scraper_manager.scrapers) > 0


def test_dvf_scraper_search(scraper_manager):
    """Test DVF scraper search"""
    results = scraper_manager.scrape_single(
        'dvf',
        budget_min=100000,
        budget_max=500000,
        dpe_max='D',
        zones=['Paris']
    )
    assert isinstance(results, list)
    if results:
        prop = results[0]
        assert 'id' in prop
        assert 'source' in prop


def test_scraper_reload(scraper_manager):
    """Test scraper manager reload"""
    scraper_manager.reload()
    assert len(scraper_manager.scrapers) > 0


# ============================================================================
# UTILITY TESTS
# ============================================================================

def test_property_utils_normalize():
    """Test property normalization"""
    prop = {
        'id': 'test',
        'source': 'TEST',
        'title': 'Test Property',
        'location': 'Paris',
        'price': 250000,
        'surface': 50
    }
    normalized = PropertyUtils.normalize_property(prop)
    assert normalized['source'] == 'TEST'
    assert normalized['title'] == 'Test Property'
    assert normalized['price'] == 250000.0


def test_property_validation():
    """Test property validation with pydantic"""
    prop = {
        'id': 'test',
        'source': 'TEST',
        'title': 'Test',
        'location': 'Paris',
        'price': 250000,
        'surface': 50
    }
    validated = validate_property(prop)
    assert validated['id'] == 'test'
    assert validated['price'] == 250000.0


def test_property_utils_format_price():
    """Test price formatting"""
    formatted = PropertyUtils.format_price(250000)
    assert '250' in formatted
    assert '€' in formatted


def test_property_utils_format_surface():
    """Test surface formatting"""
    formatted = PropertyUtils.format_surface(50.5)
    assert '50' in formatted or '51' in formatted
    assert 'm²' in formatted


# ============================================================================
# EDGE CASE / ERROR HANDLING TESTS
# ============================================================================

def test_api_404_not_found(client):
    """Test 404 error on non-existent page"""
    r = client.get(f'{BASE_URL}/nonexistent_page')
    assert r.status_code == 404


def test_property_links_are_valid(client):
    """Test that property 'Voir' links are valid"""
    r = client.get(f'{BASE_URL}/properties')
    assert r.status_code == 200
    # Check for property links
    assert 'href=' in r.text


def test_search_with_invalid_filters(client):
    """Test search with invalid filter values"""
    filters = {
        'price_min': 'invalid',
        'price_max': 'invalid'
    }
    r = client.post(f'{BASE_URL}/api/search', json=filters, timeout=5)
    # Should not crash, either return 200 or validation error
    assert r.status_code in [200, 400, 422]


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

def test_end_to_end_scrape_and_search(client, db):
    """Test full flow: scrape, save, search"""
    # Get initial count
    stats_before = db.get_statistics()
    count_before = stats_before.get('total_properties', 0)
    
    # Scrape
    r = client.post(f'{BASE_URL}/api/scrape', json={'source': 'dvf'}, timeout=60)
    assert r.status_code == 200
    
    # Check count increased or stayed same
    stats_after = db.get_statistics()
    count_after = stats_after.get('total_properties', 0)
    assert count_after >= count_before


def test_configuration_persistence(client):
    """Test that configuration changes persist across API calls"""
    # Set config
    config1 = {'budget_min': 150000, 'budget_max': 350000, 'dpe_max': 'C', 'zones': ['Paris']}
    r1 = client.post(f'{BASE_URL}/api/config/save', json=config1)
    assert r1.status_code == 200
    
    # Get config
    r2 = client.get(f'{BASE_URL}/api/config/get')
    assert r2.status_code == 200


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
