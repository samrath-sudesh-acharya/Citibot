from elasticsearch import Elasticsearch
from fastapi.responses import JSONResponse
from deep_translator import GoogleTranslator
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
from crawler.analytics import analytics
load_dotenv()

es = Elasticsearch(os.getenv("ELASTICSEARCH_URL"),ca_certs=os.getenv("CA_CERT_LOCATION"),basic_auth=(os.getenv("USER"),os.getenv("PASSWORD")))
print(os.getenv("ELASTICSEARCH_URL"))
api_key = os.getenv("API_KEY") 


def search(query:str,lang:str,website:int,whatsapp:int)->JSONResponse:

  original_query = query 
  if lang != 'en':
    query = GoogleTranslator(source=lang,target='en').translate(query)
    print(f"THE TRANSLATED QUERY IS : {query}")
  analytics(original_query,query,lang,website,whatsapp)  
  body = {
    "from": 0,
    "size": 3, 
    "query": {
      "bool": {
        "should": [
          {
            "match": {
              "raw_text": f"{query}"
            }
          },
          {
            "match": {
              "text": f"{query}"
            }
          },
          {
            "match": {
              "title": f"{query}"
            }
          }
        ]
      }
    }
  }
  raw_json = (es.search(index='page-data',body=body))
  print(f"the length of the raw data is : {len(raw_json['hits']['hits'])}")
  result = []
  if (lang != 'en'):
    for i in range(0,len(raw_json['hits']['hits'])):
      
      raw_url =   raw_json['hits']['hits'][i]['_source']['source'] 
      url = urlparse(raw_url)
      netloc:str = url.netloc.replace('.','-') + '.translate.goog'
      if(not url.query):
        query:str = url.query + f'&_x_tr_sl=auto&_x_tr_tl={lang}&_x_tr_hl=en-US&_x_tr_pto=wapp'
      else:
        query:str = url.query + f'&_x_tr_sl=auto&_x_tr_tl={lang}&_x_tr_hl=en-US&_x_tr_pto=wapp'
      built_link = f"{url.scheme}://{netloc}{url.path}{url.params}?{query}{url.fragment}"
      
      json_data = {
        "title": GoogleTranslator(source='en',target=lang).translate(raw_json['hits']['hits'][i]['_source']['title']),
        "text": GoogleTranslator(source='en',target=lang).translate(raw_json['hits']['hits'][i]['_source']['text'][:500]),
        "raw_text": GoogleTranslator(source='en',target=lang).translate(raw_json['hits']['hits'][i]['_source']['raw_text'][:500]),
        "link": built_link
      }
      
      result.append(json_data)
  else:
    for i in range(0,len(raw_json['hits']['hits'])):
      json_data = {
        "title": raw_json['hits']['hits'][i]['_source']['title'],
        "text": raw_json['hits']['hits'][i]['_source']['text'],
        "raw_text": raw_json['hits']['hits'][i]['_source']['raw_text'],
        "link": raw_json['hits']['hits'][i]['_source']['source'] + "#:~:text=" + " ".join(raw_json['hits']['hits'][i]['_source']['raw_text'].split()[:36])
      }
      result.append(json_data)
  return result