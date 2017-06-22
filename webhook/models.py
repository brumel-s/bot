from django.db import models


class TeleUser(models.Model):
    telegram_id = models.IntegerField()
    uni_api_key = models.CharField(max_length=100)

    def __str__(self):
        return self.name