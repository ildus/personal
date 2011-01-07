# -*- coding: UTF-8 -*-

from django import template
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

register = template.Library()

@register.inclusion_tag('main_menu.html', takes_context = True)
def main_menu(context):
    menu_items = (['blog', 'Блог'], ['about', 'Обо мне'])#, ['portfolio', 'Портфолио'])
    try:
        path = context['request'].path
    except:
        path = ''
        
    for item in menu_items:
        url = reverse(item[0])
        item.append(url)
        item.append(path.startswith(url))
        
    return {'menu': menu_items}