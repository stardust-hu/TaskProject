from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    person = models.OneToOneField(verbose_name='用户名', to=User, primary_key=True)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.person.username, self.person.first_name)


class Task(models.Model):
    task = models.CharField(verbose_name='任务名称', max_length=120)
    is_active = models.BooleanField(verbose_name='活动？', default=True)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    describe = models.TextField(verbose_name='描述', null=True, blank=True)

    def __str__(self):
        return self.task


class PersonTaskList(models.Model):
    person = models.ForeignKey(verbose_name='姓名', to=Person)
    date = models.DateField(verbose_name='日期')
    task = models.ManyToManyField(verbose_name='任务', to=Task)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    def __str__(self):
        return self.person.person.username


class PersonTask(models.Model):
    date = models.DateField(verbose_name='日期')
    person = models.ForeignKey(verbose_name='姓名', to=Person)
    task = models.ForeignKey(verbose_name='任务', to=Task)
    is_solve = models.NullBooleanField(verbose_name='检查?', default=None)  # 为什么改不了变量名？/(ㄒoㄒ)/~~
    url = models.URLField(verbose_name='详细链接', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    def __str__(self):
        return str(self.id)


class Tag(models.Model):
    tag = models.CharField(verbose_name='标签', max_length=120)
    is_active = models.BooleanField(verbose_name='活动？', default=True)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    describe = models.TextField(verbose_name='描述', null=True, blank=True)

    def __str__(self):
        return self.tag


class DetailPost(models.Model):
    title = models.CharField(verbose_name='标题', max_length=120)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    create_person = models.ForeignKey(verbose_name='创建人', to=Person, related_name='person_create')
    last_modified_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    is_solve = models.BooleanField(verbose_name='处理?', default=False)
    solve_date = models.DateField(verbose_name='处理日期', null=True, blank=True)
    solve_person = models.ForeignKey(verbose_name='处理人', to=Person, null=True, blank=True, related_name='person_solve')
    tag = models.ForeignKey(verbose_name='标签', to=Tag)
    text = models.TextField(verbose_name='正文', null=True, blank=True)

    def __str__(self):
        return str(self.id)
