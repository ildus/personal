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

from django.utils import feedgenerator
from django.core.urlresolvers import reverse

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

class BlogFeed(feedgenerator.Rss201rev2Feed):
    
    def add_root_elements(self, handler):
        handler.addQuickElement(u"title", self.feed['title'])
        handler.addQuickElement(u"link", self.feed['link'])
        handler.addQuickElement(u"description", self.feed['description'])
        handler.addQuickElement(u"atom:link", None, {u"rel": u"self", u"href": self.feed['feed_url']})
        if self.feed['language'] is not None:
            handler.addQuickElement(u"language", self.feed['language'])
        for cat in self.feed['categories']:
            handler.addQuickElement(u"category", cat)
        if self.feed['feed_copyright'] is not None:
            handler.addQuickElement(u"copyright", self.feed['feed_copyright'])
        #handler.addQuickElement(u"lastBuildDate", rfc2822_date(self.latest_post_date()).decode('utf-8'))
        if self.feed['ttl'] is not None:
            handler.addQuickElement(u"ttl", self.feed['ttl'])
            
        if self.feed.get('image', ''):
            handler.addQuickElement('image', self.feed['image'])
            
        handler.addQuickElement(u"pubDate", self.feed['pubdate'])    
        handler.addQuickElement(u"lastBuildDate", self.feed['lastbuilddate'])

def rss(request):
    from datetime import datetime
    from django.utils.feedgenerator import rfc2822_date
    
    items = Article.objects.all()[:50]
    
    latest = Article.objects.latest('created')
    latest_date = latest.created if latest else datetime.now()
    
    
    feed = BlogFeed(
        title = 'Оптимальный веб-блог',
        link = 'http://ildus.org',
        description = 'Блог о веб-разработке, Django, Python и о других интересных мне вещах',
        language = 'ru',
        feed_url = reverse('blog_rss'),
        categories = [unicode(category) for category in Category.objects.all()],
        pubdate = rfc2822_date(latest_date),
        lastbuilddate = rfc2822_date(datetime.now()),
        image = None
    )
    
    for item in items:        
        feed.add_item(
            title = item.title,
            link = item.get_absolute_url(),
            description = item.cat(),
            unique_id = item.get_absolute_url(),
            author_name = item.author.get_full_name(),
            author_email = item.author.email,
            author_link = reverse('about'),
            pubdate = item.created
        )
        
    return HttpResponse(feed.writeString('UTF-8'), mimetype = 'application/rss+xml; charset=utf-8');