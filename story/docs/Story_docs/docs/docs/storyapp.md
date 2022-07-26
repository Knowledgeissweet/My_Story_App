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
  
>:info: This tutorial is written based on the lastest Django version at the time, which is version 4.0.6. For the purpose of this tutorial, I will advise you install this version.

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

## Defining Urls

Without our urls defined, we would not be able to access our web application from a browser. 

In preparation for the next step (creating objects), we would define our first url path to allow us create instances of our model classes from within the admin interface.

Navigate to your story app `urls.py` and modify it to reflect this:

```
<!-- story/urls.py -->
from django.contrib import admin
from django.urls import path

app_name = 'story'

urlpatterns = [
    path('admin/', admin.site.urls),
]
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

## Writing Views

With a couple instances of our models now stored in the database, we can the views. 

In this tutorial, we would only be writing function-based views.

In your `views.py`, we would create our first function-based view that allows us to display in a browser, a list of stories, alongside a search funtionality implemented to allows us search the list of stories by `title`, `des`, `body`, and `tags`.

Now, modify your `views.py` to reflect this:

```
<!-- story/views.py -->


from queue import Empty
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Category, Story

def story_list(request):
    query=None
    category=None
    stories=Story.objects.all()
    story= [] 
    if request.method=="GET":
        query= request.GET.get("search")
        if query:
            story=Story.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)| Q(des__icontains=query)|Q(tags__name__iregex=query)).distinct()

   
    return render(request, 'story/story_list.html', {
        'story': story,
        'category': category,
        'stories': stories,
        'query':query,
        })
```

## Creating Templates

If have not done so before, go ahead and create a templates directory in your story app. Then, create a sub-directory with the name, "story", in your templates directory.

!!! caution
    Make sure your templates directory's name is "templates". This is line with best practice when using Django for web applications. The Django engine knows automatically to look into your templates directory to discover your template files.

Having done that we would create a `base.html` template. This will hold `nav` and `footer` since we expect both to repeat across all pages on our website.

Create a `base.html` in your story sub-directory. Then modify it to reflect this:

```
<!-- templates/story/base.html -->

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title></title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        {% comment %} Bootstrap CSS {% endcomment %}
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
        {% block title %} <title>story book</title> {% endblock title %}
    </head>
    <body>
       {% comment %}As a heading  {% endcomment %}
        <nav class="navbar navbar-dark bg-dark">
            <a href="{% url 'story:story_list' %}"><span class="navbar-brand mb-0 h1">Story book</span></a>
        </nav>
        {% block body %}
        
        {% endblock body %}
        <foooter class="cs-footer mt-4 bg-dark pt-5 pt-md-6 pt-lg-7">
            <div class="container pt-3 pt-md-0">
                <div class="pb-md-4 text-center">
                    <h3 class="text-light font-weight-light mb-3">Do not read all story?</h3>
                    <h2 class="text-light mb-5">Read all story for your interest</h2>
                </div>
              </div>
        </footer>
        {% comment %} Optional Javascript {% endcomment %}
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        {% comment %} <script src="static/tiny.js"></script> {% endcomment %}
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
    
    </body>
</html>
```

Next, we would create the template file for our `story_list` function view we wrote earlier.

Go ahead and create a new template in the story sub-directory with the name, "story_list".

Now, modify it to reflect this:

```
<!-- templates/story/story_list.html -->

{% extends "story/base.html" %}

{% block title %}
<title>story book</title>
{% endblock title %}

