import requests


BASE_URL = "http://127.0.0.1:8000/api"

def test_rate_limiting():
    # Send requests to the endpoint until it is rate limited
    for i in range(1, 12):
        response = requests.get(f'{BASE_URL}/books/search', headers={'Accept-Encoding': 'gzip'})
        if response.status_code == 429:
            print(f"Rate limited after {i} requests")
            assert '429 Too Many Requests' in response.text
            break
    else:
        assert False, "Rate limit was not triggered"

def test_rate_limiting_default():
    # Send requests to the endpoint until it is rate limited
    for i in range(1, 12):
        response = requests.get(f'{BASE_URL}/books/search_default_limit', headers={'Accept-Encoding': 'gzip'})
        if response.status_code == 429:
            print(f"Rate limited after {i} requests")
            assert '429 Too Many Requests' in response.text
            break
    else:
        assert False, "Rate limit was not triggered"

def test_compression():
    """ Test that compression reduces the size of the response. """
    response_compressed = requests.get(f"{BASE_URL}/large-data", headers={'Accept-Encoding': 'gzip'}, stream=True)
    response_uncompressed = requests.get(f"{BASE_URL}/large-data-no-compress", headers={'Accept-Encoding': 'gzip'}, stream=True)
        
    assert response_compressed.status_code == 200
    assert response_uncompressed.status_code == 200
    
    assert len(response_compressed.raw.read()) < len(response_uncompressed.raw.read())

