from django.contrib import admin
from server.models import MenuItem, Menu, Restaurant, UserProfile, OrderItems, Table, Seat


class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    #extra = 2 # how many rows to show

class SeatAdmin(admin.ModelAdmin):
    inlines = (OrderItemsInline,)

admin.site.register(Seat, SeatAdmin)

admin.site.register(MenuItem)
admin.site.register(Menu)
admin.site.register(Restaurant)
admin.site.register(UserProfile)
admin.site.register([Table, OrderItems])
