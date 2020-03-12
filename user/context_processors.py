# -*- coding: utf-8 -*-
from .forms import LoginForms


def login_form_init(request):
    return {'login_form': LoginForms()}
