"""Storybook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from . import views 

app_name = 'story'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.story_list, name='story_list'),
    path('<slug:category_slug>', views.story_list, name='story_category'),
    path('<int:id>/',views.story_detail, name='story_detail'),
    path('search/', views.search_story, name="story_search"),
    path('tag/<slug:tag_slug>', views.story_list, name="story_by_tag")
]
