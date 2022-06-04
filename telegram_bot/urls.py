from django.contrib import admin
from django.urls import path

from telegram_bot.credentials import BOT_TOKEN

from hadith.views import respond, set_webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{BOT_TOKEN}', respond),
    path('setwebhook', set_webhook)
]
