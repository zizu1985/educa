from django.test import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, AnonymousUser
from mixer.backend.django import mixer
from courses.views import ManageCourseListView
import pytest
from django.core.management import call_command


@pytest.mark.django_db
class TestView:

    def test_course_list_view(self):
        path = reverse('manage_course_list')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response_view = ManageCourseListView.as_view()
        response = response_view(request)
        assert response.status_code == 200

    def test_course_list_view_unauthorized(self):
        path = reverse('manage_course_list')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response_view = ManageCourseListView.as_view()
        response = response_view(request)
        #print(response.url)
        assert 'accounts/login' in response.url
