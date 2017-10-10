from api.api_commands.base_command import BaseCommand
import json
from api.exceptions import CmdException

class GetLists(BaseCommand):
    """
    Show user lists
    """

    CMD_NAME = '/getLists'

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
        Fetch start and end dates from command string

        :param text_cmd: string
        :return: int
        """
        response = super(GetLists, self).run_api_query("getLists", {}, user)
        response = self.prepare_telegram_response(response)

        bot.sendMessage(telegram_update.chat_id, response)

    def prepare_telegram_response(self, response):
        """
        Prepare user-readable response
        :param response: string
        :return: string
        """
        response = json.loads(response)
        if "error" in response.keys():
            raise CmdException(response['error'])
        results = response['result']
        if len(results) == 0:
            return 'Списки не найдены'

        text_response = ""
        for result in results:
            text_response += "\r\nId: {}, Title: {}" \
                             "\r\n----------".format(result["id"], result["title"])
        text_response += "\r\nИспользуйте /subscribe {listId} {email} для добавления email-адреса в список"

        return text_response

