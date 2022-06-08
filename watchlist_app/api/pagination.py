from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchlistPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    # page_size_query_param = 'size'
    last_page_strings = 'end',
    # offset_query_param = 'os'
    # limit_query_param = 'lm'

class WatchlistLimitPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 10