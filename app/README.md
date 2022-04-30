## API

The API is built with FastAPI(a REST API python framework) which helps the user's to query easily to the Elasticsearch both in website and Whatsapp and get the required data.

## Requests

There are currently two request in our api

```api
GET : <API_URL>/search?q=
```
> This get request handle all the query coming from the website and fecth the result from the       Elasticsearch.

```api
POST : <API_URL>/whatsapp/search
```
> This post request handle all the query coming from whatapps users through ```twilio``` and fetch the   result from the 
Elasticsearch.

### Feature

- Detects which language the query what made in 
- Transalates the required data to the following language the query was made in.
- Format the url to the language needed and also the important content to be highlighted in a       webpage.
