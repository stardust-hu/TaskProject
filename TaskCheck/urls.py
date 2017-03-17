# coding: utf8
from django.conf.urls import url

from .views import index, show_person_task_list

urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^PersonTaskList/', show_person_task_list, name='person_task_list'),
]
