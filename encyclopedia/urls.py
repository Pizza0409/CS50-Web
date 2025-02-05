from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_page, name="entry_page"),  # 為條目頁增加動態路由
    path("wiki/<str:title>/edit", views.edit_page, name="edit_page"),
    path("wiki/error_page", views.content_not_found, name="error_page"),
    path("search_result", views.search_result, name="search_result"),
    path("create_page", views.create_page, name="create_page"),
    path("random", views.random_page, name="random_page"),
]
