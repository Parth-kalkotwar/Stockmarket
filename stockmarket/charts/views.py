import requests
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from core.models import Company


def index(request, pk):
    obj = get_symbol(pk)
    return render(request, template_name='charts.html', context={
        "pk": pk,
        "obj":obj,
    })


def get_symbol(pk):
    obj = Company.objects.get(pk=pk)
    return obj


def jsondata(request, id, pk):
    qs_count = User.objects.all().count()
    obj = get_symbol(pk)
    url = 'https://financialmodelingprep.com/api/v3/historical-chart/1hour/' + str(obj.symbol)
    raw_data = requests.get(url).json()
    labels = []
    default_items = []
    for i in range(len(raw_data)):
        labels.append(raw_data[i]["date"])
        default_items.append(raw_data[i]["high"])
    data = {
        "labels": labels,
        "default": default_items,
    }
    return JsonResponse(data)



"""
class ChartsAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None, **kwargs):
        qs_count = User.objects.all().count()
        symbol = get_symbol(pk)
        print(symbol)
        url = 'https://financialmodelingprep.com/api/v3/historical-chart/1hour/AAPL'
        raw_data = requests.get(url).json()
        labels = []
        default_items = []
        for i in range(len(raw_data)):
            labels.append(raw_data[i]["date"])
            default_items.append(raw_data[i]["high"])
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)
"""