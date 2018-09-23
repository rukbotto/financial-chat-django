from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from chat.models import Profile, Room
from chat.forms import MessageForm


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'room_list.html'


class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = 'room_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MessageForm()
        return context


# TODO: Post message (AJAX/WebSockets)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profile_detail.html'
