from django.db import models


class TgUser(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    user_step = models.PositiveIntegerField(default=0)


class ZipFile(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE, related_name='zip_files')
    path = models.CharField(max_length=300)
    is_send = models.BooleanField(default=False)


class Anons(models.Model):
    text = models.TextField(max_length=2000)
    photo = models.ImageField(upload_to='anons/photos/',blank=True)
    video = models.FileField(upload_to='anons/videos/',blank=True)

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name_plural = 'Anons'

