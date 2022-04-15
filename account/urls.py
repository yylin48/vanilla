from django.urls import path, re_path
from account import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [

    path('', views.index, name='index'),

]
urlpatterns = format_suffix_patterns(urlpatterns)


