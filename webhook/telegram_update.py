class TelegramUpdate:
    def __init__(self, update):
        update_key = "message"
        try:
            update[update_key]
        except KeyError:
            update_key = "edited_message"

        self.id = update['update_id']
        self.message = update[update_key]['text']
        self.chat_id = update[update_key]['chat']['id']
        self.user_id = update[update_key]['from']['id']