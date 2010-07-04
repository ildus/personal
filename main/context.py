# -*- coding:utf-8 -*-

from scipio.forms import AuthForm

def default(request):
    data = {}
    if not request.user.is_authenticated():
        data['auth_form'] = AuthForm(request.session)
    return data
