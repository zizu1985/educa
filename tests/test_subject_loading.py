from django.test import TestCase
from courses.models import Subject


class SubjectTestLoading(TestCase):
    fixtures = ['subject.json','subject']
    all_subjects = None

    def test_number_of_loaded(self):
        self.assertEquals(Subject.objects.count(),4)
