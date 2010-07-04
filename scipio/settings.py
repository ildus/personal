# -*- coding:utf-8 -*-

import os
def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

# OpenID sessions dir.
# OpenID authentication will not work without it.
SCIPIO_STORE_ROOT = rel('storage')

# URL passed to OpenID-provider to identify site that requests authentication.
# Should not end with '/'.
# Complete site URL is passed if the value is empty.
SCIPIO_TRUST_URL = ''

# Akismet key
SCIPIO_AKISMET_KEY = ''