
from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter
def truncate_url(img_obj):

    return img_obj.name.split("/",maxsplit=1)[-1]

#区分评论数与点赞数
@register.simple_tag
def filter_comment(article_obj):
    query_set = article_obj.comment_set.select_related()
    comments = {
        'comment_count':query_set.filter(comment_type=1).count,
        'thumb_count':query_set.filter(comment_type=2).count
    }
    return comments
