from api.api_commands.base_command import BaseCommand
import json
from datetime import datetime, timedelta
import pprint
from api.exceptions import CmdException

class Campaigns(BaseCommand):
    """
    Show user campaigns
    """

    CMD_NAME = '/campaigns'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

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
        dates = self.fetch_dates(telegram_update.message)
        response = super(Campaigns, self).run_api_query("getCampaigns", dates, user)
        response = self.prepare_telegram_response(response)

        bot.sendMessage(telegram_update.chat_id, response)

    def fetch_dates(self, text_cmd):
        """
        Fetch start and end dates from command string

        :param text_cmd: string
        :return: dict
        """
        date_from = datetime.today() - timedelta(days=30)
        date_from = date_from.strftime(self.DATE_FORMAT)

        date_to = datetime.today().strftime(self.DATE_FORMAT)

        args = super(Campaigns, self).parse_arguments(text_cmd)
        count = len(args)
        if count == 2:
            try:
                date_from = datetime.strptime(args[0] + ' 00:00:00', self.DATE_FORMAT)
            except ValueError:
                raise CmdException("Неверный формат даты \"От\"")
            try:
                date_to = datetime.strptime(args[1] + ' 23:59:59', self.DATE_FORMAT)
            except ValueError:
                raise CmdException("Неверный формат даты \"До\"")
        if count == 1:
            try:
                date_from = datetime.strptime(args[0] + ' 00:00:00', self.DATE_FORMAT)
            except ValueError:
                raise CmdException("Неверный формат даты \"От\"")

        return {"from": date_from, "to": date_to}


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
            return 'Кампании за данный промежуток времени не найдены'

        response = ''
        for result in results:
            response += "\r\nId: {}" \
                       "\r\nSubject: {}" \
                       "\r\nStatus: {}" \
                       "\r\nShow statistic: /campaignStats_{}" \
                       "\r\n----------".format(
                                           result["id"],
                                           result["subject"],
                                           result["status"],
                                           result["id"]
                                        )

        return response

