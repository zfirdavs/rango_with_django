from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    return render(request, 'rango/index.html', context=context)


def about(request):
    return render(request, 'rango/about.html',
                  {'message': 'This tutorial has been put together by Me'})
