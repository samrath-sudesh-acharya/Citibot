# CitiBot
An AI powered chatbot for CitiBank. It supports multilingual support for a more wider reachabilty. It provides accurate sugestion for the user's query at very quick rate.

https://user-images.githubusercontent.com/76547134/164944272-9c960497-d6f8-42be-9bd7-8615acba8ab6.mp4

## How CitiBot works ?

The CitiBot has a very fast suggestion system built with Elasticsearch running in Docker container. The data from Elastic Search is servered to the frontend with a help of REST API made with Fastapi framework.
The data that elasticsearch is feed with by a crawler programed in python which collects all the data from webpage in citibank. The user's query is searched through the data collected and the best results
are recommended back to user with whichever language the query was made with .

for more information on<br/>
[Frontend](https://github.com/samrath-sudesh-acharya/Citibot/tree/main/chatbot-ui) | [Crawler]() | [API]()

## Information Architecture

![citibot drawio](https://user-images.githubusercontent.com/76547134/164945268-35bef611-3547-466d-9a19-c25dc2ff1532.png)
