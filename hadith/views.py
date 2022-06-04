import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from hadith.services import create_chat, get_response, get_telegram_update_object, send_message, set_telegram_webhook


@csrf_exempt
def respond(request):
    request_body = json.loads(request.body)
    update = get_telegram_update_object(request_body)
    chat_id = update.message.chat.id
    # msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    response = get_response(text)

    if text == "/subscribe":
        create_chat(chat_id)

    send_message(chat_id, response)
    return HttpResponse()


def set_webhook(request):
    webhook = set_telegram_webhook()
    if webhook:
        return HttpResponse("Webhook Set")

    return HttpResponseBadRequest("Webhook Setup Failure")
