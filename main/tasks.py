from celery import shared_task
from djangoProject.celery import app
import requests
from django.conf import settings


@app.task()
def download_file(file_path, file_id, file_name):
    response = requests.get(
        f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getFile?file_id={file_id}",
        stream=True
    )
    with open(f'{file_path}/{file_name}', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()

    print("Done")
