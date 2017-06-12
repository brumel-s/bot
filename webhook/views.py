from django.http import HttpResponse
from bot import settings
import telepot
import urllib3
import pprint

if settings.IS_PYTHONANYWERE:
    proxy_url = "http://proxy.server:3128"
    telepot.api._pools = {
        'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
    }
    telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

TelegramBot = telepot.Bot(settings.BOT_TOCKEN)

def index(request):

    updates = TelegramBot.getUpdates();
    for update in updates:
        TelegramBot.sendMessage(update['message']['chat']['id'], "You said something")
        return HttpResponse(pprint.pformat(update['message']['chat']['id'], indent=4))
    #return HttpResponse(me['username'])