from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    # page_size = 2
    # page_size_query_param = 'size'
    # max_page_size = 10000
    def __init__(self, queryset, request):
        self.queryset = queryset
        self.request = request

    def GetPaginationQueryset(self):
        self.page_size = 2
        self.page_query_param = 'page'
        self.page_size_query_param = 'size'
        self.max_page_size = 9000
        result = self.paginate_queryset(self.queryset, self.request)
        return result

