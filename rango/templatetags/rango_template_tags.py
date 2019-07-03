from django import template
from urllib.parse import urlencode
from rango.models import Category

register = template.Library()


@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(), 'act_cat': cat}


@register.simple_tag
def url_params(*_, **kwargs):
    safe_args = {key: value for key, value in kwargs.items() if value is not None}
    if safe_args:
        return f'?{format(urlencode(safe_args))}'
    return ''
