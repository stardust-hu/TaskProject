# coding: utf8
from django.conf.urls import url

from .views import login, logout, show_person_task_list, modify_person_task, show_detail_post, modify_detail_post, upload_image

urlpatterns = [
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^personTaskList/', show_person_task_list, name='person_task_list'),
    url(r'^modifyPersonTask/', modify_person_task, name='modify_person_task'),
    url(r'^showDetailPost/', show_detail_post, name='show_detail_post'),
    url(r'^modifyDetailPost/', modify_detail_post, name='modify_detail_post'),
    url(r'^uploadImage/', upload_image, name='upload_image'),
]
