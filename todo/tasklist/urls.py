from django.urls import path, re_path, register_converter
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('<int:week_num>/', views.index, name='home_with_week'),
    path('create_task/<int:week_num>/<slug:task_date>/', views.create_task, name='create_task'),
    path('delete_task/<int:week_num>/<int:task_id>/', views.delete_task, name='delete_task'),
    path('is_completed_task/<int:week_num>/<int:task_id>/', views.is_completed_task, name='is_completed_task'),

]
