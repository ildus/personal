#-*-coding:utf-8-*-

from blog.models import Article, Comment, Category
from django.views.generic import list_detail
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.utils import simplejson
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.conf import settings

def render_with_context(func):
    """ rendering with RequestContext """
    
    def my_render_function(request, *args, **kwargs):
        template, data = func(request, *args, **kwargs)
        data['categories'] = Category.objects.all()
        data['comments'] = Comment.objects.all()
        context = RequestContext(request, data)
        return render_to_response(template, context_instance=context)
    
    return my_render_function

def login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                result = {'success': False, 'error': _('Authorization required')}
                json = simplejson.dumps(result)
                return HttpResponse(json, mimetype = 'application/json')
            else:
                return redirect('/login/')
    
    return wrapper

@render_with_context
def article(request, slug):
    article = get_object_or_404(Article, slug = slug)
    
    return 'blog/article.html', {'article': article}

def paginate_by(items_key, count):
    ''' Разделяет на страницы, работает совместнго с тегом paginator '''
    def pager(func):
        def wrapper(request, *args, **kwargs):
            all_data = func(request, *args, **kwargs)
            paginator = Paginator(all_data[1][items_key], count)
    
            try:
                page_number = int(request.GET.get('page', '1'))
            except ValueError:
                page_number = 1
        
            try:
                page = paginator.page(page_number)
            except (EmptyPage, InvalidPage):
                page = paginator.page(paginator.num_pages)
                
            all_data[1]['page'] = page
            all_data[1]['page_number'] = page_number
            all_data[1][items_key] = page.object_list
            
            return all_data
    
        return wrapper
    
    return pager

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