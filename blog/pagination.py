from rest_framework.pagination import CursorPagination, LimitOffsetPagination 


class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3 