from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Category, Page
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm


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


@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                # page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


def about(request):
    return render(request, 'rango/about.html',
                  {'message': 'This tutorial has been put together by Me'})


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = user_form.cleaned_data.get('picture')

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return redirect('Your Rango account is disabled.')
        else:
            print(f'Invalid login details: {username}, {password}')
            return redirect('Invalid login details supplied.')
    else:
        return render(request, 'rango/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')
