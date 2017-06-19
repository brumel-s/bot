from django.core.management.base import BaseCommand
from bot import settings
import telepot, time, urllib3, logging, pprint
from webhook.parsers import ParserDefault
from webhook.commands import CampaignStats
from webhook.models import TeleUser
from webhook.exceptions import CmdException

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
        self.commands = []
        self.commands.append(CampaignStats())

    def handle(self):
        offset = None
        while 1:
            updates = TelegramBot.getUpdates(offset)
            for update in updates:
                offset = update['update_id'] + 1

                response_message = None
                #logger = logging.getLogger('bot_log')
                #logger.info(pprint.pformat(update))
                update_key = "message"
                try:
                    update[update_key]
                except KeyError:
                    update_key = "edited_message"

                update_message = update[update_key]['text']
                update_chat_id = update[update_key]['chat']['id']

                try:
                    result = self.run_command(update_message)
                    if result:
                        response_message = "Done!"
                except CmdException as e:
                    response_message = str(e)

                if response_message is None:
                    response_message = self.answer_text_message(update_message)

                TelegramBot.sendMessage(update_chat_id, response_message)

            #break
            time.sleep(10)

    def run_command(self, textCmd):
        """
        Find acceptable command and run it

        :param textCmd: Message text came from update
        :return: bool
        """
        for Cmd in self.commands:
            if Cmd.is_acceptable(textCmd):
                errors = Cmd.validate(textCmd)
                if errors:
                    raise CmdException(errors.pop())
                Cmd.run(textCmd)
                return True
        return False

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
        if response_message is None:
            response_message = "I don't understand you. But you are able to use commands:" + self.get_help_str()

        return response_message

    def get_help_str(self):
        """
        Get list of commands

        :return: string
        """
        cmd_list = []
        for Cmd in self.commands:
            cmd_list.append(Cmd.CMD_NAME)
        response = "\n\t".join(cmd_list)

        return response
