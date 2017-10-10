from api.api_commands.campaign_stats import CampaignStats
from api.api_commands.campaigns import Campaigns
from api.api_commands.set_api_key import SetApiKey
from api.api_commands.save_phone import SavePhone
from api.api_commands.get_lists import GetLists
from api.api_commands.subscribe import Subscribe
from api.api_commands.start import Start
from api.api_commands.help import Help


class CommandFactory:
    """
    Commands factory
    """

    def __init__(self):
        """
        Append available commands
        """
        self.commands = []
        self.commands.append(Start())
        self.commands.append(CampaignStats())
        self.commands.append(Campaigns())
        self.commands.append(SetApiKey())
        self.commands.append(GetLists())
        self.commands.append(Subscribe())
        self.commands.append(Help())

    def create_cmd(self, update, user):
        """
        Get command by telegram message

        :param update: TelegramUpdate
        :param user: Teleuser
        :return: BaseCommand|None
        """
        if update.phone is None and update.message.startswith(SetApiKey.CMD_NAME):
            return SetApiKey()

        if update.phone is None and not user.phone and not user.uni_api_key:
            return Start()

        if update.phone is not None:
            return SavePhone()

        for Cmd in self.commands:
            if Cmd.is_acceptable(update.message):
                return Cmd

        return Help()
