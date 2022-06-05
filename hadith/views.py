import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from hadith.services import (
    create_chat,
    get_response,
    get_telegram_update_object,
    send_message,
    set_telegram_webhook,
    update_language_preference,
)
from hadith.constants import LANGUAGE_COMMAND, SUBSCRIBE_COMMAND, SUPPORTED_LANGUAGES

@csrf_exempt
def respond(request):
    request_body = json.loads(request.body)
    update = get_telegram_update_object(request_body)
    chat_id = update.message.chat.id
    # msg_id = update.message.message_id
    text = update.message.text.encode("utf-8").decode()
    response = get_response(text, chat_id)

    if text == SUBSCRIBE_COMMAND:
        create_chat(chat_id)

    if LANGUAGE_COMMAND in text:
        language = text.split()[-1]
        language = language.lower()
        if language in SUPPORTED_LANGUAGES:
            create_chat(chat_id)
            update_language_preference(chat_id, language)

    send_message(chat_id, response)
    return HttpResponse()


def set_webhook(request):
    webhook = set_telegram_webhook()
    if webhook:
        return HttpResponse("Webhook Set")

    return HttpResponseBadRequest("Webhook Setup Failure")
