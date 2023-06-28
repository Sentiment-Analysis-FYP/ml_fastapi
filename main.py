from fastapi import FastAPI, UploadFile

from controller.receive import receive_scrape
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
    return send_file(file_name)


@app.post("/upload/{scrape_id}")
async def upload_file(scrape_id: str, file: UploadFile = UploadFile(...)):
    return receive_scrape(scrape_id, file)
