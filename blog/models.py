#-*-coding:utf-8-*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.html import linebreaks, escape
from django.utils.safestring import mark_safe

from django.core.urlresolvers import reverse
from tagging.fields import TagField
from tagging.models import Tag, TaggedItem

import blog

from lib.filters import filters
import lib.fields

class Category(models.Model):
    name = models.CharField(_('name'), max_length = 255)
    slug = models.SlugField(unique = True)
    
    @models.permalink
    def get_absolute_url(self):
        return blog.views.category, [self.slug]
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        
class ArticleManager(models.Manager):
    pass
    
class ArticlePublishedManager(models.Manager):
    def get_query_set(self):
        return super(ArticlePublishedManager, self).get_query_set().filter(state_published=True)

class Article(models.Model):
    author = models.ForeignKey(User, verbose_name = _('author'))
    
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, verbose_name = _('category'))
    
    title =   models.CharField(_('title'), max_length = 255)
    filter =  models.CharField(_('filter'), max_length = 20, choices=[(k, k) for k in filters.keys()], default='markdown')
    text =    models.TextField(_('text'))
    created = models.DateTimeField(auto_now_add = True)
    changed = models.DateTimeField(auto_now = True)
    deleted = models.DateTimeField(null = True, editable = False)
    state_published =  models.BooleanField(_('published'))
    
    tags = TagField()
    
    def get_tags(self):
        return Tag.objects.get_for_object(self)
    
    objects = ArticleManager()
    published = ArticlePublishedManager()
    
    @models.permalink
    def get_absolute_url(self):
        return blog.views.article, [self.slug]
    
    def get_full_url(self):
        from django.contrib.sites.models import Site        
        return 'http://%s%s' % (Site.objects.get_current().domain, self.get_absolute_url())
    
    def cat(self):
        ''' Возвращает короткий текст '''
        text = self.text
        p = text.find('<cat>')
        if p != -1:
            return self.html(text[:p])
        else:
            return self.html()
    
    def html(self, text = None):
        '''
        Возвращает HTML-текст статьи, полученный фильтрацией содержимого
        через указанный фильтр.
        '''
        if text is None:
            text = self.text.replace('<cat>', '')
            
        if self.filter in filters:
            result = filters[self.filter](text)
        else:
            result = linebreaks(escape(text))
        return mark_safe(result)
    
    def __unicode__(self):
        return '"%s" from %s at %s'% (self.title, self.author, self.created)
    
    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = ('-created', )
        
class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name = _('article'))
    author = models.ForeignKey(User, verbose_name = (_('author')))
    text = models.TextField(_('text'), max_length = 2000)
    
    created = models.DateTimeField(auto_now_add = True)
    
    def html(self):
        '''
        Возвращает HTML-текст комментария
        '''
        if 'markdown' in filters:
            result = filters['markdown'](self.text)
        else:
            result = linebreaks(escape(self.text))
        return mark_safe(result)
    
    def get_absolute_url(self):
        url_begin = self.article.get_absolute_url()
        return "%s#comment%s"%(url_begin, self.id)
    
    def __unicode__(self):
        return u"%s - at %s from %s"%(self.article, self.created, self.author)
    
    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ('-id', )