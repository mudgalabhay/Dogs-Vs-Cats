from django.urls import path, include
from .import views

app_name = 'main'

urlpatterns = [

    path('', views.homepage, name="homepage"),

    path('predict', views.upload_predict, name='predict'),

]