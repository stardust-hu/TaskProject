from django.contrib import admin
from .models import Person, Task, PersonTask, DetailPost, Tag, PersonTaskList, User


class DetailPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'create_date', 'create_person', 'last_modified_time', 'is_solve', 'solve_date', 'solve_person', 'tag')


class PersonTaskListAdmin(admin.ModelAdmin):
    list_display = ('person', 'date', 'create_date', 'last_modified_time')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active', 'create_date', 'get_date_joined', 'get_last_login')

    def is_active(self, obj):
        return obj.person.is_active

    is_active.short_description = '活动？'

    def get_date_joined(self, obj):
        return obj.person.date_joined

    get_date_joined.short_description = '加入日期'

    def get_last_login(self, obj):
        return obj.person.last_login

    get_last_login.short_description = '最后登录时间'


class PersonTaskAdmin(admin.ModelAdmin):
    list_display = ('date', 'person', 'task', 'is_solve', 'create_date', 'last_modified_time')


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'is_active', 'create_date', 'last_modified_time', 'describe')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'is_active', 'create_date', 'last_modified_time', 'describe')


admin.site.register(Person, PersonAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(PersonTaskList, PersonTaskListAdmin)
admin.site.register(PersonTask, PersonTaskAdmin)
admin.site.register(DetailPost, DetailPostAdmin)
