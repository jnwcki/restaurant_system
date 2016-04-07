# from django.shortcuts import render
from server.models import UserProfile, Restaurant, Order, MenuItem, Menu, Table
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, ListView, UpdateView
from server.forms import NewUserCreation, ServerCreateForm, CreateOrderForm
from django.forms import inlineformset_factory
# from django.forms.widgets import CheckboxSelectMultiple
from django.shortcuts import render
# from extra_views import CreateWithInlinesView, ModelFormSetView
from django.http import HttpResponseRedirect


class LandingView(TemplateView):
    template_name = 'landing.html'


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        context = super(IndexView, self).get_context_data()
        context['user'] = self.request.user
        employee_list = UserProfile.objects.filter(workplace=self.request.user.userprofile.workplace)
        context['servers'] = employee_list.filter(position='S')
        context['kitchen'] = employee_list.filter(position='K')
        return context


class UserCreateView(CreateView):
    model = User
    form_class = NewUserCreation

    def form_valid(self, form):
        user_object = form.save()
        new_restaurant = Restaurant.objects.create(
                                                    name=form.cleaned_data["restaurant_name"],
                                                    number_of_tables=form.cleaned_data['number_of_tables'],
                                                    )
        profile = UserProfile.objects.create(
                                             user=user_object,
                                             name=form.cleaned_data["first_name"],
                                             workplace=new_restaurant
                                             )
        profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('login')


class ServerHomeView(TemplateView):
    template_name = 'server_home.html'

    def get_context_data(self):
        context = super(ServerHomeView, self).get_context_data()
        current_server = UserProfile.objects.get(user=self.request.user)
        if current_server.position != 'K':
            current_restaurant = current_server.workplace
            bound_table_list = Table.objects.filter(server__workplace=current_restaurant, fulfilled=False)
            all_tables_list = [x for x in range(current_restaurant.number_of_tables)]
            bound_table_numbers = bound_table_list.values_list('number', flat=True)
            unbound_tables = [x for x in all_tables_list if x not in bound_table_numbers]

            context['restaurant'] = current_restaurant
            context['server'] = current_server
            # context['order_list'] = Order.objects.filter(server=self.request.user.userprofile)
            context['menus'] = Menu.objects.all()
            context['bound_tables'] = bound_table_list
            context['unbound_tables'] = unbound_tables
        else:
            return reverse('kitchen')
        return context


def FunctionBasedCreateOrder(request, table_number):
    server = request.user.userprofile

    OrderFormSet = inlineformset_factory(Table, Order, form=CreateOrderForm)

    if request.method == 'POST':
            new_table = Table.objects.create(server=server, number=table_number)

            order_form_set = OrderFormSet(request.POST, instance=new_table)

            if order_form_set.is_valid():
                for order in order_form_set:
                    order.save()
                # Order.objects.bulk_create(order_form_set)

            return HttpResponseRedirect(reverse('server_home'))
    else:
        order_form_set = OrderFormSet()
        return render(request, 'server/order_form.html', {'formset': order_form_set})


# class UpdateOrder(ModelFormSetView):
#     template_name = 'server/update_order_form.html'
#     model = Table
#
    # def get_queryset(self):
    #     table_id = self.kwargs['pk']
    #     return super().get_queryset().filter(pk=table_id)


def FunctionBasedUpdateOrder(request, pk):
    OrderFormSet = inlineformset_factory(Table, Order, form=CreateOrderForm)
    working_table = Table.objects.get(pk=pk)

    if request.method == 'POST':
        update_order_form_set = OrderFormSet(request.POST, instance=working_table)
        if update_order_form_set.is_valid():
            update_order_form_set.save()
            # Order.objects.filter(table=working_table).delete()
            # Order.objects.bulk_create(update_order_form_set)
        return HttpResponseRedirect(reverse('server_home'))
    else:
        update_order_form_set = OrderFormSet(instance=working_table)
        return render(request, 'server/update_order_form.html', {'formset': update_order_form_set})

# class OrderCreateView(CreateWithInlinesView):
#     form_class = CreateOrderForm
#     template_name = 'server/order_form.html'
#     success_url = '/server/home/'
#     extra = 1
#     model = Table
#     inline_model = Order
#
#     def get_extra_form_kwargs(self):
#         kwargs = super(OrderCreateView, self).get_extra_form_kwargs()
#         kwargs.update({
#             'server': self.request.user.userprofile,
#
#         })
#         return kwargs
#
#     def forms_valid(self, form, inlines):
#         form.instance.server = self.request.user.userprofile
#         return super(OrderCreateView, self).forms_valid(form, inlines)
#
#     def formset_valid(self, formset):
#         # print(formset)
#         for new_order in formset:
#             # if new_order.is_valid and not new_order.empty_permitted:
#             new_order.save(commit=False)
#             # print(self.request.user.userprofile)
#             new_order.server = UserProfile.objects.get(user=self.request.user)
#             new_order.seat_number = 1
#             new_order.table_number = 1
#             new_order.save()
#         return super(OrderCreateView, self).formset_valid(formset)


class OrderDetailView(DetailView):
    model = Order


class KitchenListView(ListView):
    model = Table

    # def get_context_data(self):
    #     context = super(KitchenListView, self).get_context_data()
    #
    #     return context


class MenuDetailView(DetailView):
    model = Menu


class AddMenuItemView(CreateView):
    model = MenuItem
    fields = ['name', 'description', 'price', 'photo']

    def form_valid(self, form):
        new_item = form.save(commit=False)
        new_item.restaurant = self.request.user.userprofile.workplace
        new_item.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('server_home')


class CreateMenuView(CreateView):
    model = Menu
    fields = ['name', 'item']

    def form_valid(self, form):
        new_item = form.save(commit=False)
        new_item.restaurant = self.request.user.userprofile.workplace
        new_item.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('server_home')


class ServerAddView(CreateView):
    form_class = ServerCreateForm
    model = User
    template_name = 'server/employee_create_form.html'

    def form_valid(self, form, **kwargs):
        new_server = form.save()
        server_restaurant = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        profile = UserProfile.objects.create(
                                             user=new_server,
                                             name=form.cleaned_data["name"],
                                             workplace=server_restaurant,
                                             position='S'
                                             )
        profile.save()
        return super().form_valid(form, **kwargs)

    def get_success_url(self):
        return reverse('index')


class KitchenAddView(CreateView):
    form_class = ServerCreateForm
    model = User
    template_name = 'server/employee_create_form.html'

    def form_valid(self, form, **kwargs):
        new_server = form.save()
        server_restaurant = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        profile = UserProfile.objects.create(
                                             user=new_server,
                                             name=form.cleaned_data["name"],
                                             workplace=server_restaurant,
                                             position='K'
                                             )
        profile.save()
        return super().form_valid(form, **kwargs)

    def get_success_url(self):
        return reverse('index')


class UpdateMenuView(UpdateView):
    model = Menu
    fields = ['name', 'item']

    def get_success_url(self, **kwargs):
        return reverse_lazy('menu_detail', kwargs={'pk': self.kwargs['pk']})


class MenuItemDetailView(DetailView):
    model = MenuItem


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['seat_number', 'table_number', 'items']


class TableStartView(TemplateView):
    template_name = 'server/table_start_view.html'


def mark_table_fulfilled(request, table_id):
    done_table = Table.objects.get(pk=table_id)
    done_table.fulfilled = True
    done_table.save()
    return HttpResponseRedirect(reverse('kitchen'))
