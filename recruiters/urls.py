from django.urls import path,include
from . import views

app_name = 'recruiters'

urlpatterns = [
    path('', views.Home,name='home'),
    path('profile/',views.Profile,name='profile'),
    path('create-job/',views.CreateJob,name='create-job'),
    path('create-user/',views.CreateUser,name='create-user'),
    path('applications/',views.Applications,name='applications'),
    path('jobs/',views.Jobs,name='jobs'),
    path('users/',views.Users,name='users'),
    path('employee-life-cycle/',views.EmployeeLifeCycle,name='employee-life-cycle'),
]
