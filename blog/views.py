#-*-coding:utf-8-*-

from blog.models import Article, Comment, Category
from django.views.generic import list_detail
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.utils import simplejson

from django.conf import settings
from lib.decorators import render_with_context as _render_with_context, login_required, paginate_by
from blog.context import default as default_context

def render_with_context(func):
    """ decorator with default context of blog """
    return _render_with_context(default_context)(func)

@render_with_context
def article(request, slug):
    article = get_object_or_404(Article, slug = slug)
    
    return 'blog/article.html', {'article': article}

@render_with_context
@paginate_by('articles', 10)
def articles(request):
    return 'blog/articles.html', {'articles' : Article.published.all()}

@render_with_context
@paginate_by('articles', 10)
def category(request, slug):
    return 'blog/articles.html', {'articles' : Article.published.filter(category__slug = slug)}

@render_with_context
@paginate_by('articles', 10)
def articles_by_tag(request, tag):

    import urllib
    from tagging.models import Tag, TaggedItem
    
    tag = urllib.unquote(unicode(tag))
    tag = get_object_or_404(Tag, name = tag)

    articles = TaggedItem.objects.get_by_model(Article, tag)

    return 'blog/articles.html', {'articles' : articles}

@login_required
def comment_edit(request):
    result = {'success': False}
    if request.method == 'POST':
        print request.POST
        id_article = int(request.POST.get('id_article', 0))
        try:
            article = Article.objects.get(pk = id_article)
        except:
            article = None
            
        if article:        
            id_comment = int(request.POST.get('id_comment', 0))
            comment = request.POST.get('comment', '')
            
            if id_comment == 0:                
                comment = Comment(author = request.user, article = article, text = comment)
                comment.save()
                result = {'success': True, 'id_comment': comment.id}
        
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype = 'application/json')
    
def comment(request, cid):
    comment = get_object_or_404(Comment, pk = cid)
    return render_to_response('blog/one_comment.html', {'one': comment})