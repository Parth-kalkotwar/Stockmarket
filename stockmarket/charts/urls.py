from django.urls import path, include
from . import views

app_name = 'charts'

urlpatterns = [
    path('<int:pk>/', views.index, name='index'),
    path('<int:id>/api/data/<int:pk>/', views.jsondata, name='api'),
]
