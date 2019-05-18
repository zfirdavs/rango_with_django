from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Rango says hey there partner! Here is the <a href="/rango/about">link</a>')


def about(request):
    return HttpResponse('Rango says here is the about page. Here is the <a href="/">link</a>')
