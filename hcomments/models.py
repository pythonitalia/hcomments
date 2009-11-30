# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.comments.models import Comment

import mptt

class HComment(Comment):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

mptt.register(HComment)

