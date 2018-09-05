from django.shortcuts import render, get_object_or_404

from .models import Course, Step


def course_list(request):
    courses = Course.objects.all()
    email = 'pwalukagga@gmail.com'
    ctx = {
        "courses": courses,
        "email": email,
    }
    return render(request, 'courses/course_list.html', ctx)


def course_detail(request, pk):
    # course = Course.objects.get(pk=pk)
    course = get_object_or_404(Course, pk=pk)
    ctx = {
        "course": course,
    }
    return render(request, 'courses/course_detail.html', ctx)


def step_detail(request, course_pk, step_pk):
    step = get_object_or_404(Step, course_id=course_pk, pk=step_pk)
    ctx = {
        "step": step,
    }
    return render(request, 'courses/step_detail.html', ctx)
