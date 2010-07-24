# -*- coding:utf-8 -*-
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.conf import settings

register=template.Library()
art_template = template.loader.get_template('blog/one_article.html')
comment_template = template.loader.get_template('blog/one_comment.html')

@register.inclusion_tag('blog/one_article.html')
def show_article_description(article):
    text = article.cat()
    if text is None:
        text = article.html()
        
    return {'one': article, 'text': text}

@register.simple_tag
def show_comment(comment):
    context = template.Context({'one': comment})
    
    return comment_template.render(context)