{% block body %}
<div class="pricing-header px-3 py-3 pt-mt-5 pb-md-4 mx-auto text-center">
    <h1 class="display-4">Story book</h1>
    <p class="lead">you can find here some short stories</p>
    <form type="get" action="#">
        {% csrf_token %}
        <label>Location:-</label>
           <input id="search" type="text" name="search" placeholder="Search...">
           <button type="submit">Submit</button>
    </form>

    {% if query %}
    <h3>{% with story.count as total_results %}
        Found {{total_results}} results
        {% endwith %}
    </h3>
    {% for x in story %}
    <div class="mt-3">
        <li style="list-style: none;"><a href="{{x.get_absolute_url}} "><h3>{{x.title}} </h3></a></li>
        <p>{{x.des}} </p>
    </div>
    {% empty %}
    <h3>There is no query</h3>
    {% endfor %}
    {% else %}
    <div class="mt-3">
        <ul style="list-style: none;">
            {% for story in stories  %}
            <li><a href="{{story.get_absolute_url}}"><h3>{{story.title}}</h3> </a></li>
            <p>{{story.des}} </p>
            {% endfor %}
        </ul>
    </div>
    {% endif %}
</div>

{% endblock body %}
```
!!! info
    The `get_absolute_url` function in the template might trigger an error. That is because we have not defined the function yet. 
    
    Don't worry. We would get to it shortly.

The `story_list.html` template allows us to view and search the story list, but it doesn't allow us to view each story's details (story body).

To view each story's details, we would  create a new template with the name, "story_detail", in the story sub-directory.

Having done that, modify the template to reflect this:

```
<!-- templates/story/story_detail.html -->


{% extends "story/base.html" %}

{% block title %}
<title>{{story.title}} </title>
{% endblock title %}

{% block body %}
    <div class="container">
      <h2 class="text-center">{{story.title}} </h2><hr>
      <p class='lead'>{{story.body|safe}} </p>
    </div>
    <hr>
    <div class="container">
       <h2>YOU MAY ALSO LIKE:</h2>
       {% for x in like_story %}
       <a href="{{x.get_absolute_url}}"><h5>{{x.title}}</h5></a>
       {% endfor %}
       <br>
    </div>

    <h2>Similar Posts</h2>
    {% for post in similar_posts %}
    <p>
        <a href="{{post.get_absolute_url}} ">{{post.title}} </a>
    </p>
    {% empty %}
    There are no similar story yet.
    {% endfor %}
    
{% endblock body %}
```

## Modifying Views

We have a template for our story details. Consequently, we need to create a corresponding function view for it.

Now, modify your `views.py` to reflect this:

```

<!-- story/views.py -->

import random       <!--  new -->
from taggit.models import Tag   <!--new  -->
from taggit.managers import TaggableManager <!--new-  -->



def story_detail(request, id):
    story=get_object_or_404(Story, id=id)
    all_story=list(Story.objects.exclude(id=id))
    like_story=random.sample(all_story,3)

    # Tags
    posts=Story.objects.get(id=id)
    similar_posts=posts.tags.similar_objects()[:2]

    return render(request, 'story/story_detail.html', {'story': story, 'like_story':like_story, 'similar_posts': similar_posts,})
```

## Modifying Models

In the Story model, we would define a function that allows us to view the details of each story when we click each story in the story list.

In your `models.py`, modify your Story model to reflect this:

```
<!-- story/models.py -->

Class Story(models.Model):
    ...

    def get_absolute_url(self):
        return reverse("story:story_detail", args=[self.id,])
```

## Modifying Urls

Now, we must define the urls to allow us access our web application in a browser.

Navigate to your story app `urls.py` and modify it to include this:

```
<!-- story/urls.py -->

from . import views <!--new  -->

urlpatterns = [
      ...
    path('', views.story_list, name='story_list'),
    path('<int:id>/',views.story_detail, name='story_detail'),
]
```
The `views.story_list` allows us to view the story list using the `http://127.0.0.1:8000/story` path; `views.story_detail` allows us to view each story's details using the `http://127.0.0.1:8000/storyapp/<int:id>/` path.

With all that done, you should have a two page website up in your browser that allows you to view and search through a story list, then, view each story detail.

## Wrapping it Up

Congratulations, you've successfully created a simple Story app. If you run into any issues or error while following this tutorial, feel free to refer to the main code.

I hope this was able to whet your appetite on the possibilities with the Django framework and get your creative juices flowing.

Keep up the coding spirit!











 <!--  -->
