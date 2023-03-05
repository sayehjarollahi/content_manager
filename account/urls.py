from django.urls import path

from account.views import register_view, create_library_view, index_view

urlpatterns = [
    path('', index_view.index, name='home'),
    path('create_library/', create_library_view.create_library, name='index'),
    path('register/', register_view.register, name='register'),
]
