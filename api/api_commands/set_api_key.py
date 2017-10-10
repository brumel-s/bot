from api.api_commands.base_command import BaseCommand
from api.exceptions import CmdException

class SetApiKey(BaseCommand):
    """
    Set user api key
    """

    CMD_NAME = '/setApiKey'

    def is_acceptable(self, text_cmd):
        """
        Check is command should be runned

        :param cmd: string
        :return: bool
        """
        if text_cmd.startswith(self.CMD_NAME):
            return True
        return False

    def run(self, bot, telegram_update, user):
        """
        Run command and send response to user

        :param bot: Bot
        :param telegram_update: TelegramUpdate
        :param user: TeleUser
        :return: void
        """
        api_key = self.fetch_api_key(telegram_update.message)
        user.uni_api_key = api_key
        user.save()

        bot.sendMessage(telegram_update.chat_id, 'Апи ключ установлен')

    def fetch_api_key(self, text_cmd):
        """
        Fetch API key from command string

        :param text_cmd: string
        :return: string
        """
        args = super(SetApiKey, self).parse_arguments(text_cmd)
        if len(args) < 1:
            raise CmdException("Ошибка! API ключ является обазязательным аргументом")

        return args[0]


