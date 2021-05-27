from .models import ZipFile, TgUser
from string import ascii_lowercase
from random import choice
import shutil
import os

def delete_files(is_send=True):
    zips = ZipFile.objects.filter(is_send=is_send)
    print(zips)
    for i in zips:
        print(i.path)
        shutil.rmtree(i.path)
        os.remove(i.path+".zip")
        i.delete()


def secure_folder_name():
    text = ""
    for _ in range(10):
        text += choice(ascii_lowercase)
    return text




