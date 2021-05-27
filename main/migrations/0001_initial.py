# Generated by Django 3.2.3 on 2021-05-26 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=2000)),
                ('photo', models.ImageField(blank=True, upload_to='anons/photos/')),
                ('video', models.FileField(blank=True, upload_to='anons/videos/')),
            ],
            options={
                'verbose_name_plural': 'Anons',
            },
        ),
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=20, unique=True)),
                ('user_step', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ZipFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=300)),
                ('is_send', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zip_files', to='main.tguser')),
            ],
        ),
    ]
