from django.conf.urls import url
from django.contrib import admin
from server_buddy import settings
from django.views.static import serve
from server.views import IndexView, ServerHomeView, UserCreateView, OrderCreateView, OrderDetailView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^server/home/$', ServerHomeView.as_view(), name='server_home'),
    url(r'^accounts/login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout_then_login, name='logout'),
    url(r'^signup/', UserCreateView.as_view(), name='signup'),
    url(r'^order/new/', OrderCreateView.as_view(), name='order_create_view'),
    url(r'^order_detail/(?P<pk>\d+)', OrderDetailView.as_view(), name='order_detail')
]
