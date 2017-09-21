from api.api_commands.base_command import BaseCommand
import json


class CampaignStats(BaseCommand):
    """
    Show campaign statistic command
    """
    CMD_NAME = '/campaignStats'

    def is_acceptable(self, cmd):
        if cmd.startswith(self.CMD_NAME):
            return True
        return False

    def validate(self, text_cmd, user):
        errors = super(CampaignStats, self).check_api_key(user)
        campaign_id = self.fetch_campaign_id(text_cmd)
        if campaign_id is None:
            errors.append("Campaign id is not set")
        try:
            campaign_id = int(campaign_id)
            if campaign_id <= 0:
                errors.append("Campaign id should be a number equal or greater 0")
        except ValueError:
            errors.append('Campaign id should be a number!')
        except:
            pass

        return errors

    def run(self, bot, telegram_update, user):
        text_cmd = telegram_update.message
        errors = self.validate(text_cmd, user)
        if errors:
            return super(CampaignStats, self).prepare_error_response(errors.pop())
        api = super(CampaignStats, self).get_api(user)
        campaign_id = self.fetch_campaign_id(text_cmd)
        response = api.run("getCampaignCommonStats", {"campaign_id": campaign_id})
        response = self.prepare_text_response(response)

        super(CampaignStats, self).log_request_response(user, text_cmd, response)

        bot.sendMessage(telegram_update.chat_id, response)

    def fetch_campaign_id(self, text_cmd):
        arguments = super(CampaignStats, self).parse_arguments(text_cmd)
        id = None
        if arguments:
            id = arguments[0]
        return id

    def prepare_text_response(self, response):
        response = json.loads(response)
        result = response['result']

        text_response = ""
        text_response += "\r\n----------"
        text_response += "\r\n Total: {}".format(result['total'])
        text_response += "\r\n Sent: {}".format(result['sent'])
        text_response += "\r\n Delivered: {}".format(result['delivered'])
        text_response += "\r\n Read unique: {}".format(result['read_unique'])
        text_response += "\r\n Read all: {}".format(result['read_all'])
        text_response += "\r\n Clicked unique: {}".format(result['clicked_unique'])
        text_response += "\r\n Clicked all: {}".format(result['clicked_all'])
        text_response += "\r\n Unsubscribed: {}".format(result['unsubscribed'])
        text_response += "\r\n Spam: {}".format(result['spam'])
        text_response += "\r\n----------"

        return text_response
