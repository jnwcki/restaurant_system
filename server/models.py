from django.db import models

POSITION_CHOICES = [('M', 'Manager'), ('S', 'Server'), ('K', 'Kitchen')]


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    number_of_tables = models.IntegerField(default=1)

    def __str__(self):
        return "{}".format(self.name)


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User')
    # name = models.CharField(max_length=100, default='default_username')
    position = models.CharField(max_length=255, choices=POSITION_CHOICES)
    workplace = models.ForeignKey(Restaurant)


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    photo = models.ImageField(upload_to="uploads", default="uploads/default.png")
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

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

    class Meta:
        ordering = ['-started']

    def __str__(self):
        return "Table {} {}".format(self.number, self.started)


class Seat(models.Model):
    table = models.ForeignKey(Table)
    items = models.ManyToManyField(MenuItem, through='OrderItems')
    seat_number = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.pk)


class OrderItems(models.Model):
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    special_instructions = models.CharField(max_length=255, null=True, blank=True)
