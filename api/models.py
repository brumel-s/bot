from django.db import models


class TeleUser(models.Model):
    telegram_id = models.IntegerField()
    username = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    uni_api_key = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class ChatLog(models.Model):
    telegram_user = models.ForeignKey(TeleUser)
    request = models.TextField(max_length=255)
    response = models.TextField(max_length=255)

    def __str__(self):
        return "Request: " + self.request[:255] + "   Response :" + self.response[:100]