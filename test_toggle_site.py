import requests

print('Disabling dvf...')
r = requests.put('http://localhost:5000/api/sites/dvf', json={'enabled': False})
print('PUT /api/sites/dvf ->', r.status_code, r.json())
print('Trying to scrape dvf directly...')
r2 = requests.post('http://localhost:5000/api/scrape', json={'source':'dvf'})
print('/api/scrape dvf ->', r2.status_code, r2.json())
print('Re-enabling dvf...')
r3 = requests.put('http://localhost:5000/api/sites/dvf', json={'enabled': True})
print('PUT re-enable ->', r3.status_code, r3.json())
print('Scrape dvf after re-enable...')
r4 = requests.post('http://localhost:5000/api/scrape', json={'source':'dvf'})
print('/api/scrape dvf ->', r4.status_code, r4.json())
