from api.api_commands.base_command import BaseCommand
import json
from api.exceptions import CmdException

class CampaignStats(BaseCommand):
    """
    Show campaign statistic command
    """
    CMD_NAME = '/campaignStats'

    def is_acceptable(self, cmd):
        """
        Check is command should be runned

        :param cmd: string
        :return: bool
        """
        if cmd.startswith(self.CMD_NAME):
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
        params = {"campaign_id": self.fetch_campaign_id(telegram_update.message)}
        response = super(CampaignStats, self).run_api_query("getCampaignCommonStats", params, user)
        response = self.prepare_telegram_response(response)

        bot.sendMessage(telegram_update.chat_id, response)

    def fetch_campaign_id(self, text_cmd):
        """
        Fetch campaign id from command string

        :param text_cmd: string
        :return: int
        """
        args = super(CampaignStats, self).parse_arguments(text_cmd)
        if len(args) < 1:
            raise CmdException("Ошибка! Не указан id кампании")
        try:
            campaign_id = int(args[0])
            if campaign_id <= 0:
                raise CmdException("Ошибка! Id кампании должно быть целым положительным числом")
        except ValueError:
            raise CmdException("Ошибка! Id кампании должно быть целым положительным числом")

        return campaign_id

    def prepare_telegram_response(self, response):
        """
        Prepare user-readable response
        :param response: string
        :return: string
        """
        response = json.loads(response)
        if "error" in response.keys():
            raise CmdException(response['error'])

        result = response['result']
        response = "\r\n----------" \
                   "\r\nTotal: {}" \
                   "\r\n Sent: {}" \
                   "\r\n Delivered: {}" \
                   "\r\n Read unique: {}" \
                   "\r\n Read all: {}" \
                   "\r\n Clicked unique: {}" \
                   "\r\n Clicked all: {}" \
                   "\r\n Unsubscribed: {}" \
                   "\r\n Spam: {}" \
                   "\r\n----------".format(
                                        result['total'],
                                        result['sent'],
                                        result['delivered'],
                                        result['read_unique'],
                                        result['read_all'],
                                        result['clicked_unique'],
                                        result['clicked_all'],
                                        result['unsubscribed'],
                                        result['spam']
                                    )

        return response
