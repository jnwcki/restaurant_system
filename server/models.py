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
                          variations={'thumbnail': {"width": 100, "height": 100, "crop": True}}
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

    class Meta:
        ordering = ['-started']

    def __str__(self):
        return "Table {} -- {}".format(self.number, self.started)


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
