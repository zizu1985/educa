from django.test import TestCase
from courses.models import Subject


class SubjectTest(TestCase):

    def setUp(self):
        Subject.objects.create(title="Advanced SQL")

    def test_subject_has_name(self):
        subject = Subject.objects.get(title="Advanced SQL")
        self.assertEquals(subject.title,"Advanced SQL")
        #self.assertEquals(subject.title, "RRR")