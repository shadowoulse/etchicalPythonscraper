import requests
from bs4 import BeautifulSoup
import re
import csv

# Public directory of galleries in Maryland
url = "https://www.artsy.net/galleries?region=Maryland"

response = requests.get(url)
if response.status_code != 200:
    print("Failed to fetch page")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Extract gallery links
galleries = soup.find_all("a", href=True)
gallery_sites = set()

for link in galleries:
    href = link["href"]
    if "gallery" in href:
        if href.startswith("/"):
            href = "https://www.artsy.net" + href
        gallery_sites.add(href)

print(f"Found {len(gallery_sites)} galleries.\n")

# Prepare CSV file
csv_file = "maryland_galleries.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Header row
    writer.writerow(["Gallery Website", "Email"])

    # Scrape emails and write rows
    for site in gallery_sites:
        print("Processing:", site)
        emails_found = set()
        try:
            r = requests.get(site, timeout=5)
            # Search for emails
            emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", r.text)
            for email in emails:
                emails_found.add(email)
        except Exception as e:
            print(f"Skipping {site}: {e}")

        if emails_found:
            for email in emails_found:
                writer.writerow([site, email])
        else:
            writer.writerow([site, ""])  # No email found

print(f"\nDone! Data saved to {csv_file}")
