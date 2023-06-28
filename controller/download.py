from starlette.responses import FileResponse


def send_file(file_name):
    file_path = f"/text_data/completed/{file_name}"
    return FileResponse(file_path, filename=file_name)
