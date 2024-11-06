# app\main.py

from fastapi import FastAPI, HTTPException, Request
from app.infrastructure.rest.controllers.ciberbullying_detection_controller import router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.infrastructure.configuration.configuration import get_spanish_peruvian_dictionary
from datetime import date
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import hunspell
import nltk
import spacy

app = FastAPI(
    title="ciberbullying-detection-api",
    description=(
        "Esta API expone un endpoint para el consumo de un modelo de aprendizaje automático entrenado con elementos textuales, emojis y emoticones para la detección de mensajes de ciberacoso en español peruano."
    ),
    version="1.0.0"
)

spanish_peruvian_dictionary = None
stopwords_es = None
hunspell_agent = None
nlp = None
stemmer = None

@app.on_event("startup")
def startup_event():
    global spanish_peruvian_dictionary
    global stopwords_es
    global hunspell_agent
    global nlp
    global stemmer

    spanish_peruvian_dictionary = get_spanish_peruvian_dictionary()

    nltk.download('stopwords')
    stopwords_es = set(stopwords.words('spanish'))

    nltk.download('punkt')

    hunspell_agent = hunspell.HunSpell('/usr/share/hunspell/es_PE.dic', '/usr/share/hunspell/es_PE.aff')

    nlp = spacy.load('es_core_news_sm')

    stemmer = SnowballStemmer('spanish')

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(content={"timestamp": date.today().isoformat(), "messages": [error['msg'] for error in exc.errors()]}, status_code=400)

app.include_router(router, prefix="/peruvian-ciberbullying", tags=["Endpoint para la detección de ciberacoso"])