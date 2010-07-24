#-*-coding:utf-8-*-

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

def index(request):
    return redirect('/about/')

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))
