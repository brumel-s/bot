from webhook.api_commands.base_command import BaseCommand


class CampaignStats(BaseCommand):
    """
    Show campaign statistic command
    """
    CMD_NAME = '/campaignStats'

    def is_acceptable(self, cmd):
        if cmd.startswith(self.CMD_NAME):
            return True
        return False

    def validate(self, text_cmd):
        errors = super(CampaignStats, self).check_api_key()
        campaign_id = self.fetch_campaign_id(text_cmd)
        try:
            campaign_id = int(campaign_id)
            if campaign_id <= 0:
                errors.append("Campaign id should be a number equal or greater 0")
        except ValueError:
            errors.append('Campaign id should be a number!')

        return errors

    def run(self, textCmd):
        errors = self.validate(textCmd)
        if errors:
            return super(CampaignStats, self).prepare_error_response(errors.pop())
        api = super(CampaignStats, self).get_api()
        campaign_id = self.fetch_campaign_id(textCmd)
        response = api.run("getCampaignCommonStats", {"campaign_id": campaign_id})

        return self.prepare_text_response(response)

    def fetch_campaign_id(self, text_cmd):
        arguments = super(CampaignStats, self).parse_arguments(text_cmd)
        return arguments[0]

    def prepare_text_response(self, response):

        return response
