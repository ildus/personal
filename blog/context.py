# -*- coding:utf-8 -*-

from blog.models import Comment, Category

def default(request):
    data = {
         'categories': Category.objects.all(),         
    }
    
    return data