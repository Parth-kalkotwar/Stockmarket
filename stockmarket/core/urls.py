from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('home/', views.homepage, name='home'),
    path('', views.index, name='index'),
    path('companies/', views.listview, name='list'),
    path('news/', views.news, name='news'),
    path('companies/<int:pk>/', views.companydetails, name='details'),
    path('companies/<int:pk>/prediction', views.market_prediction, name='prediction'),
]
