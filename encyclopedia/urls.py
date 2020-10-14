from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<slug:title>/", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("new", views.new_entry, name="new"),
    path("edit/<slug:title>", views.edit_entry, name="edit"),
    path("randompick", views.random_pick, name="randompick"),
]
