from django.core.management.base import BaseCommand
from bot import settings
import telepot, time, urllib3, logging, pprint
from webhook.parsers import ParserDefault
from webhook.command_factory import CommandFactory
from webhook.telegram_update import TelegramUpdate

from webhook.models import TeleUser


if settings.IS_PYTHONANYWERE:
    proxy_url = "http://proxy.server:3128"
    telepot.api._pools = {
        'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
    }
    telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

TelegramBot = telepot.Bot(settings.BOT_TOCKEN)


class Command(BaseCommand):
    help = 'Process Telegram updates'

    def __init__(self):
        super(Command, self).__init__()
        self.parsersList = []
        self.parsersList.append(ParserDefault())

    def handle(self, *args, **options):
        offset = None
        cmd_factory = CommandFactory()
        while 1:
            updates = self.get_telegram_updates(offset)

            for update in updates:

                offset = update.id + 1

                response_message = None

                user = self.fetch_or_create_user(update.user_id)

                cmd = cmd_factory.create_cmd(update.message, user)
                if cmd is not None:
                    response_message = cmd.run(update.message)

                if response_message is None:
                    response_message = self.answer_text_message(update.message)

                if response_message is None:
                    response_message = "I don't understand you. But you are able to use commands:"\
                                       + cmd_factory.get_help_str()

                TelegramBot.sendMessage(update.chat_id, response_message)

            #break
            time.sleep(10)

    def get_telegram_updates(self, offset):
        updates = TelegramBot.getUpdates(offset)
        telegram_updates = []
        for update in updates:
            telegram_updates.append(TelegramUpdate(update))

        return telegram_updates

    def answer_text_message(self, message):
        """
        Parse message text and return response message

        :param message:
        :return: string
        """
        response_message = None
        for parser in self.parsersList:
            response_message = parser.parse(message)
            if response_message is not None:
                break

        return response_message

    def fetch_or_create_user(self, telegram_user_id):
        """
        Fetch or create user
        :param telegram_user_id: int
        :return: TeleUser
        """
        try:
            user = TeleUser.objects.get(telegram_id=telegram_user_id)
        except TeleUser.DoesNotExist:
            user = TeleUser()
            user.telegram_id = telegram_user_id
            user.save()

        return user
