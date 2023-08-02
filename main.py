import asyncio
import concurrent
import shutil
import threading
from multiprocessing import Process

from fastapi import FastAPI, UploadFile, Request, BackgroundTasks, Form
from starlette.concurrency import run_in_threadpool

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
    # background_tasks.add_task(run_emotion_in_background, scrape_id)
    # thread = threading.Thread(target=run_emotion_in_background(scrape_id))
    # thread.start()
    # emo = await run_in_threadpool(lambda: run_emotion_in_background(scrape_id))
    # asyncio.create_task(run_emotion_in_background(scrape_id))
    background_tasks.add_task(run_classifiers_in_background, scrape_id, email)
    # background_tasks.add_task(run_emotion_in_background, scrape_id)
    print('emo added')

    return response


@app.post("/scrape/{scrape_id}")
async def begin_scrape(request: Request, scrape_id: str, background_tasks: BackgroundTasks):
    data: dict = await request.json()
    print(data)

    # save scrape to incomplete directory
    print('before send')
    background_tasks.add_task(run_scrape, data, scrape_id)

    # run classifiers on the scrape in background
    background_tasks.add_task(run_classifiers_in_background, scrape_id, data['email'])
    #
    # proc = Process(target=run_emotion(scrape_id))
    # proc.start()
    # run emotion classifier
    # background_tasks.add_task(run_emotion_in_background, scrape_id)
    # thread = threading.Thread(target=run_emotion_in_background(scrape_id))
    # thread.start()
    #
    # emo = await run_in_threadpool(lambda: run_emotion_in_background(scrape_id))
    return {"message": "running scrape task in background"}


@app.get('/emotion/{scrape_id}')
async def run_emotion_in_background(scrape_id):
    print('called run emotion in background')
    # get file with emotions classified
    df = run_emotion(scrape_id)

    json_payload = {
        'scrape_id': scrape_id,
        'data': df.to_dict(orient='records')
    }

    return {"data": json_payload}


def run_classifiers_in_background(scrape_id, email):
    print('called classifiers')
    run_classifiers(scrape_id)
    # run_emotion(scrape_id)
    print('before req')

    send_request_to_express(scrape_id, email)
    print('after req')
    return

# @app.post('/testlexmo')
# async def test_lexmo(req: Request):
#     data = await req.json()
#     text = data['text']
#     return get_emotion_info(text)
