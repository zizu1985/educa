from django.core.urlresolvers import reverse, resolve


class TestUrls():

    # Test correct mapping between view and url
    def test_login_url(self):
        path = reverse('login')
        assert resolve(path).view_name == 'login'