import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from .forms import CreateTaskForm
from .models import Task


day_today = datetime.date.today().strftime('%A, %d %B %Y')
iso_date = datetime.date.today().isocalendar()


@login_required
def index(request, cur_year=iso_date[0], week_num=iso_date[1]):
    if week_num >= 53:
        cur_year += 1
        week_num = 1
    elif week_num <= 0:
        cur_year -= 1
        week_num = 52

    day_list = [datetime.date.fromisocalendar(cur_year, int(week_num), x) for x in range(1, 8)]

    task_list = Task.objects.filter(user_id=request.user).all()

    data = {
        'title': 'Главная страница',
        'day_list': day_list,
        'task_list': task_list,
        'week_num': week_num,
        'day_today': day_today,
        'cur_year': cur_year,

    }
    return render(request, 'tasklist/index.html', context=data)


@login_required
def create_task(request, cur_year, week_num, task_date):
    if request.method == 'POST':
        new_post = dict(**request.POST)
        new_post['task_date'] = datetime.datetime.strptime(task_date, '%Y-%m-%d').date()
        new_post['user'] = request.user.id
        new_post['text'] = new_post['text'][0]
        form = CreateTaskForm(new_post)
        if form.is_valid():
            form.save()
            return redirect('home_with_week', cur_year=cur_year, week_num=week_num)
    else:
        form = CreateTaskForm()

    data = {
        'title': 'Создание задания',
        'week_num': week_num,
        'task_date': task_date,
        'form': form,
        'cur_year': cur_year,

    }
    return render(request, 'tasklist/create_task.html', context=data)


@login_required
def delete_task(request, cur_year, week_num, task_id):
    task = Task.objects.get(pk=task_id)
    if task is None:
        pass

    task.delete()
    return redirect('home_with_week', cur_year=cur_year, week_num=week_num)


def is_completed_task(request, cur_year, week_num, task_id):
    task = Task.objects.get(pk=task_id)
    if task.is_completed == 0:
        task.is_completed = 1
    else:
        task.is_completed = 0
    task.save()
    return redirect('home_with_week', cur_year=cur_year, week_num=week_num)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена</h1>')






