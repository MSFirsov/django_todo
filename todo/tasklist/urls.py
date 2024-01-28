from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('<int:cur_year>/<int:week_num>/', views.index, name='home_with_week'),
    path('create_task/<int:cur_year>/<int:week_num>/<slug:task_date>/', views.create_task, name='create_task'),
    path('delete_task/<int:cur_year>/<int:week_num>/<int:task_id>/', views.delete_task, name='delete_task'),
    path('is_completed_task/<int:cur_year>/<int:week_num>/<int:task_id>/',
         views.is_completed_task, name='is_completed_task'),

]
