# -*- coding: UTF-8 -*-

from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.comments.views import comments as comments_views

from hcomments import models

import urlparse

def post_comment(request):
    result = comments_views.post_comment(request)
    if 'async' not in request.POST:
        return result
    else:
        if isinstance(result, comments_views.CommentPostBadRequest):
            return http.HttpResponseBadRequest()           
        else:
            url = urlparse.urlsplit(result['Location'])
            cid = urlparse.parse_qs(url.query).get('c')
            try:
                cid = int(cid[0])
                comment = models.HComment.objects.get(pk = cid)
            except:
                comment = None
            else:
                s = request.session.get('user-comments', set())
                s.add(cid)
                request.session['user-comments'] = s
            return render_to_response(
                'hcomments/show_single_comment.html', {
                    'c': comment,
                    'owner': True,
                },
                context_instance = RequestContext(request)
            )
