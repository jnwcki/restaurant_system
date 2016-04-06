# from django.shortcuts import render
from server.models import UserProfile, Restaurant, Order, MenuItem, Menu
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, ListView, UpdateView
from server.forms import NewUserCreation, ServerCreateForm, CreateOrderForm
# from django.forms import formset_factory
# from django.forms.widgets import CheckboxSelectMultiple
# from django.shortcuts import render
from extra_views import FormSetView, ModelFormSetView


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
        new_restaurant = Restaurant.objects.create(name=form.cleaned_data["restaurant_name"])
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
            context['restaurant'] = current_server.workplace
            context['server'] = current_server
            context['order_list'] = Order.objects.filter(server=self.request.user.userprofile)
            context['menus'] = Menu.objects.all()
        else:
            return reverse('kitchen')
        return context

#
# def form_test(request):
#     context = {'formset': OrderFormSet()}
#
#     if request.method == 'POST':
#         post_formset = OrderFormSet(request.POST)
#         if post_formset.is_valid():
#             for post_form in post_formset:
#                 pass
#     return render(request, 'server/order_form.html', context)


class OrderCreateView(FormSetView):
    form_class = CreateOrderForm
    template_name = 'server/order_form.html'
    success_url = '/server/home/'
    extra = 1
    model = Order

    def get_extra_form_kwargs(self):
        kwargs = super(OrderCreateView, self).get_extra_form_kwargs()
        kwargs.update({
            'server': self.request.user.userprofile,
        })
        return kwargs

    def forms_valid(self, form, inlines):
        form.instance.server = self.request.user.userprofile
        return super(OrderCreateView, self).forms_valid(form, inlines)

    def formset_valid(self, formset):
        # print(formset)
        for new_order in formset:
            # if new_order.is_valid and not new_order.empty_permitted:
            new_order.save(commit=False)
            # print(self.request.user.userprofile)
            new_order.server = UserProfile.objects.get(user=self.request.user)
            new_order.seat_number = 1
            new_order.table_number = 1
            new_order.save()
        return super(OrderCreateView, self).formset_valid(formset)

# class OrderCreateView(CreateView):
#     form_class = CreateOrderForm
#     model = Order
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # form = self.form_class()
#         # items = MenuItem.objects.all().values_list("pk", "name")
#         # form.fields["items"].choices = items
#         # context['form'] = form
#         # print(form)
#         if self.request.POST:
#             context['formset'] = OrderFormSet(self.request.POST)
#         else:
#             context['formset'] = OrderFormSet()
#         return context
#
#     def form_invalid(self, formset):
#         print(formset.errors)
#         return super().form_invalid(formset.errors)
#         #return reverse('order_create_view')
#
#     def form_valid(self, form):
#         new_order = form.save(commit=False)
#         new_order.server = self.request.user.userprofile
#         new_order.seat_number = 1
#         new_order.table_number = 1
#
#         new_order.save()
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse('server_home')
#


class OrderDetailView(DetailView):
    model = Order


class KitchenListView(ListView):
    model = Order

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
