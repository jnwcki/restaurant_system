from django.conf.urls import url
from django.contrib import admin
from server_buddy import settings
from server.views import IndexView, ServerHomeView, UserCreateView, CreateOrderItem, archive_table_view, \
    KitchenListView, AddMenuItemView, CreateMenuView, MenuDetailView, ServerAddView, KitchenAddView, \
    UpdateMenuView, MenuItemDetailView, LandingView, start_table_view, add_item_to_order_view, \
    mark_table_fulfilled, RestaurantUpdateView, submit_order_view, cancel_order_view, remove_item_from_order_view, \
    add_seat_to_order_view
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
    url(r'^kitchen_list/$', KitchenListView.as_view(), name='kitchen'),
    url(r'^create/menuitem/$', AddMenuItemView.as_view(), name='add_menu_item'),
    url(r'^create/menu/$', CreateMenuView.as_view(), name='create_menu'),
    url(r'^update/menu/(?P<pk>\d+)', UpdateMenuView.as_view(), name='update_menu'),
    url(r'^menu_detail/(?P<pk>\d+)', MenuDetailView.as_view(), name='menu_detail'),
    url(r'^server/add/(?P<restaurant_id>\d+)', ServerAddView.as_view(), name='add_server'),
    url(r'^kitchen/add/(?P<restaurant_id>\d+)', KitchenAddView.as_view(), name='add_cook'),
    url(r'^menuitem/detail/(?P<pk>\d+)', MenuItemDetailView.as_view(), name='menu_item_detail'),
    url(r'^start/table/(?P<table_number>\d+)', start_table_view, name='start_table_view'),
    url(r'^table/fulfilled/(?P<table_id>\d+)', mark_table_fulfilled, name='table_fulfilled'),
    url(r'^ordercreate/(?P<table_pk>\d+)/(?P<seat_number>\d+)', CreateOrderItem.as_view(), name='order_create_view'),
    url(r'^restaurant/update/', RestaurantUpdateView.as_view(), name='restaurant_update'),
    url(r'^table/(?P<table_pk>\d+)/item/(?P<item_pk>\d+)/seat/(?P<seat_number>\d+)',
        add_item_to_order_view, name='add_item'
        ),
    url(r'^submit/order/(?P<table_pk>\d+)', submit_order_view, name='submit_order'),
    url(r'^order/cancel/(?P<table_pk>\d+)', cancel_order_view, name='cancel_order'),
    url(r'^order/ordered_item/(?P<ordered_item_pk>\d+)/table/(?P<table_pk>\d+)/seat/(?P<seat_number>\d+)',
        remove_item_from_order_view, name='remove_item'),
    url(r'table/(?P<table_pk>\d+)/archive/(?P<archive_all_boolean>\d+)', archive_table_view, name='archive'),
    url(r'tableorder/(?P<table_pk>\d+)/seat/(?P<current_seat_number>\d+)', add_seat_to_order_view, name='add_seat')
]
