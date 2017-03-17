from django.shortcuts import render
from django.http import HttpResponse
from .models import PersonTask, Person, Tag, Task, DetailPost, PersonTaskList
from .forms import AddPersonTask


def index(request):
    user = request.user
    if not user.is_authenticated():
        user = '游客'
    if request.method == 'POST':
        form = AddPersonTask(request.POST)
    else:
        form = AddPersonTask()
    return render(request, template_name="TaskCheck/index.html", context={'user': user, 'form': form})


def show_person_task_list(request):
    context = {'date': '2017-03-17'}
    if request.method == 'POST':
        date = request.POST['date']
        today_total_task_list = PersonTaskList.objects.filter(date=date, person__person__username=request.user.username)
        today_task_checked_list = PersonTask.objects.filter(date=date, person__person__username=request.user.username)
        print(today_task_checked_list)
        if len(today_total_task_list) > 1:
            print('错误，请联系管理员')
        else:
            today_total_task_list = today_total_task_list[0]
            print(today_total_task_list.date, today_total_task_list.person)
            total_task = today_total_task_list.task.all()
            for each_task in total_task:
                print(each_task.task, each_task.describe)
    else:
        pass
    return render(request, template_name="TaskCheck/person_task_list.html", context=context)
