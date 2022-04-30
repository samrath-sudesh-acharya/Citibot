from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.search import search
import os
from deep_translator import GoogleTranslator , single_detection
import pyshorteners
from fastapi import FastAPI, Form, Response,Request, HTTPException
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator 
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

user =[]

@app.get("/")
def start():
    return "Hi this is Citibot"

@app.get("/search={query}")
def intro(query:str):
    result = search(query)
    return result

@app.post("/whatsapp/search")
async def chat(
    request: Request, From: str = Form(...), Body: str = Form(...) ):
    validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])
    form_ = await request.form()
    if not validator.validate(
        str(request.url), 
        form_, 
        request.headers.get("X-Twilio-Signature", "")
    ):
        raise HTTPException(status_code=400, detail="Error in Twilio Signature")

    response = MessagingResponse()
    lang = single_detection(Body,api_key=os.getenv("API_KEY"))
    result = search(Body,lang)
    link = pyshorteners.Shortener().tinyurl.short(result[0]['link'])
    response.message(GoogleTranslator(source='en',target=lang).translate("Here are some of the result i found"))
    response.message(f"*{result[0]['title']}*\n\n{link}")
    response.message(f"*{result[1]['title']}*\n\n{link}")
    response.message(f"*{result[2]['title']}*\n\n{link}")
    return Response(content=str(response), media_type="application/xml")

origins = ["*"]

app = CORSMiddleware(
    app=app,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)