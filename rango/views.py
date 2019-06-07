from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Category, Page, UserProfile
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
from datetime import datetime
from registration.backends.simple.views import RegistrationView


def index(request):
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    viewed_pages = Page.objects.order_by('-views')[:5]
    context_dict = {
        'categories': category_list,
        'most_viewed': viewed_pages,
    }
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/index.html', context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    category = get_object_or_404(Category, slug=category_name_slug)
    pages = Page.objects.filter(category=category).order_by('-views')
    context_dict['pages'] = pages
    context_dict['category'] = category

    context_dict['query'] = category.name
    if request.method == 'POST':
        query = request.POST['query'].strip()
        result = Page.objects.filter(title__contains=query)
        if query:
            context_dict['result_list'] = result

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
    visitor_cookie_handler(request)
    context = {
        'visits': request.session['visits']
    }
    return render(request, 'rango/about.html', context)


# def register(request):
#     registered = False
#
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#
#             # Now we hash the password with the set_password method.
#             # Once hashed, we can update the user object.
#             user.set_password(user.password)
#             user.save()
#
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             if 'picture' in request.FILES:
#                 profile.picture = user_form.cleaned_data.get('picture')
#
#             profile.save()
#             registered = True
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     return render(request, 'rango/register.html', {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'registered': registered
#     })


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password)
#
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return redirect(reverse('index'))
#             else:
#                 return redirect('Your Rango account is disabled.')
#         else:
#             print(f'Invalid login details: {username}, {password}')
#             return redirect('Invalid login details supplied.')
#     else:
#         return render(request, 'rango/login.html')


# @login_required
# def user_logout(request):
#     logout(request)
#     return redirect(reverse('index'))


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        # update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def track_url(request):
    url = '/rango/'
    if request.method == 'GET':
        page_id = request.GET.get('page_id', None)
        page = get_object_or_404(Page, id=page_id)
        page.views += 1
        page.save()
        url = page.url
        return redirect(url)


@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('index')
        else:
            print(form.errors)

    return render(request, 'rango/profile_registration.html', {'form': form})


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'website': userprofile.website, 'picture': userprofile.picture}
    )

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)

    return render(request, 'rango/profile.html', {
        'userprofile': userprofile,
        'selecteduser': user,
        'form': form
    })


@login_required
def like_category(request):
    likes = 0
    if request.method == 'GET':
        cat_id = request.GET.get('category_id', None)

    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()

    return HttpResponse(likes)


def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]

    return cat_list


def suggest_category(request):
    starts_with = ''

    if request.method == 'GET':
        starts_with = request.GET.get('suggestion')
    cat_list = get_category_list(8, starts_with)

    return render(request, 'rango/cats.html', {'cats': cat_list})


@login_required
def list_profiles(request):
    return render(request, 'rango/list_profiles.html',
                  {'userprofile_list': UserProfile.objects.all()})


# Create a new class that redirects the user to the index page,
# if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('register_profile')
