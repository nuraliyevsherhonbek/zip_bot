from django.shortcuts import render
from django.conf import settings
from telebot import TeleBot
from telebot.types import Update, Message, ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove
from django.views import View
from django.http import HttpResponse
import requests
import os
from .helper import delete_files, secure_folder_name
import shutil
from .models import TgUser, ZipFile
from .tasks import download_file


bot = TeleBot(settings.BOT_TOKEN)


class WebHook(View):
    def post(self, request):
        bot.process_new_updates([Update.de_json(request.body.decode("utf-8"))])
        return HttpResponse('ok')


@bot.message_handler(commands=['start'])
def start(message: Message):
    try:
        user = TgUser.objects.get(user_id=message.from_user.id)
    except TgUser.DoesNotExist:
        user = TgUser.objects.create(user_id=message.from_user.id)
    user.user_step = 0
    user.save()
    text = "Assalom Alaykum. ZipBot sizga filelaringizni ziplashga yordam beradi!"
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Yangi zip file yaratish')

    reply_markup.add(button, row_width=1)

    bot.send_message(message.chat.id, text=text, reply_markup=reply_markup)


@bot.message_handler(content_types="text")
def get_folder_name(message: Message):
    try:
        user = TgUser.objects.get(user_id=message.from_user.id)
    except TgUser.DoesNotExist:
        user = TgUser.objects.create(user_id=message.from_user.id)
    if message.text == 'Yangi zip file yaratish':
        try:
            delete_files(is_send=True)
            delete_files(is_send=False)
        except Exception as e:
            print(e)
        print(message.text)
        reply_markup = ReplyKeyboardRemove()
        user.user_step = 1
        user.save()
        text = 'Zip filening nomini kiriting!'
        bot.send_message(message.chat.id, text=text)

    elif user.user_step == 1:
        print(message.text)
        user.user_step = 2
        user.save()
        path = os.path.join('FILES', f"{message.from_user.id}/{message.text}_{secure_folder_name()}")
        os.makedirs(path)
        zip_file = ZipFile.objects.create(user=user, path=path)
        print(f"Zip file yaratildi:{zip_file}")
        text = "Endi filelari yuboring,Filelarni yuborib bo'lganinggizdan keyin 'Zip fileni olish' tugmasini bosing "
        bot.send_message(message.chat.id, text=text)
    elif user.user_step == 2 and message.text == "Zip fileni olish":
        reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button = KeyboardButton('Yangi zip file yaratish')
        reply_markup.add(button, row_width=1)
        zip_file = ZipFile.objects.filter(user=user).first()
        zip_ = shutil.make_archive(zip_file.path, 'zip', zip_file.path)
        file = open(zip_file.path+".zip", 'rb')
        user.user_step = 0
        user.save()
        zip_file.is_send = True
        zip_file.save()
        bot.send_document(message.chat.id, file, reply_markup=reply_markup)





@bot.message_handler(func=lambda message: True, content_types=['audio', 'video', 'document', 'photo'])
def get_files(message: Message):
    try:
        user = TgUser.objects.get(user_id=message.from_user.id)
    except TgUser.DoesNotExist:
        user = TgUser.objects.create(user_id=message.from_user.id)
    if user.user_step == 2:
        zip_file = ZipFile.objects.filter(user=user).first()
        path = zip_file.path
        print(message)

        if message.document:
            file = requests.get(
                f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getFile?file_id={message.document.file_id}"

            )
            open(f'{path}/{message.document.file_name}', 'wb').write(file.content)
        elif message.photo:
            file = requests.get(
                f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getFile?file_id={message.photo.file_id}"

            )
            open(f'{path}/{message.photo.file_name}', 'wb').write(file.content)
        elif message.video:
            file = requests.get(
                f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getFile?file_id={message.video.file_id}"
            )
            s = open(f'{path}/{message.video.file_name}', 'wb').write(file.content)
            print("File:",s)
        elif message.audio:
            file = requests.get(
                f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getFile?file_id={message.audio.file_id}"
            )
            open(f'{path}/{message.audio.file_name}', 'wb').write(file.content)
        text = "File yuboring!"
        if len(os.listdir(path)) >= 1:
            text = "Zip fileni olish uchun 'Zip fileni olish' tugmasinin bosing yoki boshqa file qoshmoqchi bo'lsangiz uni yuboring!! "
            reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
            button = KeyboardButton("Zip fileni olish")
            reply_markup.add(button, row_width=1)

        bot.send_message(message.chat.id, text=text, reply_markup=(reply_markup if reply_markup else None))


bot.polling()