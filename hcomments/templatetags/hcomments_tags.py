# -*- coding: UTF-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType
from django.template import Context

import mptt
import mptt.utils

from hcomments import models

import hashlib
import urllib

register = template.Library()

def _get_comment_list(object):
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
    return comments

@register.tag
def get_comment_list(parser, token):
    """
    {% get_comment_list object as comments %}
    """
    class Node(template.Node):
        def __init__(self, object, var_name):
            self.object = template.Variable(object)
            self.var_name = var_name

        def render(self, context):
            context[self.var_name] = _get_comment_list(self.object.resolve(context))
            return ''

    contents = token.split_contents()
    tag_name = contents.pop(0)
    object = contents.pop(0)

    if contents[-2] != 'as':
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
    var_name = contents[-1]
    return Node(object, var_name)

@register.inclusion_tag('hcomments/show_comment_list.html', takes_context = True)
def show_comment_list(context, object, object_owner=None):
    ctx = Context(context)
    ctx.update({
        'comments': _get_comment_list(object),
        'object_owner': object_owner,
    })
    return ctx

@register.inclusion_tag('hcomments/show_single_comment.html', takes_context = True)
def show_single_comment(context, comment, object_owner=None):
    request = context['request']
    if 'user-comments' in request.session:
        owner = comment.id in request.session['user-comments']
    else:
        owner = False
    return {
        'c': comment,
        'owner': owner,
        'object_owner': object_owner,
    }

@register.inclusion_tag('hcomments/show_comment_form.html', takes_context=True)
def show_comment_form(context, object):
    ctx = Context(context)
    ctx.update({
        'object': object,
    })
    return ctx

@register.inclusion_tag('hcomments/show_subscribe_form.html', takes_context=True)
def show_subscribe_form(context, object):
    ctx = Context(context)
    ctx.update({
        'object': object,
    })
    return ctx

@register.filter
def subscribed(object, user):
    return models.ThreadSubscription.objects.subscribed(object, user)

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

