import logging, pprint

class CampaignStats():

    CMD_NAME = '/campaignStats'

    def is_acceptable(self, cmd):
        if cmd.startswith(self.CMD_NAME):
            return True
        return False

    def validate(self, cmd):
        parts = cmd.partition(' ')
        campaign_id = parts[2]
        errors = []
        try:
            campaign_id = int(campaign_id)
            if campaign_id <= 0:
                errors.append("Campaign id should be a number equal or greater 0")
        except ValueError:
            errors.append('Campaign id should be a number!')

        return errors

    def run(self, command):
        logger = logging.getLogger('bot_log')
        logger.info(pprint.pformat("Running" + command))