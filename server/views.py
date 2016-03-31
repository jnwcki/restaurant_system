# from django.shortcuts import render
from server.models import UserProfile, Restaurant, Order
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, TemplateView, DetailView, ListView
from server.forms import NewUserCreation


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        context = super(IndexView, self).get_context_data()
        context['user'] = UserProfile.objects.get(user=self.request.user)
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
