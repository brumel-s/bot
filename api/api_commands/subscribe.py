from api.api_commands.base_command import BaseCommand
import json
import pprint
from api.exceptions import CmdException

class Subscribe(BaseCommand):
    """
    Subscribe provided email to list
    """

    CMD_NAME = '/subscribe'

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
        subscribe_params = self.fetch_params(telegram_update.message)
        response = super(Subscribe, self).run_api_query("subscribe", subscribe_params, user)
        response = self.prepare_telegram_response(response)
        bot.sendMessage(telegram_update.chat_id, response)

    def fetch_params(self, text_cmd):
        """
        Fetch listId and email from command string

        :param text_cmd: string
        :return: dict
        """
        args = super(Subscribe, self).parse_arguments(text_cmd)
        if len(args) < 2:
            raise CmdException("Ошибка! Id списка или имейл")
        try:
            list_id = int(args[0])
            if list_id <= 0:
                raise CmdException("Ошибка! Id списка должно быть целым положительным числом")
        except ValueError:
            raise CmdException("Ошибка! Id списка должно быть целым положительным числом")

        return {"list_ids": args[0], "fields[email]": args[1]}

    def prepare_telegram_response(self, response):
        """
        Prepare user-readable response
        :param response: string
        :return: string
        """
        response = json.loads(response)
        if "error" in response.keys():
            raise CmdException(response['error'])
        if "result" not in response.keys():
            raise CmdException("При добавлении имейла произошла ошибка")

        return "Имейл добавлен в список"

