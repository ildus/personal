#-*-coding:utf-8-*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.html import linebreaks, escape
from django.utils.safestring import mark_safe

from django.core.urlresolvers import reverse
from tagging.fields import TagField
from tagging.models import Tag, TaggedItem

from lib.utils import make_upload_path
from lib.filters import filters

class Solution(models.Model):
    title = models.CharField(_('title'), max_length = 1000)
    description = models.TextField(verbose_name = _('description'))
    image = models.ImageField(_('image'), upload_to = make_upload_path)
    url = models.URLField(_('url'), blank = True)
    repository = models.URLField(_('repository'), blank = True)
    
    created = models.DateField(auto_now_add = True)
    
    dev_begin = models.DateField(_("start of development"), null = True)
    dev_end = models.DateField(_('end of development'), null = True)
    
    tags = TagField(_('tags'))
    
    def text(self):
        if 'markdown' in filters:
            result = filters['markdown'](self.description)
        else:
            result = linebreaks(escape(self.description))
        return mark_safe(result)
        
    
    def __unicode__(self):
        return "%s"%(self.title)
    
    class Meta:
        verbose_name = _('solution')
        verbose_name_plural = _('solutions')
        ordering = ('-created', )