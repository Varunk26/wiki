from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.title, name="title"),
    path("search", views.search, name="search"),
    path("createpage/", views.createpage, name="createpage"),
    path("editpage/<str:name>", views.editpage, name="editpage"),
    path("randompage", views.randompage, name="randompage")
]
