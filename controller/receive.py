from os import path

from fastapi import UploadFile


async def receive_scrape(scrape_id: str, file: UploadFile = UploadFile(...)):
    save_directory = "/text_data/incomplete"
    file_path = path.join("text_data", "incomplete", f"{scrape_id}.json")
    # file_path = path.join(save_directory, f"{scrape_id}.json")

    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)

    except Exception:
        return {"message": "There was an error uploading the file"}

    finally:
        file.file.close()

    # with open(file_path, "wb") as buffer:
    #     buffer.write(await file.read())
    #
    # await file.close()
    return {"filename": f"{scrape_id}.json", "scrape_id": scrape_id}
