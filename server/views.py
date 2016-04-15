from server.models import UserProfile, Restaurant, MenuItem, Menu, Table, OrderedItem
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, ListView, UpdateView
from server.forms import EmployeeCreateForm, MenuItemForm, MenuCreateForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm


class LandingView(TemplateView):
    template_name = 'landing.html'


def employee_login_redirect(request):
    employee_position = request.user.userprofile.position
    if employee_position == 'M':
        return HttpResponseRedirect(reverse('index'))
    elif employee_position == 'S':
        return HttpResponseRedirect(reverse('server_home'))
    else:
        return HttpResponseRedirect(reverse('kitchen'))


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        context = super(IndexView, self).get_context_data()
        current_server = UserProfile.objects.get(user=self.request.user)
        current_restaurant = current_server.workplace
        all_menus = Menu.objects.filter(restaurant=current_restaurant)
        employee_list = UserProfile.objects.filter(workplace=self.request.user.userprofile.workplace)

        context['user'] = self.request.user
        context['servers'] = employee_list.filter(position='S')
        context['kitchen'] = employee_list.filter(position='K')
        context['menus'] = all_menus
        return context


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm

    def form_valid(self, form):
        user_object = form.save()
        new_restaurant = Restaurant.objects.create()
        profile = UserProfile.objects.create(
                                             user=user_object,
                                             workplace=new_restaurant,
                                             position='M'
                                             )
        profile.save()
        Menu.objects.create(restaurant=new_restaurant, name="Menu")
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)

    def get_success_url(self):
        return reverse('login')


class ServerHomeView(TemplateView):
    template_name = 'server_home.html'

    def get_context_data(self):
        context = super(ServerHomeView, self).get_context_data()
        current_server = UserProfile.objects.get(user=self.request.user)
        if current_server.position != 'K':
            current_restaurant = current_server.workplace
            bound_table_list = Table.objects.filter(server__workplace=current_restaurant,
                                                    fulfilled=False,
                                                    canceled=False,
                                                    )
            all_tables_list = [x for x in range(1, current_restaurant.number_of_tables + 1)]
            bound_table_numbers = bound_table_list.values_list('number', flat=True)
            unbound_tables = [x for x in all_tables_list if x not in bound_table_numbers]
            all_menus = Menu.objects.filter(restaurant=current_restaurant)

            context['first_menu'] = all_menus[0]
            context['restaurant'] = current_restaurant
            context['server'] = current_server
            context['bound_tables'] = bound_table_list
            context['unbound_tables'] = unbound_tables
        else:
            return reverse('kitchen')
        return context


def start_table_view(request, table_number, menu_pk):
    server = request.user.userprofile
    created_table = Table.objects.create(number=table_number, server=server)

    return HttpResponseRedirect(reverse('order_create_view',
                                        kwargs={'table_pk': created_table.pk,
                                                'seat_number': 1,
                                                'menu_pk': menu_pk
                                                }
                                        )
                                )


def add_item_to_order_view(request, table_pk, item_pk, seat_number, menu_pk):
    working_table = Table.objects.get(pk=table_pk)
    working_item = MenuItem.objects.get(pk=item_pk)

    OrderedItem.objects.create(table=working_table, item=working_item, seat_number=seat_number)

    return HttpResponseRedirect(reverse('order_create_view',
                                        kwargs={'table_pk': table_pk,
                                                'seat_number': seat_number,
                                                'menu_pk': menu_pk
                                                }
                                        )
                                )


def remove_item_from_order_view(request, table_pk, ordered_item_pk, seat_number, menu_pk):
    working_item_order = OrderedItem.objects.get(pk=ordered_item_pk)
    working_item_order.canceled = True
    working_item_order.save()
    return HttpResponseRedirect(reverse('order_create_view',
                                        kwargs={'table_pk': table_pk,
                                                'seat_number': seat_number,
                                                'menu_pk': menu_pk
                                                }
                                        )
                                )


def submit_order_view(request, table_pk):
    # print("working table is working!!!")
    working_table = Table.objects.get(pk=table_pk)
    working_table.sent = True
    for item in working_table.ordereditem_set.all():
        item.sent = True
        item.save()
    working_table.save()
    return HttpResponseRedirect(reverse('server_home'))


def cancel_order_view(request, table_pk):
    working_table = Table.objects.get(pk=table_pk)
    working_table.canceled = True
    working_table.save()
    return HttpResponseRedirect(reverse('server_home'))


def archive_table_view(request, table_pk, archive_all_boolean):
    if str(archive_all_boolean) == '0':
        working_table = Table.objects.get(pk=table_pk)
        working_table.archived = True
        working_table.save()

    else:
        tables_to_archive = Table.objects.filter(
                                                 sent=True,
                                                 fulfilled=True,
                                                 archived=False
                                                 )
        for table in tables_to_archive:
            table.archived = True
            table.save()

    return HttpResponseRedirect(reverse('kitchen'))


