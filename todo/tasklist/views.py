import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView

from .forms import CreateTaskForm
from .models import Task


day_today = datetime.date.today().strftime('%A, %d %B %Y')
iso_date = datetime.date.today().isocalendar()


@login_required
def index(request, week_num=iso_date[1]):

    day_list = [
        datetime.date.fromisocalendar(iso_date[0], int(week_num), 1),
        datetime.date.fromisocalendar(iso_date[0], int(week_num), 2),
        datetime.date.fromisocalendar(iso_date[0], int(week_num), 3),
        datetime.date.fromisocalendar(iso_date[0], int(week_num), 4),
        datetime.date.fromisocalendar(iso_date[0], int(week_num), 5),
        datetime.date.fromisocalendar(iso_date[0], int(week_num), 6),
        datetime.date.fromisocalendar(iso_date[0], int(week_num), 7)
    ]

    task_list = Task.objects.filter(user_id=request.user).all()

    data = {
        'title': 'Главная страница',
        'day_list': day_list,
        'task_list': task_list,
        'week_num': week_num,
        'day_today': day_today,

    }
    return render(request, 'tasklist/index.html', context=data)


@login_required
def create_task(request, week_num, task_date):
    if request.method == 'POST':
        new_post = dict(**request.POST)
        new_post['task_date'] = datetime.datetime.strptime(task_date, '%Y-%m-%d').date()
        new_post['user'] = request.user.id
        new_post['text'] = new_post['text'][0]
        new_post['csrfmiddlewaretoken'] = new_post['csrfmiddlewaretoken'][0]
        form = CreateTaskForm(new_post)
        if form.is_valid():
            # print(request.POST)
            # print(new_post)
            form.save()
            return redirect('home_with_week', week_num=week_num)
    else:
        form = CreateTaskForm()

    data = {
        'title': 'Создание задания',
        'week_num': week_num,
        'task_date': task_date,
        'form': form,
    }
    return render(request, 'tasklist/create_task.html', context=data)


@login_required
def delete_task(request, week_num, task_id):
    task = Task.objects.get(pk=task_id)
    if task is None:
        pass

    task.delete()
    return redirect('home_with_week', week_num=week_num)


def is_completed_task(request, week_num, task_id):
    task = Task.objects.get(pk=task_id)
    if task.is_completed == 0:
        task.is_completed = 1
    else:
        task.is_completed = 0
    task.save()
    return redirect('home_with_week', week_num=week_num)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена</h1>')






