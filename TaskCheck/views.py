# coding: utf8
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, Http404
from .models import PersonTask, Person, Tag, DetailPost, PersonTaskList, Picture

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
                context['task_checked_id'] = today_task_checked.id
                detail_post_id = DetailPost.objects.filter(person_task_id=today_task_checked.id)
                if len(detail_post_id) == 0:
                    context['detail_post_id'] = None
                else:
                    context['detail_post_id'] = detail_post_id[0].id
                context['is_solve'] = today_task_checked.is_solve
                context['create_date'] = today_task_checked.create_date
                context['last_modified_time'] = today_task_checked.last_modified_time
    else:
        date = request.POST['date']
        task = request.POST['task']
        today_task_checked = PersonTask.objects.filter(date=date, task__task=task, person__person__username=request.user.username)
        if len(today_task_checked) != 1:
            context['error'] = True
            context['error_message'] = 'len(today_task_checked_list) != 1, 请联系管理员'
        else:
            today_task_checked = today_task_checked[0]
            is_solve = request.POST['checked']
            if is_solve == 'ok':
                today_task_checked.is_solve = True
            elif is_solve == 'error':
                today_task_checked.is_solve = False
            else:
                today_task_checked.is_solve = None
            today_task_checked.save()
        return HttpResponseRedirect('/personTaskList/?date=%s&task=%s' % (date, task))
    return render(request, template_name="TaskCheck/modify_person_task.html", context=context)