def add_seat_to_order_view(request, table_pk, current_seat_number, menu_pk):
    seat_number = int(current_seat_number) + 1
    return HttpResponseRedirect(reverse('order_create_view',
                                        kwargs={'table_pk': table_pk,
                                                'seat_number': seat_number,
                                                'menu_pk': menu_pk
                                                }
                                        )
                                )


class CreateOrderItem(TemplateView):
    template_name = 'server/order_form.html'

    def get_context_data(self, **kwargs):
        context = super(CreateOrderItem, self).get_context_data(**kwargs)
        seat_number = self.kwargs['seat_number']
        current_table = Table.objects.get(pk=self.kwargs['table_pk'])
        ordered_items_list = OrderedItem.objects.filter(table=current_table, canceled=False)
        current_menu = Menu.objects.get(pk=self.kwargs['menu_pk'])

        seats_list = [1]
        for item in ordered_items_list:
            seats_list.append(item.seat_number)

        context['working_seats'] = set(seats_list)
        context['last_seat'] = max(context['working_seats'])

        ticket_total = 0
        for item in ordered_items_list:
            ticket_total += item.item.price
        context['ticket_total'] = ticket_total
        context['current_table'] = current_table
        context['current_menu'] = current_menu
        context['table_pk'] = current_table.pk
        context['table_number'] = current_table.number
        context['seat_number'] = int(seat_number)
        context['ordered_items_list'] = ordered_items_list
        context['menus_list'] = Menu.objects.filter(restaurant=self.request.user.userprofile.workplace)
        return context


class KitchenListView(ListView):
    model = Table

    def get_context_data(self, **kwargs):
        context = super(KitchenListView, self).get_context_data(**kwargs)
        context['table_list'] = Table.objects.filter(
                                                     server__workplace=self.request.user.userprofile.workplace,
                                                     sent=True,
                                                     canceled=False,
                                                     archived=False
                                                     )

        return context


class MenuDetailView(DetailView):
    model = Menu


class AddMenuItemView(CreateView):
    model = MenuItem
    # fields = ['name', 'description', 'price', 'photo', 'item_type']
    form_class = MenuItemForm
    # fields = '__all__'

    def form_valid(self, form):
        new_item = form.save(commit=False)
        new_item.restaurant = self.request.user.userprofile.workplace
        new_item.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


class CreateMenuView(CreateView):
    model = Menu
    form_class = MenuCreateForm

    def form_valid(self, form):
        new_item = form.save(commit=False)
        new_item.restaurant = self.request.user.userprofile.workplace
        new_item.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('server_home')


class ServerAddView(CreateView):
    form_class = UserCreationForm
    model = User
    template_name = 'server/employee_create_form.html'

    def form_valid(self, form, **kwargs):
        new_server = form.save()
        server_restaurant = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        profile = UserProfile.objects.create(
                                             user=new_server,
                                             workplace=server_restaurant,
                                             position='S'
                                             )
        profile.save()
        return super().form_valid(form, **kwargs)

    # def form_invalid(self, form):
    #     print("Your Form Is Invalid sir!")
    #     print(form.errors)
    #     return super().form_invalid(form)

    def get_context_data(self):
        context = super().get_context_data()
        context['user_type'] = 'Server'
        return context

    def get_success_url(self):
        return reverse('index')


class KitchenAddView(CreateView):
    form_class = UserCreationForm
    model = User
    template_name = 'server/employee_create_form.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['user_type'] = 'Kitchen'
        return context

    def form_valid(self, form, **kwargs):
        new_server = form.save()
        server_restaurant = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        profile = UserProfile.objects.create(
                                             user=new_server,
                                             workplace=server_restaurant,
                                             position='K'
                                             )
        profile.save()
        return super().form_valid(form, **kwargs)

    def get_success_url(self):
        return reverse('index')


class UpdateMenuView(UpdateView):
    model = Menu
    form_class = MenuCreateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('menu_detail', kwargs={'pk': self.kwargs['pk']})


class MenuItemDetailView(DetailView):
    model = MenuItem


def mark_table_fulfilled(request, table_id):
    done_table = Table.objects.get(pk=table_id)
    done_table.fulfilled = True
    done_table.save()
    return HttpResponseRedirect(reverse('kitchen'))


class RestaurantUpdateView(UpdateView):
    model = Restaurant
    fields = '__all__'

    def get_object(self):
        return self.request.user.userprofile.workplace

    def get_success_url(self):
        return reverse('index')


class UpdateMenuItemView(UpdateView):
    model = MenuItem
    form_class = MenuItemForm

    def get_success_url(self):
        return reverse('index')
