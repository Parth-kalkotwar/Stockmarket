import os
from sqlite3 import IntegrityError

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
#from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render
import json
import requests
from django.utils import timezone
from django.views.generic import ListView, DetailView
from .models import Company, News
import csv
from newsandcommodities.views import get_com
from .lstm import get_preds



def listview(request):
    query = request.GET.get("q", None)
    """for row in Company.objects.all().reverse():
        if Company.objects.filter(name=row.name).count() > 1:
            row.delete()"""
    companies = Company.objects.all()[40:100]
    if query is not None:
        companies = Company.objects.all()
        companies = companies.filter(Q(name__icontains=query) |
                                     Q(symbol__icontains=query) |
                                     Q(exchange__icontains=query)
                                     )
    return render(request, template_name='elements.html', context={"companies": companies})


def companydetails(request, pk):
    obj = Company.objects.get(pk=pk)
    url = 'https://financialmodelingprep.com/api/v3/quote/' + obj.symbol
    raw_data = requests.get(url).json()
    obj.price = raw_data[0]['price']
    obj.change = raw_data[0]['change']
    obj.change_perc = raw_data[0]['changesPercentage']
    obj.low = raw_data[0]['dayLow']
    obj.high = raw_data[0]['dayHigh']
    obj.latestVolume = raw_data[0]['volume']
    obj.open = raw_data[0]['open']
    obj.previousClose = raw_data[0]['previousClose']
    obj.save()
    news = News.objects.order_by('-timestamp')
    return render(request, template_name='details.html', context={"company": obj,
                                                                  "news": news,
                                                                  })


def get_actives():
    """try:

        url = 'https://financialmodelingprep.com/api/v3/stock/actives'
        raw_data = requests.get(url).json()
        for i in range(len(raw_data['mostActiveStock'])):
            name = raw_data['mostActiveStock'][i]['companyName']
            change = raw_data['mostActiveStock'][i]['changes']
            price = raw_data['mostActiveStock'][i]['price']
            symbol = raw_data['mostActiveStock'][i]['ticker']
            try:
                obj = Company.objects.filter(name=name).first()
                obj.is_active = True
                obj.change = change
                obj.price = price
                obj.symbol = symbol
                obj.save()
            except (ObjectDoesNotExist, AttributeError, IntegrityError):
                obj = Company()
                obj.name = name
                obj.price = price
                obj.change = change
                obj.is_active = True
                obj.symbol = symbol
                obj.save()
    except:"""
    objects = Company.objects.filter(is_active=True)
    return objects


def get_gainers():
    url = 'https://financialmodelingprep.com/api/v3/stock/gainers'
    raw_data = requests.get(url).json()
    for i in range(len(raw_data['mostGainerStock'])):
        name = raw_data['mostGainerStock'][i]['companyName']
        change = raw_data['mostGainerStock'][i]['changes']
        price = raw_data['mostGainerStock'][i]['price']
        symbol = raw_data['mostGainerStock'][i]['ticker']
        try:
            obj = Company.objects.filter(name=name).first()
            obj.is_gainer = True
            obj.change = change
            obj.price = price
            obj.symbol = symbol
            obj.save()
        except (ObjectDoesNotExist, AttributeError,IntegrityError):
            obj = Company()
            obj.name = name
            obj.price = price
            obj.change = change
            obj.symbol = symbol
            obj.is_gainer = True
            obj.save()
    objects = Company.objects.filter(is_gainer=True)
    return objects


