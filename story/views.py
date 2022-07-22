from queue import Empty
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import random
from taggit.models import Tag
from django.db.models import Count
from django.db.models import Q
from taggit.managers import TaggableManager


# Create your views here.

from .models import Category, Story

def story_list(request, category_slug=None):
    query_id=None
    query=None
    category=None
    # categories=Category.objects.all()
    stories=Story.objects.all()
    story= [] 
    if request.method=="GET":
        query= request.GET.get("search") #another contribution
        if query:
            story=Story.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)| Q(des__icontains=query)|Q(tags__name__iregex=query)).distinct()

   
    return render(request, 'story/story_list.html', {
        # 'categories': categories,
        'story': story,
        'category': category,
        'stories': stories,
        'query':query,
        # 'page':page,
        # 'recent_story':recent_story
        # 'tag':tag,
        })


def story_detail(request, id):
    story=get_object_or_404(Story, id=id)
    all_story=list(Story.objects.exclude(id=id))
    like_story=random.sample(all_story,3)

    # Tags
    posts=Story.objects.get(id=id)
    similar_posts=posts.tags.similar_objects()[:2]
    

    return render(request, 'story/story_detail.html', {'story': story, 'like_story':like_story, 'similar_posts': similar_posts,})







    # contributed a context variable, "similar_posts":similar_posts.

# def search_story(request):
#     query=None
#     results=[]
#     if request.method =="GET":
#         query=request.GET.get("search")
#         if query:
#             results=Story.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)| Q(des__icontains=query))
#     return render(request, 'story/search.html', {'query':query,'results':results,})





# post_tags_ids=Story.tags.values_list('id', flat=True)
    # # similar_posts=Story.objects.filter(tags__in=post_tags_ids).exclude(id=story.id)
    # similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:3]


# new contribution nested if query.
    





# paginator=Paginator(story,5)
    # page=request.GET.get('page')
    # tag=None
    # try:
    #     story=paginator.page(page)
    # except PageNotAnInteger:
    #     story=paginator.page(1)
    # except EmptyPage:
    #     story=paginator.page(paginator.num_pages)
    # if category_slug:
    #     story=Story.objects.all()
    #     category=get_object_or_404(Category,slug=category_slug)
    #     story=story.filter(category=category)
    #     paginator=Paginator(story,3)
    #     page=request.GET.get('page')
    #     try:
    #         story=paginator.page(page)
    #     except PageNotAnInteger:
    #         story=paginator.page(1)
    #     except EmptyPage:
    #         story=paginator.page(paginator.num_pages)
    # all_story=list(Story.objects.all())
    # recent_story=random.sample(all_story,3)



     # elif tag_slug:
    #     story= Story.objects.filter(tags__in=[tag_slug])
     
        
        # paginator=Paginator(story,2)
        # page=request.GET.get('page')
        # try:
        #     story=paginator.page(page)
        # except PageNotAnInteger:
        #     story=paginator.page(1)
        # except EmptyPage:
        #     story=paginator.page(paginator.num_pages)