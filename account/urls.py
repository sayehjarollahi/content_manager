from django.urls import path

from account.views import register_view, index_view, my_page_view, content_view, profile_view, \
    library_view

urlpatterns = [
    path('', index_view.index, name='home'),
    path('register/', register_view.register, name='register'),
    path('add-content/', content_view.add_content, name='add-content'),
    path('profile/', profile_view.profile, name='profile'),
    path('delete-content', content_view.delete_content, name='delete-content'),
    path('add-library/', library_view.add_library, name='add-library'),
    path('delete-library', library_view.delete_library, name='delete-library'),
    path('my-page/<str:page_type>/<str:categoryTitle>/', my_page_view.my_page, name='my_page'),
    path('library/<int:libraryId>/', library_view.library_page, name='library-page'),
    path('content/<int:content_id>/addLibrary/<int:library_id>/', content_view.add_to_library, name='add_library'),
    path('content/<int:content_id>/shareContent/<str:username>/', content_view.share_content, name='share_content'),
    path('content/<int:content_id>/download-link-content', content_view.create_download_link, name='download-content'),

    path('content/<int:content_id>/', content_view.content_main_page, name='content_main_page'),
]
