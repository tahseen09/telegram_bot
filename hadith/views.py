import json
import telegram

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from hadith.services import get_random_hadith

from telegram_bot.credentials import BOT_TOKEN, APP_URL

bot = telegram.Bot(token=BOT_TOKEN)


@csrf_exempt
def respond(request):
    request_body = json.loads(request.body)
    update = telegram.Update.de_json(request_body, bot)
    chat_id = update.message.chat.id
    # msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    if text == "/start":
        response = "Assalamu-aliakum! Use this bot to read Hadiths and make your day better. You can message anything and you shall receive a hadith in response. Jazakallah"
    else:
        response = get_random_hadith()
    bot.sendMessage(chat_id=chat_id, text=response)
    return HttpResponse()


def set_webhook(request):
    webhook = bot.setWebhook(f"{APP_URL}{BOT_TOKEN}")
    if webhook:
        return HttpResponse("Webhook Set")

    return HttpResponseBadRequest("Webhook Setup Failure")
