from os import path

from fastapi import UploadFile


async def receive_scrape(scrape_id: str, file: UploadFile = UploadFile(...)):
    file_path = f"text_data/incomplete/{scrape_id}.csv"

    try:
        contents = file.file.read()
        with open(file_path, 'wb') as f:
            f.write(contents)

    except Exception:
        return {"message": "There was an error uploading the file"}

    finally:
        file.file.close()

    # with open(file_path, "wb") as buffer:
    #     buffer.write(await file.read())
    #
    # await file.close()
    return {"filename": f"{scrape_id}.csv", "scrape_id": scrape_id}
