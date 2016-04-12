from django.contrib import admin
from server.models import MenuItem, Menu, Restaurant, UserProfile, Table, Order


class OrderInLine(admin.TabularInline):
    model = Order


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderInLine,)

admin.site.register(MenuItem)
admin.site.register(Menu)
admin.site.register(Restaurant)
admin.site.register(UserProfile)
admin.site.register(Table)
admin.site.register(Order)
