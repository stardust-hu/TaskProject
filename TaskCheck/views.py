# coding: utf8
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, Http404
from .models import PersonTask, Person, Tag, Task, DetailPost, PersonTaskList
from .forms import AddPersonTask

from django.contrib import auth

import time


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/logout')
        else:
            return render(request, template_name="TaskCheck/login.html")
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if (user is not None) and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/personTaskList')
        else:
            return render(request, template_name="TaskCheck/login.html", context={})


def logout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    elif request.method == 'GET':
        return render(request, template_name="TaskCheck/logout.html")
    elif request.POST['logout'] == 'true':
        auth.logout(request)
        return HttpResponseRedirect('/login')
    else:
        return render(request, template_name="TaskCheck/logout.html")


def index(request):
    user = request.user
    if not user.is_authenticated():
        user = '游客'
    if request.method == 'POST':
        form = AddPersonTask(request.POST)
    else:
        form = AddPersonTask()
    return render(request, template_name="TaskCheck/index.html", context={'user': user, 'form': form})


def modify_person_task(request):
    context = {}
    if request.method == 'GET':
        if len(request.GET) == 0:
            return HttpResponseRedirect('/login')
        else:
            date = request.GET['date']
            task = request.GET['task']
            today_task_checked = PersonTask.objects.filter(date=date, task__task=task, person__person__username=request.user.username)
            if len(today_task_checked) != 1:
                context['error'] = True
                context['error_message'] = 'len(today_task_checked_list) != 1, 请联系管理员'
            else:
                today_task_checked = today_task_checked[0]
                context['task'] = task
                context['date'] = date
                context['is_solve'] = today_task_checked.is_solve
                context['url'] = today_task_checked.url
                context['create_date'] = today_task_checked.create_date
                context['last_modified_time'] = today_task_checked.last_modified_time
    else:
        date = request.POST['date']
        task = request.POST['task']
        checked = request.POST['checked']
        # url = request.POST['url']
        return HttpResponseRedirect('/modifyPersonTask/?date=%s&task=%s' % (date, task))
    return render(request, template_name="TaskCheck/modify_person_task.html", context=context)


def get_checked_list(task_checked_list):
    checked_list = dict()
    for task in task_checked_list:
        checked_list[task.task.task] = {
            'is_checked': task.is_solve,
            'url': task.url,
        }
    return checked_list


def show_person_task_list(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    context = {
        'index': False,
        'error': False,
    }
    if request.method != 'POST':
        date = time.strftime("%Y-%m-%d")
        context['date'] = date
    elif 'modify' in request.POST.keys():
        date = request.POST['date']
        task = request.POST['task']
        return HttpResponseRedirect('/modifyPersonTask/?date=%s&task=%s' % (date, task))
    else:
        date = request.POST['date']
        context['date'] = date
        today_total_task_list = PersonTaskList.objects.filter(date=date, person__person__username=request.user.username)
        today_task_checked_list = PersonTask.objects.filter(date=date, person__person__username=request.user.username)
        checked_list = get_checked_list(today_task_checked_list)
        if len(today_total_task_list) != 1:
            context['error'] = True
            context['error_message'] = 'len(today_total_task_list) != 1, 请联系管理员'
        else:
            show_table = []
            today_total_task_list = today_total_task_list[0]
            total_task = today_total_task_list.task.all()
            for each_task in total_task:
                each_row = [None, None, None, None]
                each_row[0] = each_task.task
                each_row[1] = checked_list[each_task.task]['is_checked']
                each_row[2] = checked_list[each_task.task]['url']
                each_row[3] = each_task.describe
                show_table.append(each_row)
            context['show_table'] = show_table
    return render(request, template_name="TaskCheck/person_task_list.html", context=context)


@csrf_exempt
def upload_image(request):
    print(request.GET)
    print(request.POST)
    if request.method == 'POST':
        callback = request.GET.get('CKEditorFuncNum')
        try:
            path = "media/uploads/" + time.strftime("%Y/%m/", time.localtime())
            # 这里path修改你要上传的路径, 这样就上传到了media/upload/下对应年月的文件夹
            f = request.FILES["upload"]
            file_name = path + f.name
            des_origin_f = open(file_name, "wb+")
            for chunk in f:
                des_origin_f.write(chunk)
            des_origin_f.close()
        except Exception as e:
            print(e)
        res = r"<script>window.parent.CKEDITOR.tools.callFunction(" + callback + ",'/" + file_name + "', '');</script>"
        return HttpResponse(res)
    else:
        raise Http404()


def modify_detail_post(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    context = {}
    detail_post = DetailPost.objects.all()[0]
    context['id'] = detail_post.id
    context['title'] = detail_post.title
    context['create_date'] = detail_post.create_date
    context['create_person'] = detail_post.create_person
    context['last_modified_time'] = detail_post.last_modified_time
    context['is_solve'] = detail_post.is_solve
    context['solve_date'] = detail_post.solve_date
    context['solve_person'] = detail_post.solve_person
    context['tag'] = detail_post.tag
    context['text'] = detail_post.text
    print(request.POST)
    return render(request, template_name="TaskCheck/modify_detail_post.html", context=context)
