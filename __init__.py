# -*- coding: UTF-8 -*-

from django.core.urlresolvers import reverse

from hcomments import models
from hcomments import forms

def get_model():
    return models.HComment

def get_form():
    return forms.HCommentForm

