from django.contrib import admin
from server.models import MenuItem, Menu, Restaurant, UserProfile, Order, Table

admin.site.register(MenuItem)
admin.site.register(Menu)
admin.site.register(Restaurant)
admin.site.register(UserProfile)
admin.site.register([Order, Table])
