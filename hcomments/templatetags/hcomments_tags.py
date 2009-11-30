# -*- coding: UTF-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType

import mptt
import mptt.utils

from hcomments import models

import hashlib
import urllib

register = template.Library()

@register.inclusion_tag('hcomments/show_comment_list.html', takes_context = True)
def show_comment_list(context, object):
    ctype = ContentType.objects.get_for_model(object)
    tree = models.HComment.tree.root_nodes().filter(
        content_type = ctype,
        object_pk = object.id,
        is_public = True,
        is_removed = False,
    )
    comments = []
    for root in tree:
        comments.extend(root.get_descendants(True))
    context.update({ 'comments': comments })
    return context

@register.inclusion_tag('hcomments/show_single_comment.html', takes_context = True)
def show_single_comment(context, comment):
    request = context['request']
    if 'user-comments' in request.session:
        owner = comment.id in request.session['user-comments']
    else:
        owner = False
    return {
        'c': comment,
        'owner': owner,
    }

@register.filter
def gravatar(email, args=''):
    if args:
        args = dict(a.split('=') for a in args.split(','))
    else:
        args = {}

    # Set your variables here
    default = args.get('default', '404')
    size = args.get('size', '80')
    rating = args.get('rating', 'r')

    # construct the url
    gravatar_url = 'http://www.gravatar.com/avatar/%s?' % hashlib.md5(email.lower()).hexdigest()
    gravatar_url += urllib.urlencode({
        'default': default,
        'size': str(size),
        'rating': rating,
    })
    return gravatar_url

