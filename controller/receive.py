from os import path

from fastapi import UploadFile


async def receive_scrape(scrape_id: str, file: UploadFile = UploadFile(...)):
    file_path = f"text_data/incomplete/{scrape_id}.csv"

    try:
        contents = file.file.read()

        # insert analysis here
        with open(file_path, 'wb') as f:
            f.write(contents)

    except Exception as e:
        return {"message": f"There was an error uploading the file: \n{e}"}

    finally:
        file.file.close()

    # return would be analyzed document
    return {"filename": f"{scrape_id}.csv", "scrape_id": scrape_id}
