from bs4 import BeautifulSoup
import re
from print import grab_data 

def scrape_links(xml:bytes):
    urls = []
    soup = BeautifulSoup(xml,'lxml')
    xml_tag = soup.find_all('loc')
    for data in xml_tag:
        info = data.text
        url = re.sub('\\r\\n', '', info)
        urls.append(url)
    grab_data(urls)