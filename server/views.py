# from django.shortcuts import render
from server.models import UserProfile, Restaurant, Order, MenuItem, Menu
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, ListView, UpdateView
from server.forms import NewUserCreation, ServerCreateForm


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


class OrderCreateView(CreateView):
    model = Order
    fields = ['seat_number', 'table_number', 'items']

    def form_valid(self, form):
        new_order = form.save(commit=False)
        new_order.server = self.request.user.userprofile
        new_order.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('server_home')


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
