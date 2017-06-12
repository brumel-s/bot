from django.http import HttpResponse
from bot import settings
import telepot

TelegramBot = telepot.Bot(settings.BOT_TOCKEN)

def index(request):

    return HttpResponse(TelegramBot.getMe())