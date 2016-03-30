from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    user_profile = models.ForeignKey(UserProfile)


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    photo = models.ImageField(upload_to="uploads", default="uploads/default.png")
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Server(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='server_model')
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length=100)
    item = models.ManyToManyField(MenuItem)

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(MenuItem)
    seat = models.IntegerField()


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    number = models.IntegerField()
    seats = models.IntegerField()
    customer_order = models.ForeignKey(Order)

    def __str__(self):
        return str(self.number)
