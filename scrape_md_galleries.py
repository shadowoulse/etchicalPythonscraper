import requests
from bs4 import BeautifulSoup
import re
import csv
import time

BASE_URL = "https://www.artsy.net"
START_URL = f"{BASE_URL}/galleries?region=Maryland"

csv_file = "maryland_galleries.csv"

# Function to extract gallery links from a page
def extract_gallery_links(page_url):
    try:
        response = requests.get(page_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch {page_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)
    gallery_sites = set()

    for link in links:
        href = link["href"]
        if "gallery" in href:
            if href.startswith("/"):
                href = BASE_URL + href
            gallery_sites.add(href)
    return gallery_sites

# Function to extract emails from a gallery page
def extract_emails(site_url):
    emails = set()
    try:
        r = requests.get(site_url, timeout=5)
        r.raise_for_status()
        found = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", r.text)
        for email in found:
            emails.add(email)
    except Exception as e:
        print(f"Skipping {site_url}: {e}")
    return emails

# Main scraping loop
all_gallery_sites = set()
page = 1

print("Starting scraping Artsy galleries in Maryland...\n")

while True:
    print(f"Processing page {page}...")
    page_url = f"{START_URL}&page={page}"
    gallery_sites = extract_gallery_links(page_url)
    
    if not gallery_sites:
        break  # no more pages

    all_gallery_sites.update(gallery_sites)
    page += 1
    time.sleep(1)  # polite delay

print(f"\nTotal galleries found: {len(all_gallery_sites)}\n")

# Write results to CSV
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Gallery Website", "Email"])

    for site in all_gallery_sites:
        print("Processing:", site)
        emails_found = extract_emails(site)

        if emails_found:
            for email in emails_found:
                print(f"  Found email: {email}")
                writer.writerow([site, email])
        else:
            print("  No email found")
            writer.writerow([site, ""])

print(f"\nDone! Data saved to {csv_file}")
