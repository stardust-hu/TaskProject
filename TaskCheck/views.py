from django.shortcuts import render
from django.http import HttpResponse
from .models import PersonTask, Person, Tag, Task, DetailPost, PersonTaskList
from .forms import AddPersonTask


def login(request):
    return render(request, template_name="TaskCheck/login.html")


def index(request):
    user = request.user
    if not user.is_authenticated():
        user = '游客'
    if request.method == 'POST':
        form = AddPersonTask(request.POST)
    else:
        form = AddPersonTask()
    return render(request, template_name="TaskCheck/index.html", context={'user': user, 'form': form})


def get_checked_list(task_checked_list):
    checked_list = dict()
    for task in task_checked_list:
        checked_list[task.task.task] = {
            'is_checked': task.is_solve,
            'url': task.url,
        }
    return checked_list


def show_person_task_list(request):
    context = {'date': '2017-03-17'}
    if request.method == 'POST':
        date = request.POST['date']
        today_total_task_list = PersonTaskList.objects.filter(date=date, person__person__username=request.user.username)
        today_task_checked_list = PersonTask.objects.filter(date=date, person__person__username=request.user.username)
        checked_list = get_checked_list(today_task_checked_list)
        if len(today_total_task_list) != 1:
            print('错误，请联系管理员')
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
    else:
        pass
    return render(request, template_name="TaskCheck/person_task_list.html", context=context)
