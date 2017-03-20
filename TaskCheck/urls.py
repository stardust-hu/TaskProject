# coding: utf8
from django.conf.urls import url

from .views import login, logout, index, show_person_task_list, modify_person_task, modify_detail_post, upload_image

urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^personTaskList/', show_person_task_list, name='person_task_list'),
    url(r'^modifyPersonTask/', modify_person_task, name='modify_person_task'),
    url(r'^modifyDetailPost/', modify_detail_post, name='modify_detail_post'),
    url(r'^uploadImage/', upload_image, name='upload_image'),
]
