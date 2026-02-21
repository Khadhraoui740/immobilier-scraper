# Simple unit test for DVF scraper
from scrapers.dvf_scraper import DVFScraper


def run_test():
    s = DVFScraper({'name': 'DVF', 'timeout': 10})
    results = s.search(100000, 800000, 'D', ['Paris'])
    print('Found', len(results), 'properties')
    if not isinstance(results, list):
        print('ERROR: results not a list')
        raise SystemExit(2)
    # check first item fields
    if results:
        r = results[0]
        required = ['id', 'source', 'url', 'title', 'price', 'surface']
        missing = [k for k in required if k not in r]
        if missing:
            print('ERROR: missing fields', missing)
            raise SystemExit(3)
    print('DVF unit test OK')


if __name__ == '__main__':
    run_test()
