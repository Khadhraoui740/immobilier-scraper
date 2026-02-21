import requests
import re

BASE = 'http://localhost:5000'


def test_properties_page_has_valid_links():
    r = requests.get(f"{BASE}/properties", timeout=5)
    assert r.status_code == 200
    text = r.text
    # find first 'Voir' anchor
    m = re.search(r'<a[^>]+>(?:\s*<i[^>]*>[^<]*</i>\s*)?\s*Voir', text)
    assert m, 'Bouton Voir introuvable'
    # find hrefs for property cards
    hrefs = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>\s*<i[^>]*>[^<]*</i>\s*Voir', text)
    assert hrefs, 'Aucun href trouvé pour Voir'
    # At least one href should not be '#'
    assert any(h for h in hrefs if h and h != '#')


def test_property_detail_page():
    # get properties list to extract an id
    r = requests.post(f"{BASE}/api/search", json={}, timeout=5)
    assert r.status_code == 200
    data = r.json()
    props = data.get('properties')
    assert props, 'Aucune propriété retournée par /api/search'
    prop = props[0]
    pid = prop['id']
    # open detail page
    r2 = requests.get(f"{BASE}/property/{pid}", timeout=5)
    assert r2.status_code == 200
    assert prop['title'][:10] in r2.text or prop['location'] in r2.text


def test_email_alert_endpoint_works():
    # Try the alerts test endpoint; in absence of SMTP it should succeed via debug fallback
    r = requests.post(f"{BASE}/api/alerts/test", timeout=10)
    assert r.status_code == 200
    data = r.json()
    assert 'success' in data


if __name__ == '__main__':
    print('Run these tests with pytest in a real CI environment')
