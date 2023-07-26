from fastapi import FastAPI, UploadFile, Request, BackgroundTasks

from classifier.main import run_classifiers
from classifier.utils import send_request_to_express
from controller.receive import receive_scrape
from controller.scrape import run_scrape
from controller.send import send_file, send_compilation

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


@app.get("/download/complete/compilation")
async def download_compilation():
    response = send_compilation()
    return response


@app.post("/upload/{scrape_id}")
async def upload_file(scrape_id: str, file: UploadFile = UploadFile(...)):
    response = await receive_scrape(scrape_id, file)
    return response


@app.post("/scrape/{scrape_id}")
async def begin_scrape(request: Request, scrape_id: str, background_tasks: BackgroundTasks):
    data: dict = await request.json()
    # print(data['keywords'])

    # save scrape to incomplete directory
    background_tasks.add_task(run_scrape, data, scrape_id)

    # run classifiers on the scrape in background
    background_tasks.add_task(run_classifiers_in_background, scrape_id)

    return {"message": "running scrape task in background"}


def run_classifiers_in_background(scrape_id):
    run_classifiers(scrape_id)
    rsp = send_request_to_express(scrape_id)
    print(rsp)
    return
