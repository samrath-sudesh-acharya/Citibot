# Crawler

The crawler is python script written with ```Beautifulsoup``` library, ```Trafilatura``` package and live output of the scraping of data, of each page is made with ```rich``` library. 

https://user-images.githubusercontent.com/76547134/166112307-67b77def-241f-4070-8d48-22bb9d885f4e.mp4

## How it works ?

BeautifulSoup is used to extract all the links form the sitemap and provide it to the Trafilatura.Trafilatura is a python package which helps in extracting data from all webpages. It extracts data and provides output in all format which include ```txt```,```xml```,```json``` etc. We use the json format as all the data is stored in the Elasticsearch . Trafilatura library makes scraping data very easy and it very fast having a generic solution to extract any data from any webpage.

### What data is collected ?

```json
{
  "title":"str",
  "author":"str",
  "hostname":"str",
  "data":"str",
  "categories":"str",
  "tags":"str",
  "fingerprint":"str",
  "id":"str",
  "license":"str",
  "comments":"str",
  "raw_text":"str",
  "text":"str",
  "source":"str",
  "source-hostname":"str",
  "excerpt":"str",
}
```
