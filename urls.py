# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *
from microblog import views, models, feeds, settings

urlpatterns = patterns('',
    url(
        r'post$', 'hcomments.views.post_comment',
        name = 'hcomments-post-comment',
    ),
)
