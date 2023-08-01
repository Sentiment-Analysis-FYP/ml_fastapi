import pandas
from starlette.responses import FileResponse


def send_file(file_name):
    file_path = f"text_data/emotion/{file_name}.csv"
    df = pandas.read_csv(file_path, encoding='utf-8')
    json_payload = {
        'scrape_id': file_name,
        'data': df.to_dict(orient='records')
    }
    return json_payload
    # return FileResponse(file_path, filename=file_name)


def send_compilation():
    file_path = "text_data/compilation/compilation.csv"
    return FileResponse(file_path, filename="compilation.csv")
