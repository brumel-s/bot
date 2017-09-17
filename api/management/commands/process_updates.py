from django.core.management.base import BaseCommand
from bot import settings
import telepot, time, urllib3, logging
from pprint import pprint
from api.parsers import ParserDefault
from api.command_factory import CommandFactory
from api.telegram_update import TelegramUpdate
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

from api.models import TeleUser


#if settings.IS_PYTHONANYWERE:
#    proxy_url = "http://proxy.server:3128"
#    telepot.api._pools = {
#        'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
#    }
#    telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

TelegramBot = telepot.Bot(settings.BOT_TOCKEN)


class Command(BaseCommand):
    help = 'Process Telegram updates'

    def __init__(self):
        super(Command, self).__init__()
        self.parsersList = []
        self.parsersList.append(ParserDefault())

    def handle(self, *args, **options):
        TelegramBot.message_loop(self.process_updates)
        while 1:
            time.sleep(10)

    def process_updates(self, update):

        update = TelegramUpdate(update)

        cmd_factory = CommandFactory()

        response_message = None

        user = self.fetch_or_create_user(update)

        cmd = cmd_factory.create_cmd(update)
        if cmd is not None:
            response_message = cmd.run(update, user)

        if response_message is None:
            response_message = self.answer_text_message(update.message)

        if user.phone is None:
            TelegramBot.sendMessage(update.chat_id, 'Please, share you phone and we will try ti set up you api key',
                                    reply_markup=ReplyKeyboardMarkup(
                                        keyboard=[
                                            [KeyboardButton(text='Share contact', request_contact=True)]
                                        ],
                                        one_time_keyboard=True
                                    ))
            return

        if response_message is None:
            response_message = "I don't understand you. But you are able to use commands:"\
                               + self.get_help_str(cmd_factory)

        TelegramBot.sendMessage(update.chat_id, response_message)

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

    def fetch_or_create_user(self, telegram_update):
        """
        Fetch or create user
        :param telegram_user_id: int
        :return: TeleUser
        """
        try:
            user = TeleUser.objects.get(telegram_id=telegram_update.user_id)
        except TeleUser.DoesNotExist:
            user = TeleUser()
            user.telegram_id = telegram_update.user_id
            user.username = telegram_update.username
            user.save()

        return user


    def get_help_str(self, cmd_factory):
        """
        Get list of commands

        :return: string
        """

        cmd_list = []
        for Cmd in cmd_factory.commands:
            cmd_list.append(Cmd.CMD_NAME)
        response = "\n\t".join(cmd_list)

        return response
