# -*- coding: UTF-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType

import mptt
import mptt.utils

from hcomments import models

register = template.Library()

@register.inclusion_tag('hcomments/show_comment_list.html', takes_context = True)
def show_comment_list(context, object):
    ctype = ContentType.objects.get_for_model(object)
    print repr(ctype), ctype.id
    tree = models.HComment.tree.root_nodes().filter(
        content_type = ctype,
        object_pk = object.id,
    )
    comments = []
    for root in tree:
        comments.extend(root.get_descendants(True))
    return {
        'comments': comments,
    }
