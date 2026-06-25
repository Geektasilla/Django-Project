from rest_framework.pagination import CursorPagination

class CategoryPagination(CursorPagination):
    ordering = 'name'

class MainCursorPagination(CursorPagination):
    ordering = '-created_at'
