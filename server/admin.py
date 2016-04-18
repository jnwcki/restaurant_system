from django.contrib import admin
from server.models import MenuItem, Menu, Restaurant, UserProfile, Table, OrderedItem, ApiKey


admin.site.register(MenuItem)
admin.site.register(Menu)
admin.site.register(Restaurant)
admin.site.register(UserProfile)
admin.site.register(Table)
admin.site.register(OrderedItem)
admin.site.register(ApiKey)
