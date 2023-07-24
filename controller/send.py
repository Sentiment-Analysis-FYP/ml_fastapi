from starlette.responses import FileResponse


def send_file(file_name):
    file_path = f"text_data/complete/{file_name}.csv"
    return FileResponse(file_path, filename=file_name)


def send_compilation():
    file_path = "text_data/compilation/compilation.csv"
    return FileResponse(file_path, filename="compilation.csv")
