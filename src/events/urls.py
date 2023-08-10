from . import views
from django.urls import path

urlpatterns = [
    path('', views.homepage),
    path('create_event/', views.create_event, name="create_event"),
    path('edit_event/<str:event_id>', views.edit_event, name="edit_event"),
    path("change_num/<str:event_id>",views.change_num,name="change_num"),
    # path('search_events/<str:search_text>', views.search_events, name="search_events"),
]
