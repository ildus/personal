#coding: utf-8

from django.conf import settings
import widgets
from django.db import models

class MarkdownTextField(models.TextField):
    def formfield(self, **kwargs):
        kwargs['widget'] = widgets.MarkdownEditor
        return super(MarkdownTextField, self).formfield(**kwargs)
    
