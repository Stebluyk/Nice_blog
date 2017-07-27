from django.views.generic.base import ContextMixin


class CustomPaginatorMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(CustomPaginatorMixin, self).get_context_data(**kwargs)
        if context['is_paginated']:
            context['page_range'] = get_page_range(context.get('page_obj').number, context.get('paginator'))
        return context


def get_page_range(page, paginator):
    """ Return page range (for pagination). """
    page = int(page)
    min_p = page - 2
    max_p = page + 3
    if min_p < 1:
        min_p = 1
    if page < 3:
        max_p = 6
    else:
        buff = paginator.num_pages - page
        if buff < 2:
            min_p = page - 4 + buff
        if min_p < 1:
            min_p = 1
    if max_p > paginator.num_pages:
        max_p = paginator.num_pages + 1
    return range(min_p, max_p)
