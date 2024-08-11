from django.urls import path
from . import views

app_name='wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.entry_page,name="entry"),
    path("search",views.search,name="search"),
    path("random",views.random_page,name="random"),
    path("edit/<str:title>",views.edit_page,name="edit"),
    path("create",views.new_page,name="create")
]
