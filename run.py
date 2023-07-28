import time
import os
import requests
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import re

load_dotenv()


PROXY = os.getenv("PROXY")
INPUT_URL = os.getenv("INPUT_URL")
OUTPUT_FILE = os.getenv("OUTPUT_FILE")

proxies = {
    "http": f"http://{PROXY}",
    "https": f"http://{PROXY}",
}

def scrape_quotes(url):
     
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    time.sleep(5) 

    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find("script", text=re.compile("var data"))

    quotes = []
    # finds var data and converts content to json string
    json_str = re.search(r'var data = (\[.*?\]);', script_tag.string, re.DOTALL).group(1)
    
    # loads json to python object
    data = json.loads(json_str) 
    quotes = [{"text": quote["text"], "by": quote["author"]['name'], "tags": quote["tags"]} for quote in data]
    return quotes

def save_to_file(quotes, filename):
    with open(filename, 'w') as f:
        for quote in quotes:
            f.write(json.dumps(quote) + "\n")

if __name__ == "__main__":
    quotes = scrape_quotes(INPUT_URL)
    save_to_file(quotes, OUTPUT_FILE)
