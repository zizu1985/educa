from courses.models import Subject
from mixer.backend.django import mixer
import pytest
from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'subject.json')


# marker used to ensure database access is setup for pytest tests
@pytest.mark.django_db
class TestModule:

    def test_subject_is_upper(self):
        # Not optiomal
        #subject = Subject.objects.create(title='PARTITIONING')
        subject = mixer.blend('courses.Subject',title='PARTITIONING')
        assert subject.is_correct_subject == True

    def test_subject_is_not_upper(self):
        subject = mixer.blend('courses.Subject', title='PARTITIONINg')
        assert subject.is_correct_subject == False

    @pytest.mark.usefixtures("django_db_setup")
    def test_number_of_loaded(self):
        assert Subject.objects.count() == 4

    @pytest.mark.usefixtures("django_db_setup")
    def test_number_of_loaded_wrong(self):
        assert Subject.objects.count() != 5