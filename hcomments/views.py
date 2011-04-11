# -*- coding: UTF-8 -*-
import urlparse

try:
    parse_qs = urlparse.parse_qs
except AttributeError:
    from cgi import parse_qs

from django import http
from django.conf import settings as dsettings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.comments.views import comments as comments_views
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from hcomments import models

def post_comment(request):
    result = comments_views.post_comment(request)
    if 'async' not in request.POST:
        return result
    else:
        if isinstance(result, comments_views.CommentPostBadRequest):
            if dsettings.DEBUG:
                msg = 'invalid request'
            else:
                msg = ''
            return http.HttpResponseBadRequest(msg)
        else:
            try:
                url = urlparse.urlsplit(result['Location'])
                cid = parse_qs(url.query).get('c')
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
            except Exception, e:
                if dsettings.DEBUG:
                    return http.HttpResponseBadRequest(str(e))
                else:
                    raise

def delete_comment(request):
    if request.method != 'POST':
        return http.HttpResponseBadRequest()
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

def subscribe(request):
    if request.method != 'POST':
        return http.HttpResponseNotAllowed(('POST',))
    if not request.user.is_authenticated():
        return http.HttpResponseBadRequest()
    content_type = request.POST['content_type']
    object_pk = request.POST['object_pk']

    app_label, model = content_type.split('.', 1)
    ct = ContentType.objects.get(app_label=app_label, model=model)
    object = ct.get_object_for_this_type(pk=object_pk)
    if 'subscribe' in request.POST:
        models.ThreadSubscription.objects.subscribe(object, request.user)
    elif 'unsubscribe' in request.POST:
        models.ThreadSubscription.objects.unsubscribe(object, request.user)

    return redirect(request.META.get('HTTP_REFERER', '/'))

@staff_member_required
def moderate_comment(request, cid, public = False):
    try:
        comment = get_object_or_404(models.HComment, pk = int(cid))
    except (TypeError, ValueError):
        return http.HttpResponseBadRequest()
    comment.is_public = public
    comment.save()
    return http.HttpResponse(content = 'done', status = 200)
