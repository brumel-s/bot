from api.uni_api import UniApi
from api.models import ChatLog
from api.exceptions import CmdException


class BaseCommand(object):
    """
    Base command
    """
    def run_api_query(self, cmd_name, params, user):
        """
        Run query to UniSender API

        :param cmd_name: string
        :param params: dict
        :param user: TeleUser
        :return: string
        """
        if not user.uni_api_key:
            raise CmdException("Set api key first! Use \"/setApiKey {apiKey}\"")

        api = UniApi(user.uni_api_key)
        response = api.run(cmd_name, params)
        self.log_request_response(user, cmd_name, response)

        return response

    def parse_arguments(self, text_cmd):
        """
        Fetch arguments from command string

        :param text_cmd: string
        :return: list
        """
        if ' ' in text_cmd:
            delimiter = ' '
        else:
            delimiter = '_'

        parts = text_cmd.split(delimiter)
        parts.pop(0)

        return parts

    def log_request_response(self, user, text_request, text_response):
        """
        Log request and response

        :param user: TeleUser
        :param text_request: string
        :param text_response: string
        :return: void
        """
        chat_log = ChatLog()
        chat_log.telegram_user = user
        chat_log.request = text_request[:255]
        chat_log.response = text_response[:255]
        chat_log.save()
