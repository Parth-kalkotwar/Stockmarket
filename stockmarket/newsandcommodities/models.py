from django.db import models


class Commodity(models.Model):
    name = models.CharField(max_length=250)
    symbol = models.CharField(max_length=100, null=True, blank=True)
    price = models.CharField(max_length=2000)
    change = models.CharField(max_length=100)
    change_perc = models.CharField(max_length=250, null=True, blank=True)
    high = models.FloatField(max_length=100, null=True, blank=True)
    low = models.FloatField(max_length=100, null=True, blank=True)
    latestVolume = models.CharField(max_length=1000, null=True, blank=True)
    open = models.CharField(max_length=1000, null=True, blank=True)
    previousClose = models.CharField(max_length=1000, null=True, blank=True)
    close = models.CharField(max_length=1000, null=True, blank=True)
    exchange = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name





