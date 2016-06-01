from django.test import TestCase
from django.core.urlresolvers import reverse

from server.views import LandingView


class LandingViewTest(TestCase):
    def test_hardcoded_url_returns_response(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_landing_view_response(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
