"""
Unit tests for ProgramEnrollment models.
"""
from __future__ import unicode_literals

from uuid import uuid4

from django.test import TestCase

from lms.djangoapps.program_enrollments.models import ProgramEnrollment, User
from student.tests.factories import UserFactory


class ProgramEnrollmentModelTests(TestCase):
    """
    Tests for the ProgramEnrollment model.
    """
    def setUp(self):
        """
        Set up the test data used in the specific tests
        """
        super(ProgramEnrollmentModelTests, self).setUp()
        self.user = UserFactory.create()
        self.enrollment = ProgramEnrollment.objects.create(
            user=self.user,
            email='foo@bar.com',
            external_user_key='abc',
            program_uuid=uuid4(),
            curriculum_uuid=uuid4(),
            status='enrolled'
        )


    def test_user_retirement(self):
        """
        Test that the email address and external_user_key are
        successfully retired for a user's program enrollments and history.
        """
        new_status = 'withdrawn'

        self.enrollment.status = new_status
        self.enrollment.save()

        # Ensure that all the records had values for email and external_user_key
        self.assertEquals(self.enrollment.email, 'foo@bar.com')
        self.assertEquals(self.enrollment.external_user_key, 'abc')

        for record in self.enrollment.historical_records.all():
            self.assertEquals(record.email, 'foo@bar.com')
            self.assertEquals(record.external_user_key, 'abc')

        ProgramEnrollment.retire_user(self.user.id)
        self.enrollment.refresh_from_db()

        # Ensure those values are retired
        self.assertEquals(self.enrollment.email, None)
        self.assertEquals(self.enrollment.external_user_key, None)

        for record in self.enrollment.historical_records.all():
            self.assertEquals(record.email, None)
            self.assertEquals(record.external_user_key, None)
