from api.api_commands.base_command import BaseCommand
import json
from datetime import datetime, timedelta
import pprint


class Campaigns(BaseCommand):
    """
    Show user campaigns
    """

    CMD_NAME = '/campaigns'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S';

    def is_acceptable(self, text_cmd):
        if text_cmd.startswith(self.CMD_NAME):
            return True
        return False

    def validate(self, text_cmd, user):
        return super(Campaigns, self).check_api_key(user)

    def run(self, telegram_update, user):
        text_cmd = telegram_update.message
        errors = self.validate(text_cmd, user)
        if errors:
            return super(Campaigns, self).prepare_error_response(errors.pop())

        api = super(Campaigns, self).get_api(user)

        dates = self.fetch_dates(text_cmd)
        text_response = self.prepare_text_response(api.run("getCampaigns", dates))
        super(Campaigns, self).log_request_response(user, text_cmd, text_response)

        return text_response

    def fetch_dates(self, text_cmd):

        date_from = datetime.today() - timedelta(days=30)
        date_from = date_from.strftime(self.DATE_FORMAT)

        date_to = datetime.today().strftime(self.DATE_FORMAT)

        if ' ' in text_cmd:
            parts = text_cmd.split(' ')
            pprint.pprint(parts)
            count = len(parts)
            if count == 3:
                try:
                    date_from = datetime.strptime(parts[1] + ' 00:00:00', self.DATE_FORMAT)
                except ValueError:
                    date_from = datetime.today() - timedelta(days=30)
                    date_from = date_from.strftime(self.DATE_FORMAT)
                try:
                    date_to = datetime.strptime(parts[2] + ' 23:59:59', self.DATE_FORMAT)
                except ValueError:
                    date_to = datetime.today().strftime(self.DATE_FORMAT)
            if count == 2:
                try:
                    date_from = datetime.strptime(parts[1] + ' 00:00:00', self.DATE_FORMAT)
                except ValueError:
                    date_from = datetime.today() - timedelta(days=30)

        return {"from": date_from, "to": date_to}


    def prepare_text_response(self, response):
        response = json.loads(response)
        if "error" in response.keys():
            return "Error: " + response['error']
        results = response['result']
        text_response = ""
        for result in results:
            text_response += "\r\n Id: {}".format(result["id"])
            text_response += "\r\n Subject: {}".format(result["subject"])
            text_response += "\r\n Status: {}".format(result["status"])
            text_response += "\r\n Show statistic: /campaignStats_{}".format(result["id"])
            text_response += "\r\n----------"
        return text_response

