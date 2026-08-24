import requests
import re
from urllib.parse import unquote

def extract_coordinates(url, session):
    try:
        res = session.get(url, allow_redirects=True, timeout=10)
        final_url = unquote(res.url)

        # 1. Pattern !3d...!4d...
        match = re.search(r'!3d(-?\d+(?:\.\d+)?)!4d(-?\d+(?:\.\d+)?)', final_url)
        if match:
            return float(match.group(1)), float(match.group(2))

        # 2. Pattern @lat,lng
        match = re.search(r'@(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)', final_url)
        if match:
            return float(match.group(1)), float(match.group(2))

        # 3. Staticmap og:image or center parameter in HTML content
        match = re.search(r'center=(-?\d+(?:\.\d+)?)%2C(-?\d+(?:\.\d+)?)', res.text)
        if match:
            return float(match.group(1)), float(match.group(2))

        # 4. staticmap center=lat,lng unescaped
        match = re.search(r'center=(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)', res.text)
        if match:
            return float(match.group(1)), float(match.group(2))

        # 5. window.APP_INITIALIZATION_STATE or general float array lat/lng pattern [null,null,lat,lng]
        match = re.search(r'\[null,null,(-?\d+\.\d+),(-?\d+\.\d+)\]', res.text)
        if match:
            return float(match.group(1)), float(match.group(2))

    except Exception as e:
        pass

    return None, None

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
})

test_urls = [
    "https://maps.app.goo.gl/55FZayHEF4aTtW9n8",
    "https://maps.app.goo.gl/uK8xiaJjqtKyDq6a6?g_st=ac",
    "https://maps.app.goo.gl/muBAG8wkZAGEBatAA?g_st=ac",
    "https://maps.app.goo.gl/xcF7nDDyoSTeEKr96?g_st=ac",
    "https://maps.app.goo.gl/cDNnhQAtwfRRTbYR9"
]

for u in test_urls:
    lat, lng = extract_coordinates(u, session)
    print(f"URL: {u} -> ({lat}, {lng})")
