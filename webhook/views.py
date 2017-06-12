from django.http import HttpResponse
from bot import settings
import telepot
import pprint

TelegramBot = telepot.Bot(settings.BOT_TOCKEN)

def index(request):

    updates = TelegramBot.getUpdates();
    for update in updates:
        TelegramBot.sendMessage(update['message']['chat']['id'], "You said something")
        return HttpResponse(pprint.pformat(update['message']['chat']['id'], indent=4))
    #return HttpResponse(me['username'])