def get_losers():
    url = 'https://financialmodelingprep.com/api/v3/stock/losers'
    raw_data = requests.get(url).json()
    for i in range(len(raw_data['mostLoserStock'])):
        name = raw_data['mostLoserStock'][i]['companyName']
        change = raw_data['mostLoserStock'][i]['changes']
        price = raw_data['mostLoserStock'][i]['price']
        symbol = raw_data['mostLoserStock'][i]['ticker']
        try:
            obj = Company.objects.filter(name=name).first()
            obj.is_loser = True
            obj.change = change
            obj.price = price
            obj.symbol = symbol
            obj.save()
        except (ObjectDoesNotExist, AttributeError, IntegrityError):
            obj = Company()
            obj.name = name
            obj.price = price
            obj.change = change
            obj.is_loser = True
            obj.symbol = symbol
            obj.save()
    objects = Company.objects.filter(is_loser=True)
    return objects


def initialize():
    url = 'https://financialmodelingprep.com/api/v3/company/stock/list'
    raw_data = requests.get(url).json()
    for i in range(0,2):
        name = raw_data['symbolsList'][i]['name']
        symbol = raw_data['symbolsList'][i]['symbol']
        price = raw_data['symbolsList'][i]['price']
        exchange = raw_data['symbolsList'][i]['exchange']
        if Company.objects.filter(name=name).exists():
            pass
        else:
            obj = Company()
            obj.name = name
            obj.price = price
            obj.symbol = symbol
            obj.exchange = exchange
            obj.save()


def homepage(request):
    #initialize()
    try:
        top_gainers = get_gainers()
        top_losers = get_losers()
        top_actives = get_actives()
    except IntegrityError:
        pass
    news_title, news_description, news_img, subject = get_news()
    for i in range(len(news_img)):
        obj = News()
        obj.title = news_title[i]
        obj.description = news_description[i]
        obj.img = news_img[i]
        obj.subject = subject
        obj.save()
    #news = zip(news_title, news_description, news_img, subject)
    news = News.objects.order_by('-timestamp')
    apple_news = get_news('apple')[0][0]
    amazon = get_news('amazon')[0][0]
    tesla = get_news('tesla')[0][0]
    facebook = get_news('facebook')[0][0]
    com = get_com()
    gold_price = com['Gold']
    silver_price = com['Silver']
    crude = com['Crude Oil']
    ng = com['Natural Gas']
    context = {
        "gold": gold_price,
        "silver": silver_price,
        "crude": crude,
        "ng": ng,
        "apple_news" : apple_news,
        "tesla": tesla,
        "facebook": facebook,
        "amazon_news": amazon,
        "news": news,
        'top_gainers': top_gainers[10:14],
        "top_losers": top_losers[10:14],
        "top_actives": top_actives[10:14],
    }

    return render(request, template_name='index.html', context=context)


def market_prediction(request, pk):
    obj = Company.objects.get(pk=pk)
    symbol = obj.symbol
    msg = get_preds(symbol)
    if msg == "Success":
        print("SUccess")
        url = "{% static 'mlFB.png' %}"
        return render(request, template_name='ml.html', context={
            #"symbol": symbol,
            "url":url,
        })
    else:
        pass



def news(request):
    news = News.objects.order_by('-timestamp')[3:7]
    trending = News.objects.order_by('-timestamp').first()
    #print(news)
    return render(request, template_name='latest_news.html', context = {
        "news":news,
        "trending": trending,
    })


def get_news(sub = None):
    if sub is not None:
        url = 'http://newsapi.org/v2/top-headlines?q=' + sub + '&apiKey=38b55515799f486cbd0c7b54d490a2d4'
        subject = sub
    else:
        url = 'http://newsapi.org/v2/top-headlines?q=stock&apiKey=38b55515799f486cbd0c7b54d490a2d4'
        subject = "stock"
    response = requests.get(url).json()
    title = []
    description = []
    img = []

    for i in range(len(response['articles'])):
        title.append(response['articles'][i]['title'])
        description.append(response['articles'][i]['description'])
        img.append(response['articles'][i]['urlToImage'])
    return title,description, img, subject




def index(request):
    news = News.objects.order_by('-timestamp')
    news_apple = get_news(sub='amazon')
    #print(news_apple)
    return render(request, template_name='index.html', context={
        "news": news,
        "news_apple": news_apple,
    })



