"""
URL configuration for mywebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp.views import home
from myapp import views
from django.contrib.auth import views as auth_views
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('', include('myapp.urls')),
    path('pets/', views.pets, name='pets'),
    path('buy-pet/', views.buy_pet, name='buy_pet'),
    path('select-pet/', views.select_pet, name='select_pet'),  # Add this line
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.task_list, name='task_list'),
    path('exercises/', views.exercise_list, name='exercise_list'),
    path('stretching/', views.stretching_list, name='stretching_list'),
    path('cardio/', views.cardio_list, name='cardio_list'),
    path('get-tips/', views.get_tips, name='get_tips'),  # New endpoint for fetching tips
    path('<str:category>/', views.category_task_list, name='category_task_list'),
    path('<str:category>/add/', views.add_task, name='add_task'),
    path('<str:category>/complete/<int:task_id>/', views.mark_task_complete, name='mark_task_complete'),
]
