from django.db import models
from stdimage.models import StdImageField

POSITION_CHOICES = [('M', 'Manager'), ('S', 'Server'), ('K', 'Kitchen')]
ITEM_CHOICES = [
                ('N', 'Non-Alcoholic Beverage'),
                ('A', 'Appetizer'),
                ('E', 'Entree'),
                ('D', 'Dessert'),
                ('B', 'Alcohol')
                ]


class Restaurant(models.Model):
    name = models.CharField(max_length=255, default="Unnamed Restaurant")
    number_of_tables = models.IntegerField(default=1)
    tax_percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    current_menu = models.ForeignKey('Menu', related_name='current_working_menu', null=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User')
    position = models.CharField(max_length=255, choices=POSITION_CHOICES)
    workplace = models.ForeignKey(Restaurant)

    def __str__(self):
        return self.user.username


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    photo = StdImageField(upload_to="uploads",
                          default="uploads/default.png",
                          variations={'thumbnail': {"width": 100, "height": 100}}
                          )
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    item_type = models.CharField(max_length=1, choices=ITEM_CHOICES, default='E')

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length=100)
    item = models.ManyToManyField(MenuItem)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Table(models.Model):
    server = models.ForeignKey(UserProfile)
    number = models.IntegerField()
    started = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    number_of_seats = models.IntegerField(default=1)

    class Meta:
        ordering = ['-started']

    def __str__(self):
        return "Table {} -- {}".format(self.number, self.started)

    def total_ticket_price(self):
        good_items = self.ordereditem_set.filter(canceled=False, sent=True)
        counter = 0
        for item in good_items:
            counter += item.item.price
        return counter

    def price_category_totals(self):
        category_totals = {'N': 0, 'A': 0, 'E': 0, 'D': 0, 'B': 0}
        sold_items = self.ordereditem_set.filter(canceled=False, sent=True)
        for item in sold_items:
            if item.item.item_type == 'N':
                category_totals['N'] += item.item.price
            elif item.item.item_type == 'A':
                category_totals['A'] += item.item.price
            elif item.item.item_type == 'E':
                category_totals['E'] += item.item.price
            elif item.item.item_type == 'D':
                category_totals['D'] += item.item.price
            elif item.item.item_type == 'B':
                category_totals['B'] += item.item.price
        # print(category_totals)
        return category_totals

    def price_with_tax(self):
        if self.server.workplace.tax_percentage:
            pay_this_amount = self.total_ticket_price * self.server.workplace.tax_percentage / 100
        else:
            pay_this_amount = self.total_ticket_price
        return pay_this_amount

    def stripe_total(self):
        good_items = self.ordereditem_set.filter(canceled=False, sent=True)
        counter = 0
        for item in good_items:
            counter += item.item.price

        if self.server.workplace.tax_percentage:
            pay_this_amount = counter * self.server.workplace.tax_percentage
        else:
            pay_this_amount = counter
            total = pay_this_amount * 100
        return total


class OrderedItem(models.Model):
    table = models.ForeignKey(Table)
    item = models.ForeignKey(MenuItem)
    seat_number = models.IntegerField(null=True, blank=True)
    special_instructions = models.CharField(max_length=255, blank=True, null=True)
    sent = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)

    class Meta:
        ordering = ['seat_number']

    def __str__(self):
        return str(self.pk)


class ApiKey(models.Model):
    provider = models.CharField(max_length=50)
    public_key = models.TextField()
    private_key = models.TextField()
