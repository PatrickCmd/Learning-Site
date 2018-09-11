from django import template
from django.utils.safestring import mark_safe

import markdown2

from courses.models import Course

register = template.Library()


@register.simple_tag
def newest_course():
    """
    Returns the newest course added in the Library
    """
    course = Course.objects.filter(published=True).latest('created_at')
    return course


@register.inclusion_tag("courses/course_nav.html")
def nav_courses_list():
    """
    Returns a dictionary of courses to display as a nav
    """
    # courses = Course.objects.all()[:5]
    # courses = Course.objects.filter(published=True)[:5]
    courses = Course.objects.filter(
        published=True).order_by('-created_at').values('id', 'title')[:5]
    cxt = {
        "courses": courses,
    }
    return cxt


@register.filter('time_estimate')
def time_estimate(word_count):
    """
    Estimate the number of minutes it would take to complete a course step
    based on the word count
    """
    minutes = round(word_count/20)
    return minutes


@register.filter('markdown_to_html')
def markdown_to_html(markdown_text):
    """Converts markdown to HTML"""
    html_body = markdown2.markdown(markdown_text)
    return mark_safe(html_body)
