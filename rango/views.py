from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Category, Page


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    viewed_pages = Page.objects.order_by('-views')[:5]
    context_dict = {
        'categories': category_list,
        'most_viewed': viewed_pages
    }
    return render(request, 'rango/index.html', context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    category = get_object_or_404(Category, slug=category_name_slug)
    pages = Page.objects.filter(category=category)
    context_dict['pages'] = pages
    context_dict['category'] = category

    return render(request, 'rango/category.html', context_dict)


def about(request):
    return render(request, 'rango/about.html',
                  {'message': 'This tutorial has been put together by Me'})
