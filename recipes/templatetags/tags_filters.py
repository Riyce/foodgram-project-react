from django import template

register = template.Library()


@register.filter
def get_tags(request):
    return request.GET.getlist('tags')


@register.filter
def set_tags(request, tag):
    new_request = request.GET.copy()
    tags = request.GET.getlist('tags')
    if tag.slug in tags:
        tags.remove(tag.slug)
    else:
        tags.append(tag.slug)
    new_request.setlist('tags', tags)
    return new_request.urlencode()


@register.filter
def add_tags(request):
    tags = [f'tags={tag}' for tag in request.GET.getlist('tags')]
    return '&'.join(tags)
