from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from registration.backends.simple.views import RegistrationView

from .models import Category, Page, UserProfile
from .forms import CategoryForm, PageForm, UserProfileForm


class IndexView(TemplateView):
    template_name = 'rango/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('-likes')[:5]
        context['most_viewed'] = Page.objects.order_by('-views')[:5]
        return context


def show_category(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)
    context_dict = {
        'pages': category.pages.order_by('-views'),  # Using related query via related name model attribute
        'category': category,
        'query': category.name
    }

    if request.method == 'POST':
        query = request.POST['query'].strip()
        result = Page.objects.filter(title__contains=query)
        if query:
            context_dict['result_list'] = result

    return render(request, 'rango/category.html', context_dict)


class CategoryList(ListView):
    queryset = Category.objects.order_by('name')
    template_name = 'rango/category_list.html'
    paginate_by = 10
    context_object_name = 'category_list'


class CategoryAdd(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('index')
    template_name = 'rango/add_category.html'
    success_message = 'The new category added successfully'

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['name'])
        return super(CategoryAdd, self).form_valid(form)


class PageAdd(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Page
    form_class = PageForm
    slug_url_kwarg = 'category_name_slug'
    template_name = 'rango/add_page.html'
    success_message = 'The new page has been added'

    def get_context_data(self, **kwargs):
        context = super(PageAdd, self).get_context_data(**kwargs)
        context['category'] = self.get_related_category()
        return context

    def get_success_url(self):
        cat_name_slug = self.kwargs['category_name_slug']
        return reverse_lazy('show_category', args=[cat_name_slug])

    def get_related_category(self):
        return get_object_or_404(Category, slug=self.kwargs['category_name_slug'])

    def form_valid(self, form):
        form.instance.category = self.get_related_category()
        return super(PageAdd, self).form_valid(form)


def track_url(request):
    url = '/rango/'
    if request.method == 'GET':
        page_id = request.GET.get('page_id', None)
        page = get_object_or_404(Page, id=page_id)
        page.views += 1
        page.save()
        url = page.url
        return redirect(url)
    if request.is_ajax():
        page_id = request.GET.get('page_id')
        return HttpResponse(page_id)


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
    cat_id = None
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


class ProfilesList(LoginRequiredMixin, ListView):
    queryset = UserProfile.objects.order_by('id')
    context_object_name = 'user_profile_list'
    template_name = 'rango/list_profiles.html'
    paginate_by = 2


# Create a new class that redirects the user to the index page,
# if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('register_profile')
