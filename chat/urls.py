from django.urls import path

from chat import views


urlpatterns = [
    path('rooms/', views.RoomListView.as_view(), name='room_list'),
    path('room/<str:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile_detail'),
]
