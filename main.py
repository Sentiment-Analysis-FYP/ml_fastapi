import shutil

from fastapi import FastAPI, UploadFile, Request, BackgroundTasks, Form

from classifier.main import run_classifiers, run_emotion
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
async def upload_file(scrape_id: str, background_tasks: BackgroundTasks, email: str = Form(...),
                      file: UploadFile = UploadFile(...)):
    print(email)
    response = await receive_scrape(scrape_id, file)
    background_tasks.add_task(run_classifiers_in_background, scrape_id, email)
    return response


@app.post("/scrape/{scrape_id}")
async def begin_scrape(request: Request, scrape_id: str, background_tasks: BackgroundTasks):
    data: dict = await request.json()
    print(data)

    # save scrape to incomplete directory
    background_tasks.add_task(run_scrape, data, scrape_id)

    # run classifiers on the scrape in background
    background_tasks.add_task(run_classifiers_in_background, scrape_id, data['email'])

    # run emotion classifier
    background_tasks.add_task(run_emotion_in_background, scrape_id)

    return {"message": "running scrape task in background"}


def run_classifiers_in_background(scrape_id, email):
    run_classifiers(scrape_id)
    rsp = send_request_to_express(scrape_id, email)
    print(rsp)
    return


# @app.post('/testlexmo')
# async def test_lexmo(req: Request):
#     data = await req.json()
#     text = data['text']
#     return get_emotion_info(text)

def run_emotion_in_background(scrape_id):
    # get file with emotions classified
    run_emotion(scrape_id)
    return
