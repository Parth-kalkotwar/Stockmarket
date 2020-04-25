import requests
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Commodity


def get_com():
    top_commodities = {}
    top_commodities['Gold'] = Commodity.objects.filter(name__contains='Gold').first().price
    top_commodities['Silver'] = Commodity.objects.filter(name__contains='Silver').first().price
    top_commodities['Crude Oil'] = Commodity.objects.filter(name__contains='Crude Oil').first().price
    top_commodities['Natural Gas'] = Commodity.objects.filter(name__contains='Natural Gas').first().price
    return top_commodities


def com_home(request):
    url = 'https://financialmodelingprep.com/api/v3/quotes/commodity'
    raw_data = requests.get(url).json()
    for i in range(len(raw_data)):
        name = raw_data[i]['name']
        if Commodity.objects.filter(name__contains = name):
            continue
        else:
            pass
        try:
            obj = Commodity.objects.get(name=name)
            obj.price = raw_data[i]['price']
            obj.change = raw_data[i]['change']
            obj.change_perc = raw_data[i]['changesPercentage']
            obj.low = raw_data[i]['dayLow']
            obj.high = raw_data[i]['dayHigh']
            obj.latestVolume = raw_data[i]['volume']
            obj.open = raw_data[i]['open']
            obj.previousClose = raw_data[i]['previousClose']
            obj.save()
        except ObjectDoesNotExist:
            obj = Commodity()
            obj.name = name
            obj.symbol = raw_data[i]['symbol']
            obj.price = raw_data[i]['price']
            obj.change = raw_data[i]['change']
            obj.change_perc = raw_data[i]['changesPercentage']
            obj.low = raw_data[i]['dayLow']
            obj.high = raw_data[i]['dayHigh']
            obj.latestVolume = raw_data[i]['volume']
            obj.open = raw_data[i]['open']
            obj.previousClose = raw_data[i]['previousClose']
            obj.save()
    top_changes = Commodity.objects.all().order_by('-change_perc')[:5]
    top_commodities = {}
    top_commodities['Gold'] = Commodity.objects.filter(name__contains='Gold').first()
    top_commodities['Silver'] = Commodity.objects.filter(name__contains='Silver').first()
    top_commodities['Crude Oil'] = Commodity.objects.filter(name__contains='Crude Oil').first()
    top_commodities['Natural Gas'] = Commodity.objects.filter(name__contains='Natural Gas').first()
    print(top_commodities)
    return render(request, template_name='com/home.html', context={"top_changes":top_changes,
                                                                   "top_commodities": top_commodities,
                                                                   })


def details(request,pk):
    commodity = Commodity.objects.get(pk = pk)
    return render(request, template_name='com_detail.html', context={"commodity": commodity})


def commoditylistview(request):
    query = request.GET.get("q", None)
    commodities = Commodity.objects.all()
    if query is not None:
        commodities = commodities.filter(Q(name__icontains=query) |
                                     Q(symbol__icontains=query) |
                                     Q(exchange__icontains=query)
                                     )
    return render(request, template_name='commodities.html', context={"commodities": commodities})





