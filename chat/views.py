from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from chat.models import Profile, Room


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'room_list.html'


class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = 'room_detail.html'


# TODO: Post message (AJAX/WebSockets)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profile_detail.html'
