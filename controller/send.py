from starlette.responses import FileResponse


def send_file(file_name):
    file_path = f"/text_data/completed/{file_name}"
    return FileResponse(file_path, filename=file_name)


def send_compilation():
    file_path = f"/text_data/compilation/compilation.csv"
    return FileResponse(file_path, filename="compilation.csv")
