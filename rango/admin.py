from django.contrib import admin
from .models import Category, Page


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


admin.site.register(Page, PageAdmin)
admin.site.register(Category, CategoryAdmin)
