# -*-coding:utf-8-*-

from portfolio.models import Solution
from lib.decorators import render_with_context, paginate_by
from portfolio.context import default
from django.shortcuts import get_object_or_404, render_to_response, redirect

@render_with_context(default)
@paginate_by('solutions', 20)
def solutions(request):
    solutions = Solution.objects.all()
    
    return 'portfolio/solutions.html', {'solutions': solutions}

@render_with_context(default)
@paginate_by('solutions', 20)
def solutions_by_tag(request, tag):

    import urllib
    from tagging.models import Tag, TaggedItem
    
    tag = urllib.unquote(unicode(tag))
    tag = get_object_or_404(Tag, name = tag)

    solutions = TaggedItem.objects.get_by_model(Solution, tag)

    return 'portfolio/solutions.html', {'solutions': solutions}