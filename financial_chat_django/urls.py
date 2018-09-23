from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as dj_auth_views
from django.urls import include, path
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/chat/rooms/'), name='home'),
    path('admin/', admin.site.urls),
    path('login/', dj_auth_views.LoginView.as_view(), name='login'),
    path('logout/', dj_auth_views.LogoutView.as_view(), name='logout'),
    path('chat/', include('chat.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
