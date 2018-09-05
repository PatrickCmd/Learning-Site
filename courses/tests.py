from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Course, Step


class CourseModelTests(TestCase):

    def setUp(self):
        self.course=Course.objects.create(
            title="Introduction to django",
            description="Django urls and templates"
        )

    def test_course_creation(self):
        course = Course.objects.create(
            title="Python Regular Expressions",
            description="How to user regex functions"
        )
        now = timezone.now()
        self.assertLess(course.created_at, now)
        self.assertEqual(course.title, "Python Regular Expressions")
    
    def test_step_creation(self):
        course = Course.objects.create(
            title="Python Regular Expressions",
            description="How to user regex functions"
        )
        step = Step.objects.create(
            title="Regex Overview",
            description = "An overview of regular expressions",
            content = "How regex expressions are used and work",
            course = self.course
        )
        self.assertEqual(step.course_id, self.course.pk)
        self.assertIn("regex expressions", step.content)
        self.assertIn(step, self.course.step_set.all())


class CourseViewTests(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            title="Python Regular Expressions",
            description="How to user regex functions"
        )
        self.course2=Course.objects.create(
            title="Introduction to django",
            description="Django urls and templates"
        )
        self.step = Step.objects.create(
            title="Regex Overview",
            description = "An overview of regular expressions",
            content = "How regex expressions are used and work",
            course = self.course
        )
    
    def test_course_list(self):
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.course, response.context['courses'])
        self.assertIn(self.course, response.context['courses'])
    
    def test_course_detail(self):
        response = self.client.get(reverse('courses:course_detail',
                                   kwargs={'pk': self.course2.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.course2.title, response.context['course'].title)
    
    def test_course_detail_steps(self):
        response = self.client.get(reverse('courses:course_detail',
                                   kwargs={'pk': self.course.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.step, response.context['course'].step_set.all())
    
    def test_step_detail(self):
        response = self.client.get(reverse('courses:step_detail',
                                   kwargs={'course_pk': self.course.pk,
                                   'step_pk': self.step.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.step.title, response.context['step'].title)
    
    def test_course_list_template_used(self):
        response = self.client.get(reverse('courses:course_list'))
        self.assertTemplateUsed(response, 'courses/course_list.html')
        self.assertContains(response, self.course.title)
    
    def test_course_detail_template_used(self):
        response = self.client.get(reverse('courses:course_detail',
                                   kwargs={'pk': self.course2.pk}))
        self.assertTemplateUsed(response, 'courses/course_detail.html')
        self.assertContains(response, self.course2.title)
    
    def test_step_detail_template_used(self):
        response = self.client.get(reverse('courses:step_detail',
                                   kwargs={'course_pk': self.course.pk,
                                   'step_pk': self.step.pk}))
        self.assertTemplateUsed(response, 'courses/step_detail.html')
        self.assertContains(response, self.step.title)
