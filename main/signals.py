from .models import Anons,TgUser
from django.db.models.signals import pre_save
from django.core.signals import setting_changed
from .views import bot
from django.dispatch import receiver


@receiver(pre_save,sender=Anons)
def send_anons(sender, instance, **kwargs):
    if instance.photo:
        for user in TgUser.objects.all():
            bot.send_photo(chat_id=user.user_id, photo=instance.photo, caption=instance.text)