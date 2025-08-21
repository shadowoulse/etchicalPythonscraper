## UPDATE Branch: Example Python Scraper (Art Galleries)

This branch contains an UPDATE **example Python scraper** that collects information from Artsy.net for galleries using BeautifulSoup.

### What this update does

- Scrapes Artsy gallery pages for galleries as an example.
- Collects:
  - Gallery website URL
  - Email addresses (if found)
- Outputs the results to a CSV file: this example would be `maryland_galleries.csv`.
- Automatically loops through multiple pages of gallery listings.
this update also has a Includes a 1-second delay between pages to avoid overwhelming the server.
### How to run

1. Make sure Python 3 is installed.
2. Install required packages:

```bash
pip install requests beautifulsoup4
run with python3 scrape_md_galleries.py or change the name for your use and rewrite etc.
