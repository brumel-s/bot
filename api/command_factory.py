from api.api_commands.campaign_stats import CampaignStats
from api.api_commands.campaigns import Campaigns
from api.api_commands.set_api_key import SetApiKey
from api.api_commands.save_phone import SavePhone
from pprint import pprint

class CommandFactory:

    def __init__(self):
        self.commands = []
        self.commands.append(CampaignStats())
        self.commands.append(Campaigns())
        self.commands.append(SetApiKey())

    def create_cmd(self, update):
        """
         Find acceptable command
         :param text_cmd: Message text came from update
         :return: Command|None
         """

        if update.phone is not None:
            return SavePhone()

        for Cmd in self.commands:
            if Cmd.is_acceptable(update.message):
                return Cmd
        return None
