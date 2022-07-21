# Creating a Django Story App

In this tutorial, you learn to create a simple story app that allows you the following functionalities:

1. A public site that allows you to search stories, and view them by their categories, tags, and slug.
2. An admin site that lets you add, change, and delete stories, categories and tags.

## Prerequisites & Installations

### Prerequisites

This tutorial is for beginners to the Django framework—although not for absolute beginners. If this is your first attempt at Django, I will strongly recommend perusing first [the Django tutorial](https://docs.djangoproject.com/en/4.0/intro/tutorial01/) as it is more detailed. It will help you get familiar with the framework before you try out your hand on other fun/practice projects.

The following prerequites are also required:

   1. Comfortable using the command line

   2. Installation of Python3, preferably version 3.8 and above.

   3. An understanding of the OOP(Object-oriented programming) paradigm.

### Setting Up your Development Workstation

In this tutorial, we would be setting up our Django project in a virtual environment—inline with best practices.

Navigate to your working directory—using command line/powershell—on your local machine and carry out the following instructions.

1. Create a new virtual environment

2. Enter the virtual environment

3. Activate the virtual environment

 It should appear similar to this in your command line:

```
.../> virtualenv <name>  <!--name: storybook  -->
.../> cd <name>
.../<name>/> scripts/activate
```

Now, install the following:

- [Django](https://docs.djangoproject.com/en/4.0/intro/install/)
- [Django-taggit](https://django-taggit.readthedocs.io/en/latest/getting_started.html)
  
!!! info
    This tutorial is written based on the lastest Django version at the time, which is version 4.0.6. For the purpose of this tutorial, I will advise you install this version.

!!! caution
    Ensure your virtual environment is activated when installing Django-taggit. Failure to do so might trigger a `ModuleNotFoundError: No module named 'taggit'` when making migrations later on in the project.

With out development environment set up, let's create our django project.

## Creating a Project

If you have done [the django tutorial](https://docs.djangoproject.com/en/4.0/intro/tutorial01/), you should be familiar with initiating a new django project.

```
django-admin startproject <name> <!-- name: story -->
```

The command should create this directory structure:

```
storybook     <!--name of the project created (outer directory)-->
    │   manage.py
    │   
    └───storybook     <!-- inner directory --> 
            asgi.py
            settings.py
            urls.py
            wsgi.py
            __init__.py
```

!!! info
    You can run the `python manage.py runserver` to confirm your project is well set-up. The development server should run in your browser. You should see a rocket shooting flames downward about to take off, and a bold message: The install worked successfully! Congratulations!

## Creating an App

Next, create an app in your Django project. It should be in the outer directory, on the same level with the inner directory.

```
django-admin startapp <name>
```

The command should create this directory structure:

```
story
    │   admin.py
    │   apps.py
    │   models.py
    │   tests.py
    │   views.py
    │   __init__.py
    │   
    └───migrations
            __init__.py
```

With that done, we would update `INSTALLED_APPS` within our `settings.py` to notify Django about our newly created app.

!!! Info
    Recall we installed Django-taggit at the beginning of the tutorial? We need the plugin for creating and managing our story tags. Alongside your app, add `taggit` to `INSTALLED_APPS`.

```
 <!--storybook/settings.py  -->
 INSTALLED_APPS = [
    ...
    "story.apps.StoryappConfig",
    "taggit",
 ]
```

Next up, we would add our app to the `urls.py` in our project directory. To do that, first, we would create a `urls.py` file in our app. Next, we navigate to our project urls file and modify it to reflect this:

```
<!-- storybook/urls.py -->
from django.contrib import admin
from django.urls import path, include  <!-- new  -->
from argparse import Namespace   <!-- new -->


urlpatterns = [
    path('admin/', admin.site.urls),
    path('story/', include(('story.urls', 'story'), namespace='story')), <!-- new -->
]
```

Having done that, now we can run our first migrations. These commands creates a database for our project. For convenience, we would be using the default database (Sqlite) Django have provided us.

```
.../> python manage.py makemigrations
.../> python manage.py migrate
```

!!! note
    When working on your own, you can decide to modify your url files much later on after making migrations or even after you've created some models and views. The order doesn't matter.

## Creating Models

Our app will have two models: `Category` and `Story`. `Category` will have two fields: `name` and `slug`. `Story` will have five fields: `category`, `title`, `des`, `body` and `tag`.

Finally, we would add a `Meta` class and a `__str__` function to each of the models.

Modify your app's `models.py` to reflect this:

```
<!-- story/models.py -->

from django.db import models
from django.urls import reverse 
from taggit.managers import TaggableManager

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=150, db_index=True,)
    slug=models.SlugField(unique=True)
    class Meta:
        ordering= ('-name',)

    def __str__(self):
        return self.name

class Story(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    body=models.TextField()
    des=models.TextField()
    publish=models.DateTimeField(auto_now_add=True)
    tags=TaggableManager()

    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title
```
Now, we must run migrations again to create database tables for our models.

Having done that, we would modify our app's `admin.py` to enable us create, modify and delete instances of our model classes from the admin.

First, we would import models into our app's `admin.py`.Then, we would add `ModelAdmin` classes to register our models in the admin. In this tutorial, we would also use [register decorators](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#the-register-decorator) on each of the `ModelAdmin` classes.

Modify your app's `admin.py` to reflect this:

```
<!-- story/admin.py -->
from django.contrib import admin
from .models import Category, Story

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display=['title','publish']
    search_fields=['title',]
```

!!! note
    You won't be able to view your admin if haven't created your user yet. To create a user, run this command in your command line:`python manage.py createsuperuser`.

    Thereafter, you should be able to login from your local domain using this url: `http://127.0.0.1:8000/admin/`.

    You should be able to see your Story app, alongside the models, displayed on the admin page on login.

## Creating Objects

At this point, you should be able to create instances of your models from within your admin. 

<figure markdown align="center">
  ![Creating categories](img/Screenshot%20(72).png)
  <figcaption><i>Creating categories</i></figcaption>
</figure>

<figure markdown align="center">
  ![Creating categories](img/Screenshot%20(74).png)
  <figcaption><i>Creating stories</i></figcaption>
</figure>

Go ahead and create instances of your model classes. The data from this exercise will come handy when writing our views.


 <!--  -->