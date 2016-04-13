from django.conf.urls import url
from django.contrib import admin
from server_buddy import settings
from server.views import IndexView, ServerHomeView, UserCreateView, \
    KitchenListView, AddMenuItemView, CreateMenuView, MenuDetailView, ServerAddView, KitchenAddView, \
    UpdateMenuView, MenuItemDetailView, LandingView, FunctionBasedCreateOrder, \
    FunctionBasedUpdateOrder, mark_table_fulfilled, RestaurantUpdateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)', 'django.views.static.serve', {"document_root": settings.MEDIA_ROOT}),
    url(r'^$', LandingView.as_view(), name='landing'),
    url(r'^index/$', IndexView.as_view(), name='index'),
    url(r'^server/home/$', ServerHomeView.as_view(), name='server_home'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
    url(r'^signup/$', UserCreateView.as_view(), name='signup'),
    url(r'^order/new/(?P<table_number>\d+)', FunctionBasedCreateOrder, name='order_create_view'),
    # url(r'^order_detail/(?P<pk>\d+)', OrderDetailView.as_view(), name='order_detail'),
    # url(r'^order/update/(?P<pk>\d+)', OrderUpdateView.as_view(), name='order_update'),
    url(r'^kitchen_list/$', KitchenListView.as_view(), name='kitchen'),
    url(r'^create/menuitem/$', AddMenuItemView.as_view(), name='add_menu_item'),
    url(r'^create/menu/$', CreateMenuView.as_view(), name='create_menu'),
    url(r'^update/menu/(?P<pk>\d+)', UpdateMenuView.as_view(), name='update_menu'),
    url(r'^menu_detail/(?P<pk>\d+)', MenuDetailView.as_view(), name='menu_detail'),
    url(r'^server/add/(?P<restaurant_id>\d+)', ServerAddView.as_view(), name='add_server'),
    url(r'^kitchen/add/(?P<restaurant_id>\d+)', KitchenAddView.as_view(), name='add_cook'),
    url(r'^menuitem/detail/(?P<pk>\d+)', MenuItemDetailView.as_view(), name='menu_item_detail'),
    url(r'^table/order/update/(?P<table_pk>\d+)', FunctionBasedUpdateOrder, name='order_update_view'),
    url(r'^table/fulfilled/(?P<table_id>\d+)', mark_table_fulfilled, name='table_fulfilled'),
    # url(r'^ordercreate/(?P<table_number>\d+)', CreateOrderItem.as_view(), name='order_create_viewx'),
    url(r'^restaurant/update/', RestaurantUpdateView.as_view(), name='restaurant_update')
]
