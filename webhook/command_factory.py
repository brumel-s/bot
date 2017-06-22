from webhook.api_commands.campaign_stats import CampaignStats
from webhook.api_commands.campaigns import Campaigns
from webhook.api_commands.set_api_key import SetApiKey


class CommandFactory:

    def __init__(self):
        self.commands = []
        self.commands.append(CampaignStats())
        self.commands.append(Campaigns())
        self.commands.append(SetApiKey())

    def create_cmd(self, textCmd, user):
        """
         Find acceptable command
         :param textCmd: Message text came from update
         :return: Command|None
         """
        for Cmd in self.commands:
            if Cmd.is_acceptable(textCmd):
                Cmd.set_user(user)
                return Cmd
        return None

    def get_help_str(self):
        """
        Get list of commands

        :return: string
        """
        cmd_list = []
        for Cmd in self.commands:
            cmd_list.append(Cmd.CMD_NAME)
        response = "\n\t".join(cmd_list)

        return response
