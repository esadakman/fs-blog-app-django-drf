from rest_framework.pagination import CursorPagination, LimitOffsetPagination , PageNumberPagination


class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 6 
    # page_size=1
    # limit_query_param='count' 
    # max_limit='count'

class MyCursorPagination(CursorPagination):
    page_size=3
    ordering = "-date_posted"   

 

