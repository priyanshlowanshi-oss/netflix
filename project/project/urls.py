"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.firstpage, name='firstpage'),
    path('superadmin/', views.superadmin, name='superadmin'),
    path('adlogin/', views.adlogin, name='adlogin'),
    path('delete_employee/<int:emp_id>/', views.delete_employee, name='delete_employee'),
    path('aadmin/', views.aadmin, name='aadmin'),
    path('movies_delete/<int:movie_id>/', views.movies_delete, name='movies_delete'),


    path('user/', views.user, name='user'),
    path('base/', views.base, name='base'),
    path('login/', views.login, name='login'),
    path('otp/',views.otp, name='otp'),
    path('notification/',views.notification, name='notification'),


    path('mylist/add/<int:movie_id>/', views.add_to_mylist, name='add_to_mylist'),

    path('reset/', views.reset, name='reset'),

    path('nlogo/', views.nlogo, name='nlogo'),

    path('Subscription/', views.Subscription, name='Subscription'),
    path("movie/<int:movie_id>/", views.movie_details, name="movie_details"),


    path('profile/', views.profile, name='profile'),
    
    path('nav/', views.nav, name='nav'),
    path('tvshows/', views.tvshows, name='tvshows'),
    path('movies/', views.movies, name='movies'),
    path('help/', views.help, name='help'),
    path('setting/', views.setting, name='setting'),
    path('history/', views.history, name='history'),



    path("search/", views.search_movies, name="search_movies"),



    path('newpopular/', views.newpopular, name='newpopular'),
    path('mylist/', views.mylist, name='mylist'),
    path('browselanguage/', views.browselanguage, name='browselanguage'),
    path("movie/<int:movie_id>/",views.movie_details, name="movie_details"),



]
