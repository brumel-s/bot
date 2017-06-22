from webhook.api_commands.base_command import BaseCommand
import json


class Campaigns(BaseCommand):
    """
    Show user campaigns
    """

    CMD_NAME = '/campaigns'

    def is_acceptable(self, text_cmd):
        if text_cmd.startswith(self.CMD_NAME):
            return True
        return False

    def validate(self, text_cmd):
        return super(Campaigns, self).check_api_key()

    def run(self, text_cmd):
        errors = self.validate(text_cmd)
        if errors:
            return super(Campaigns, self).prepare_error_response(errors.pop())

        api = super(Campaigns, self).get_api()

        return self.prepare_text_response(api.run("getCampaigns", {}))

    def prepare_text_response(self, response):
        response = json.loads(response)
        results = response['result']
        text_response = "";
        for result in results:
            text_response += "\r\n----------"
            text_response += "\r\n Id: {}".format(result["id"])
            text_response += "\r\n Subject: {}".format(result["subject"])
            text_response += "\r\n Status: {}".format(result["status"])
            text_response += "\r\n Show statistic: /campaignStats_{}".format(result["id"])
            text_response += "\r\n----------"
        return text_response

