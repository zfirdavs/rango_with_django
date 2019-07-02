from django import forms
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from .models import Category, Page, UserProfile


class CategoryForm(forms.ModelForm):
    name = forms.CharField(help_text='Please enter the category name.')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

    def clean_name(self):
        name = self.cleaned_data['name']
        slug = slugify(name)

        if Category.objects.filter(slug=slug).exists():
            raise ValidationError(f'A category with {slug} slug already exists.')
        return name


class PageForm(forms.ModelForm):
    title = forms.CharField(help_text='Please enter the title of the page.')
    url = forms.URLField(max_length=200,
                         help_text='Please enter the URL of the page.')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
            return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
