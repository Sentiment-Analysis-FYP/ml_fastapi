from fastapi import FastAPI, UploadFile, Body, Request

from controller.receive import receive_scrape
from controller.scrape import run_scrape
from controller.send import send_file

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/download/{file_name}")
async def download_file(file_name: str):
    response = send_file(file_name)
    return response


@app.post("/upload/{scrape_id}")
async def upload_file(scrape_id: str, file: UploadFile = UploadFile(...)):
    response = await receive_scrape(scrape_id, file)
    return response


@app.post("/scrape/{scrape_id}")
async def begin_scrape(request: Request, scrape_id: str):
    data: dict = await request.json()
    # print(data['keywords'])
    scrape = await run_scrape(data)
    # scrape = []
    return scrape
