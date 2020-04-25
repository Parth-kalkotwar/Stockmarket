from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    symbol = models.CharField(max_length=100, null=True,blank=True)
    price = models.CharField(max_length=2000)
    change = models.CharField(max_length=100)
    change_perc = models.CharField(max_length=250,null=True,blank=True)
    high = models.FloatField(max_length=100,null=True,blank=True)
    low = models.FloatField(max_length=100,null=True,blank=True)
    latestVolume = models.CharField(max_length=1000,null=True,blank=True)
    open = models.CharField(max_length=1000,null=True,blank=True)
    previousClose = models.CharField(max_length=1000, null=True, blank=True)
    close = models.CharField(max_length=1000, null=True, blank=True)
    exchange = models.CharField(max_length=250,null=True,blank=True)
    is_active = models.BooleanField(default=False)
    is_loser = models.BooleanField(default=False)
    is_gainer  = models.BooleanField(default=False)
    pred_img = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000,blank=True, null=True)
    img = models.CharField(max_length=1000, null=True, blank=True)
    subject = models.CharField(max_length=250, blank=True, null=True)
    timestamp = models.DateField(auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return self.title

