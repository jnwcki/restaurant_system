from django.shortcuts import render
from django.views.generic import TemplateView
from server.models import UserProfile, Restaurant, Order
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, ListView, DetailView, View
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
        current_server = Server.objects.get(user_profile=self.request.user.userprofile)
        current_restaurant = Restaurant.objects.get(server__user_profile=current_server.user_profile)
        context['server'] = current_server
        context['restaurant'] = current_restaurant
        context['table_list'] = Table.objects.filter(restaurant=current_restaurant)
        return context


# class TableView(DetailView):
#     model = Table
