from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def get_action(action_parameter=None, *args, **kwargs):
    if action_parameter is not None:
        action_data = {
            'create': ['add', 'post', 'create'],
            'view': ['view', 'show', 'get'],
            'delete': ['remove', 'delete', 'del'],
            'patch': ['update', 'upgrade', 'edit']
        }
        for key, value in action_data.items():
            if action_parameter in value:
                return key
    else:
        return False

def pagination_function(request=None, data=None, *args, **kwargs):
    page_data = Paginator(data, 2)
    num_pages = page_data.num_pages
    if request.data.get('pagination', None):
        if int(request.data.get('pagination')) != 0:
            try:
                data = page_data.page(int(request.data['pagination']))
            except PageNotAnInteger:
                data = page_data.page(1)
            except EmptyPage:
                data = page_data.page(page_data.num_pages)
            return {'data': data, 'num_pages': num_pages}
        return {'data': data}
    return {'data': 404}
