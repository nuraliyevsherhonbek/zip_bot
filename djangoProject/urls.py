from django.contrib import admin
from django.urls import path, include
from main.views import WebHook
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webhook/',csrf_exempt(WebHook.as_view()))
]
