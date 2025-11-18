import os
import requests
 
# Settings
BASE_URL = "https://library.cgpbooks.co.uk/digitalcontent/MXHT42DF/assets/common/page-html5-substrates/page{page_num}_{quality}.{ext}"
OUTPUT_DIR = r""  # Save location
 
QUALITIES = [5, 4, 3, 2, 1]  # Order to try
EXTENSIONS = ["png", "jpg"]     # Prefer PNG first
 
# Paste your cookies string from your logged-in browser session here:
COOKIES = ""
 
os.makedirs(OUTPUT_DIR, exist_ok=True)
 
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    ),
    "Referer": "https://library.cgpbooks.co.uk/",
    "Cookie": COOKIES
}
 
# --- Input range ---
min_page = int(input("Enter starting page number: "))
max_page = int(input("Enter ending page number: "))
 
for page in range(min_page, max_page + 1):
    page_str = str(page).zfill(4)
    downloaded = False
 
    # Try PNG first, then JPG
    for ext in EXTENSIONS:
        for quality in QUALITIES:
            url = BASE_URL.format(page_num=page_str, quality=quality, ext=ext)
            response = requests.get(url, headers=HEADERS, stream=True)
 
            if response.status_code == 200:
                filename = f"page{page_str}_q{quality}.{ext}"
                filepath = os.path.join(OUTPUT_DIR, filename)
 
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
 
                print(f"✅ Downloaded {filename}")
                downloaded = True
                break  # Found best quality for this format
        if downloaded:
            break  # Stop checking other formats
 
    if not downloaded:
        print(f"⚠ No available image for page {page_str}.")