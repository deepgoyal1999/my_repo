from blog.models import Post
from django import template
register=template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.count()


@register.inclusion_tag('blog/latest_posts123.html')
def show_latest(count=3):
    latest_posts=Post.objects.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

from django.db.models import Count
@register.assignment_tag
def  get_most_commented_posts(count=3):
    return Post.objects.annotate(tot_cmmnt=Count('comments')).order_by('-tot_cmmnt')[:count]