def get_checked_list(task_checked_list):
    checked_list = dict()
    for task in task_checked_list:
        checked_list[task.task.task] = {
            'is_checked': task.is_solve,
            'person_task_id': task.id,
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
        if len(request.GET) == 0:
            date = time.strftime("%Y-%m-%d")
            context['date'] = date
        else:
            date = request.GET['date']
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
                    each_row = [None, None, None, None, None]
                    each_row[0] = each_task.task
                    each_row[1] = checked_list[each_task.task]['is_checked']
                    each_row[2] = each_task.describe
                    each_row[3] = checked_list[each_task.task]['person_task_id']
                    detail_post = DetailPost.objects.filter(person_task_id=each_row[3])
                    if len(detail_post) == 0:
                        each_row[4] = ''
                    else:
                        each_row[4] = detail_post[0].id
                    show_table.append(each_row)
                context['show_table'] = show_table
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
                each_row = [None, None, None, None, None]
                each_row[0] = each_task.task
                each_row[1] = checked_list[each_task.task]['is_checked']
                each_row[2] = each_task.describe
                each_row[3] = checked_list[each_task.task]['person_task_id']
                detail_post = DetailPost.objects.filter(person_task_id=each_row[3])
                if len(detail_post) == 0:
                    each_row[4] = ''
                else:
                    each_row[4] = detail_post[0].id
                show_table.append(each_row)
            context['show_table'] = show_table
    return render(request, template_name="TaskCheck/person_task_list.html", context=context)


def show_detail_post(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    if len(request.GET) != 0:
        detail_post_id = request.GET['detail_post_id']
        person_task_id = request.GET['person_task_id']
        person_task = PersonTask.objects.get(id=person_task_id)
        detail_post = DetailPost.objects.filter(person_task_id=person_task_id)
        if len(detail_post) == 0:
            return HttpResponseRedirect('/modifyDetailPost/?person_task_id=%s&detail_post_id=%s' % (person_task_id, detail_post_id))
        else:
            context = {
                'index': False,
                'error': False,
            }
            detail_post = detail_post[0]
            context['detail_post_id'] = detail_post.id
            context['person_task_id'] = detail_post.person_task.id
            context['title'] = detail_post.title
            context['create_date'] = detail_post.create_date
            context['person_task'] = person_task.task
            context['person_task_date'] = str(detail_post.create_date.date())
            context['create_person'] = detail_post.create_person
            context['last_modified_time'] = detail_post.last_modified_time
            context['is_solve'] = detail_post.is_solve
            context['solve_date'] = '' if detail_post.solve_date is None else detail_post.solve_date
            context['solve_person'] = detail_post.solve_person
            context['tag'] = detail_post.tag
            context['text'] = detail_post.text
            return render(request, template_name="TaskCheck/show_detail_post.html", context=context)
    else:
        raise Http404()


def modify_detail_post(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    context = {
        'index': False,
        'error': False,
    }
    if (request.method == 'GET') and (len(request.GET) != 0):
        detail_post_id = request.GET['detail_post_id']
        person_task_id = request.GET['person_task_id']
        if detail_post_id == 'None':
            person_task = PersonTask.objects.get(id=person_task_id)
            person_task.is_solve = False
            person_task.save()
            create_person = Person.objects.get(person__username=request.user.username)
            context['is_solve'] = False
            context['create_person'] = create_person
            person_list = list(map(lambda x: "%s - %s" % (x.person.username, x.person.first_name), Person.objects.filter(person__is_active=True)))
            context['person_list'] = person_list
            tag_list = list(map(lambda x: "%s" % x.tag, Tag.objects.filter(is_active=True)))
            context['tag_list'] = tag_list
            context['person_task_id'] = person_task_id
        else:
            detail_post = DetailPost.objects.filter(id=detail_post_id)
            if len(detail_post) != 1:
                context['error'] = True
                context['error_message'] = 'len(detail_post) != 1, 请联系管理员'
            else:
                detail_post = detail_post[0]
                context['id'] = detail_post.id
                context['title'] = detail_post.title
                context['create_date'] = detail_post.create_date
                context['create_person'] = detail_post.create_person
                context['last_modified_time'] = detail_post.last_modified_time
                context['is_solve'] = detail_post.is_solve
                context['solve_date'] = '' if detail_post.solve_date is None else detail_post.solve_date
                context['solve_person'] = str(detail_post.solve_person)
                person_list = list(map(lambda x: "%s - %s" % (x.person.username, x.person.first_name), Person.objects.filter(person__is_active=True)))
                context['person_list'] = person_list
                context['tag'] = str(detail_post.tag)
                tag_list = list(map(lambda x: "%s" % x.tag, Tag.objects.filter(is_active=True)))
                context['tag_list'] = tag_list
                context['person_task_id'] = detail_post.person_task.id
                context['text'] = detail_post.text
    elif (request.method == 'POST') and (len(request.GET) != 0):
        post_id = request.GET['detail_post_id']
        person_task_id = request.GET['person_task_id']
        if post_id == 'None':
            detail_post = DetailPost()
            detail_post.person_task = PersonTask.objects.get(id=person_task_id)
            detail_post.title = request.POST['title']
            create_person = Person.objects.get(person__username=request.user.username)
            detail_post.create_person = create_person
            is_solve = request.POST['is_solve']
            detail_post.is_solve = True if is_solve == 'ok' else False
            solve_date = request.POST['solve_date']
            if '-' in solve_date:
                detail_post.solve_date = solve_date
            elif '' == solve_date:
                detail_post.solve_date = None
            solve_person = request.POST['solve_person'].split(' - ')[0]
            detail_post.solve_person = Person.objects.get(person__username=solve_person)
            tag = request.POST['tag']
            detail_post.tag = Tag.objects.get(tag=tag)
            detail_post.text = request.POST['text']
            detail_post.save()

            if detail_post.is_solve is True:
                detail_post.person_task.is_solve = True
            else:
                detail_post.person_task.is_solve = False
            detail_post.person_task.save()
            return HttpResponseRedirect('/showDetailPost/?person_task_id=%d&detail_post_id=%d' % (detail_post.person_task.id, detail_post.id))
        else:
            detail_post = DetailPost.objects.filter(id=post_id)
            if len(detail_post) != 1:
                context['error'] = True
                context['error_message'] = 'len(detail_post) != 1, 请联系管理员'
            else:
                detail_post = detail_post[0]
                detail_post.title = request.POST['title']
                create_person = Person.objects.get(person__username=request.user.username)
                detail_post.create_person = create_person
                is_solve = request.POST['is_solve']
                detail_post.is_solve = True if is_solve == 'ok' else False
                solve_date = request.POST['solve_date']
                if '-' in solve_date:
                    detail_post.solve_date = solve_date
                elif '' == solve_date:
                    detail_post.solve_date = None
                solve_person = request.POST['solve_person'].split(' - ')[0]
                detail_post.solve_person = Person.objects.get(person__username=solve_person)
                tag = request.POST['tag']
                detail_post.tag = Tag.objects.get(tag=tag)
                detail_post.text = request.POST['text']
                detail_post.save()
                if detail_post.is_solve is True:
                    detail_post.person_task.is_solve = True
                else:
                    detail_post.person_task.is_solve = False
                detail_post.person_task.save()
                return HttpResponseRedirect('/showDetailPost/?person_task_id=%d&detail_post_id=%d' % (detail_post.person_task.id, detail_post.id))
    else:
        raise Http404()
    return render(request, template_name="TaskCheck/modify_detail_post.html", context=context)


@csrf_exempt
def image_upload(request):
    if request.method == 'POST':
        if 'upload' in request.POST:
            return HttpResponse('上传出错')

        if 'upload' in request.FILES:
            image = request.FILES["upload"]
            image.name = request.user.username + '_' + image.name
            picture = Picture(uploader=request.user, image=image)
            picture.save()
            if 'responseType=json' in request.path:
                res = '{"uploaded": 1,"fileName": "%s","url": "%s"}' % (image.name, picture.image.url)
            else:
                callback = request.GET.get('CKEditorFuncNum')
                res = "<script>window.parent.CKEDITOR.tools.callFunction(" + callback + ",'" + picture.image.url + "', '');</script>"
            return HttpResponse(res)
    else:
        raise Http404()
