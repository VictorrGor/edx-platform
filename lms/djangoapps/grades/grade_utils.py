"""
This module contains utility functions for grading.
"""
from datetime import timedelta
from django.utils import timezone
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from .config.waffle import ENFORCE_FREEZE_GRADE_AFTER_COURSE_END, waffle_flags


def are_grades_frozen(course_key):
    """ Returns whether grades are frozen for the given course. """
    if waffle_flags()[ENFORCE_FREEZE_GRADE_AFTER_COURSE_END].is_enabled(course_key):
        course = CourseOverview.get_from_id(course_key)
        if course.end:
            freeze_grade_date = course.end + timedelta(30)
            now = timezone.now()
            return now > freeze_grade_date
    return False
