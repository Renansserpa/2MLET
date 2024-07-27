from fastapi import FastAPI
from utils.scraping import scrap_website

app = FastAPI()


@app.get("/")
async def say_hello():
    return {"message": "Hello World?"}

@app.get("/links")
async def get_website_links():
    website_content = scrap_website("https://iseb3.com.br/respostas-em-planilhas")
    return website_content