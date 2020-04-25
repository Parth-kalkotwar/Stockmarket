from django.urls import path, include
from . import views

app_name = 'nandc'

urlpatterns = [
    path('home/', views.com_home, name='home'),
    path('list/', views.commoditylistview, name='list'),
    path('<int:pk>/', views.details, name='details'),
]
