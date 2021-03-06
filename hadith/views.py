import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from hadith.services import (
    get_responses,
    get_telegram_update_object,
    send_message,
    set_telegram_webhook,
)


@csrf_exempt
def respond(request):
    request_body = json.loads(request.body)
    update = get_telegram_update_object(request_body)
    try:
        chat_id = update.message.chat.id
        name = f"{update.message.chat.first_name} {update.message.chat.last_name}"
    except AttributeError:
        return HttpResponseBadRequest()
    # msg_id = update.message.message_id
    text = update.message.text.encode("utf-8").decode()
    responses = get_responses(text, chat_id, name)
    for response in responses:
        send_message(chat_id, response)
    return HttpResponse()


def set_webhook(request):
    webhook = set_telegram_webhook()
    if webhook:
        return HttpResponse("Webhook Set")

    return HttpResponseBadRequest("Webhook Setup Failure")
