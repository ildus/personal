from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms import widgets

class MarkdownEditor(widgets.Textarea):
    
    def __init__(self, attrs=None):
        if not attrs: attrs = {}
        
        if not attrs.has_key('class'): attrs['class'] = ''        
        attrs['class'] += ' markdown_editor'
        
        default_attrs = {'cols': '80', 'rows': '20'}
        
        if attrs:
            default_attrs.update(attrs)
        super(MarkdownEditor, self).__init__(default_attrs)
    
    class Media:
        js = (
            settings.MEDIA_URL + 'lib/js/jquery.js',
            settings.MEDIA_URL + 'lib/markitup/jquery.markitup.pack.js',
            settings.MEDIA_URL + 'lib/markitup/sets/markdown/set.js',
        )
        
        css = {
            'screen': (
                settings.MEDIA_URL + 'lib/markitup/skins/simple/style.css',
                settings.MEDIA_URL + 'lib/markitup/sets/markdown/style.css',
            )
        }

    def render(self, name, value, attrs=None):       
        
        rendered = super(MarkdownEditor, self).render(name, value, attrs)
        return rendered + mark_safe('''
            <script type="text/javascript">
                $(document).ready(function()    {
                    $('textarea.markdown_editor').markItUp(mySettings);
                });
            </script>
        ''')