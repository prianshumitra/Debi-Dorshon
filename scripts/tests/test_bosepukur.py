import requests
import re

url = "https://maps.app.goo.gl/Bfk1kHVQEGhUzFj4A?g_st=ac"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

res = requests.get(url, headers=headers)
hex_ids = re.findall(r'0x[0-9a-fA-F]+:0x[0-9a-fA-F]+', res.url)

if hex_ids:
    cid_hex = hex_ids[0].split(":")[1]
    cid_dec = int(cid_hex, 16)
    cid_url = f"https://maps.google.com/?cid={cid_dec}"
    r_cid = requests.get(cid_url, headers=headers)
    print("CID final URL:", r_cid.url)
    
    m1 = re.search(r'!3d(-?\d+(?:\.\d+)?)!4d(-?\d+(?:\.\d+)?)', r_cid.url)
    m2 = re.search(r'@(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)', r_cid.url)
    print("m1 from CID:", m1.groups() if m1 else None)
    print("m2 from CID:", m2.groups() if m2 else None)
    
    # search staticmap in r_cid.text
    m3 = re.findall(r'center=(-?\d+(?:\.\d+)?)%2C(-?\d+(?:\.\d+)?)', r_cid.text)
    print("m3 from CID text:", m3)
