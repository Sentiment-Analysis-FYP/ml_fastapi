from fastapi import FastAPI

from controller.download import send_file

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