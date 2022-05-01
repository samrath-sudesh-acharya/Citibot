from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

load_dotenv()

es = Elasticsearch(os.getenv('ELASTICSEARCH_URL'),ca_certs=os.getenv('CA_CERT_LOCATION'),basic_auth=(os.getenv('USER'),os.getenv('PASSWORD')))
if es.indices.exists(index="chatbot-analytics"):
    print("YES")
else:
    print("CREATED")
    es.indices.create(index='chatbot-analytics',ignore=400)

def analytics(original_query:str,query:str,lang:str,website:int,whatsapp:int):
    if exist(query.lower()):
        print("UPDATING")
        if website > whatsapp:
            print("WEBSITE")
            es.update(index='chatbot-analytics' ,  id=f"{query.lower()}" , body=
            {
                "script" : {
                "lang" : "painless",
                "source" :  """            
                            ctx._source.total_count += params.counts;
                            ctx._source.website_count += 1;
                            ctx._source.whatsapp_count += 0
                            """,
                "params" : {
                        "counts" : 1
                }
                }
            })
        else:
            print("WHATSAPP")
            es.update(index='chatbot-analytics' ,  id=f"{query.lower()}" , body=
        {
            "script" : {
            "lang" : "painless",
            "source" :  f"""            
                        ctx._source.total_count += params.counts;
                        ctx._source.website_count += 0;
                        ctx._source.whatsapp_count += 1
                        """,
            "params" : {
                    "counts" : 1
                }
            }
        })
    else:
        print("CREATING")
        es.index(index='chatbot-analytics' , id=f'{original_query.lower()}' , body={'query':f'{query.lower()}','language':f'{lang}','total_count' : 1 ,'website_count': website,'whatsapp_count':whatsapp, 'doc_as_upsert' : True})

def exist(query:str)->bool:
    print("YES")
    result=es.search(index="chatbot-analytics",body={
        'query':{
            "bool": {
                "should": [
                    {
                    "match_phrase":{
                        "query" : f"{query}"
                    }
                    }
                ]
            }
        }
    })
    print(f"RESULT : {result}")
    if(result['hits']['hits']!=[]):
        return True
    else:
        return False
