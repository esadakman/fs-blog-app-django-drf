from rest_framework.pagination import CursorPagination, LimitOffsetPagination 


class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3 

class MyCursorPagination(CursorPagination):
    page_size=3
    ordering = "-date_posted"   