from requests import get,Response
from print import print_response
from scarper import scrape_links

def get_links(url:str):
    xml = get(url)
    scrape_links(xml.content)

def grab_data(urls:list):
    for link in range(0,len(urls)):
        response = get(link)
        print_response(response)



