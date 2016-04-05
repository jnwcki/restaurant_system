from django.test import TestCase
from server.models import MenuItem
from server.forms import CreateOrderForm


# class MenuItemTests(TestCase):
#
#     def test_if_this_works(self):
#         self.fail("x")


class FormTests(TestCase):
    def test_validation(self):
        form_data = {
            'items': 'X' * 300,
        }

        form = CreateOrderForm(data=form_data)
        self.assertTrue(form.is_valid())
