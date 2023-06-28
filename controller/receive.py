from os import path

from fastapi import UploadFile


def receive_scrape(scrape_id: str, file: UploadFile = UploadFile(...)):
    save_directory = "/text_data/incomplete"
    file_path = path.join(save_directory, f"{scrape_id}.json")

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {"filename": f"{scrape_id}.json", "scrape_id": scrape_id}
