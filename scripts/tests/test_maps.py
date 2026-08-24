import requests
import re

url = "https://maps.app.goo.gl/muBAG8wkZAGEBatAA?g_st=ac"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

res = requests.get(url, headers=headers)
hex_ids = re.findall(r'0x[0-9a-fA-F]+:0x[0-9a-fA-F]+', res.url)
cid_dec = int(hex_ids[0].split(":")[1], 16)

cid_url = f"https://maps.google.com/?cid={cid_dec}"
r_cid = requests.get(cid_url, headers=headers)

# search for lat/lng inside r_cid.text
m = re.findall(r'\[\s*(-?\d{1,2}\.\d{5,15})\s*,\s*(-?\d{1,3}\.\d{5,15})\s*\]', r_cid.text)
print("Bracket pairs in r_cid text:", len(m))
for pair in m:
    if "22." in pair[0] or "22." in pair[1] or "88." in pair[0] or "88." in pair[1]:
        print("  Found pair:", pair)

m2 = re.findall(r'22\.\d{5,8}', r_cid.text)
m3 = re.findall(r'88\.\d{5,8}', r_cid.text)
print("22.x in cid text:", set(m2))
print("88.x in cid text:", set(m3))
