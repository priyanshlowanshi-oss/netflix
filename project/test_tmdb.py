import requests

url = "https://api.themoviedb.org/3/trending/movie/day?api_key=YOUR_REAL_API_KEY"

try:
    r = requests.get(url, timeout=10)
    print(r.status_code)
    print(r.text[:200])
except Exception as e:
    print(e)