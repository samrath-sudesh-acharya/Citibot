from rich import print
from turtle import color
from rich.panel import Panel
import requests
import re
import time
import json
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from trafilatura import fetch_url, extract
import os
from dotenv import load_dotenv
from rich.live import Live
from elasticsearch import Elasticsearch

load_dotenv()
console = Console()

#  Elastic configuration  

es = Elasticsearch(os.getenv('ELASTICSEARCH_URL'),ca_certs=os.getenv('CA_CERT_LOCATION'),basic_auth=(os.getenv('USER'),os.getenv('PASSWORD')))
es.indices.create(index='page-data',ignore=400)

# CONSTANTS

urls = []
data = []
color = 'green'
s_no = 0
id = 0

# Grab links from sitemap

xml = requests.get('https://www.online.citibank.co.in/sitemap.xml')
soup = BeautifulSoup(xml.content, 'lxml')
xml_tag = soup.find_all('loc')
for i in xml_tag:
    s=i.text
    url = re.sub('\\r\\n', '', s)
    urls.append(url)

# Get the response for the link

for i in range(0,len(urls)):
    res = requests.get(urls[i])
    if res.status_code != 200:
        color = 'red'
    print(Panel(f"URL : [blue]{urls[i]}[/blue] || RESPONSE CODE : [{color}]{res.status_code}",width=100))

    # Collecting data form the links 

    page = BeautifulSoup(res.content,'lxml')
    xml_tag = page.find_all('loc')
    table = Table(show_header=True, header_style="bold magenta",width=150)
    table.add_column("S.No",style="dim")
    table.add_column("URL")
    table.add_column("STATUS")
    with Live(table, refresh_per_second=1):
        for link in xml_tag:
            status_color = 'green'
            status = 'PASS'
            s_no=s_no +1
            time.sleep(2)
            downloaded = fetch_url(link.text)
            if downloaded is not None:
                result = extract(downloaded,output_format='json',include_links=True)
                if result is not None:
                    id = id + 1
                    es.index(index='page-data',document=result,id=id)
                    data.append(json.loads(result))
                else:
                    status_color = 'red'
                    status = 'FAIL'
                with open("sample.json", "w",encoding='utf8') as outfile:
                    json.dump(data, outfile, ensure_ascii=False)
            else:
                status_color = 'red'
                status = 'FAIL'
            table.add_row(f"{s_no}",f"{link.text}",f"[{status_color}]{status}")
        