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
                if not comment.is_public:
                    return http.HttpResponse(content = 'moderated', status = 403)
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

def delete_comment(request):
    if request.method != 'POST':
        raise http.HttpResponseBadRequest()
    try:
        cid = int(request.POST['cid'])
    except:
        raise http.HttpResponseBadRequest()
    s = request.session.get('user-comments', set())
    if cid not in s:
        raise http.HttpResponseBadRequest()
    s.remove(cid)
    try:
        comment = models.HComment.objects.get(pk = cid)
    except models.HComment.DoesNotExist:
        pass
    else:
        comment.delete()
    return http.HttpResponse('')
