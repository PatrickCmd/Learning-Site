from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.db.models import Count, Q, Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Course, Text, Quiz, Question
from .forms import QuizForm, TrueFalseQuestionForm, MultipleChoiceQuestionForm, AnswerQuestionForm


def course_list(request):
    # courses = Course.objects.all()
    courses = Course.objects.filter(
        published=True
    ).annotate(total_steps=Count(
        'text', distinct=True)+Count('quiz', distinct=True)
    )
    total = courses.aggregate(total=Sum('total_steps'))
    email = 'pwalukagga@gmail.com'
    ctx = {
        "courses": courses,
        "total": total,
        "email": email,
    }
    return render(request, 'courses/course_list.html', ctx)


def courses_by_teacher(request, teacher):
    courses = Course.objects.filter(teacher__username=teacher, published=True)
    email = 'pwalukagga@gmail.com'
    ctx = {
        "courses": courses,
        "email": email,
    }
    return render(request, 'courses/course_list.html', ctx)


def course_detail(request, pk):
    # course = Course.objects.get(pk=pk)
    # course = get_object_or_404(Course, pk=pk, published=True)
    try:
        course = Course.objects.prefetch_related(
            'quiz_set', 'text_set', 'quiz_set__question_set'
        ).get(pk=pk, published=True)
    except Course.DoesNotExist:
        raise Http404
    else:
        steps = sorted(chain(course.text_set.all(), course.quiz_set.all()),
                    key=lambda step: step.order)
    ctx = {
        "course": course,
        "steps": steps,
    }
    return render(request, 'courses/course_detail.html', ctx)


def search_courses(request):
    term = request.GET.get('q')
    # courses = Course.objects.filter(title__icontains=term, published=True)
    courses = Course.objects.filter(Q(title__icontains=term) |
                                    Q(description__icontains=term),
                                    published=True)
    email = 'pwalukagga@gmail.com'
    ctx = {
        "courses": courses,
        "email": email,
    }
    return render(request, 'courses/course_list.html', ctx)


# def step_detail(request, course_pk, step_pk):
#     step = get_object_or_404(Step, course_id=course_pk, pk=step_pk)
#     ctx = {
#         "step": step,
#     }
#     return render(request, 'courses/step_detail.html', ctx)


def text_detail(request, course_pk, step_pk):
    step = get_object_or_404(Text, course_id=course_pk, pk=step_pk,
                             course__published=True)
    ctx = {
        "step": step,
    }
    return render(request, 'courses/text_detail.html', ctx)


def quiz_detail(request, course_pk, step_pk):
    # step = get_object_or_404(Quiz, course_id=course_pk, pk=step_pk,
    #                          course__published=True)
    try:
        step = Quiz.objects.select_related(
            'course'
        ).prefetch_related(
            'question_set',
            'question_set__answer_set',
        ).get(
            course_id=course_pk, pk=step_pk, course__published=True
        )
    except Quiz.DoesNotExist:
        raise Http404
    else:
        ctx = {
            "step": step,
        }
        return render(request, 'courses/quiz_detail.html', ctx)


@login_required
def quiz_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk, course__published=True)
    form = QuizForm()

    if request.method == "POST":
        form = QuizForm(request.POST)
        
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.add_message(request, messages.SUCCESS,
                         "Quiz to the question has been created!")
            return redirect(reverse('courses:quiz_detail', args=[quiz.course.pk, quiz.pk]))
    cxt = {
        "form": form,
        "course": course,
    }
    return render(request, "courses/quiz_form.html", cxt)


@login_required
def quiz_edit(request, course_pk, step_pk):
    quiz = get_object_or_404(Quiz, pk=step_pk, course_id=course_pk,
                             course__published=True)
    form = QuizForm(instance=quiz)

    if request.method=="POST":
        form = QuizForm(instance=quiz, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Quiz has been updated")
            return redirect(reverse('courses:edit_quiz', args=[quiz.course.pk, quiz.pk]))

    cxt = {
        "form": form,
        "course": quiz.course,
    }
    return render(request, "courses/quiz_form.html", cxt)


@login_required
def create_question(request, quiz_pk, question_type):
    quiz = get_object_or_404(Quiz, pk=quiz_pk, course__published=True)
    
    if question_type == "tf":
        form_class = TrueFalseQuestionForm
    else:
        form_class = MultipleChoiceQuestionForm
    
    form = form_class()

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, "Question added!")
            # return redirect(reverse(quiz.get_absolute_url()))
            return HttpResponseRedirect(quiz.get_absolute_url())
    cxt = {
        "quiz": quiz,
        "form": form,
    }
    return render(request, "courses/question_form.html", cxt)


@login_required
def edit_question(request, question_pk, quiz_pk):
    question = get_object_or_404(Question, pk=question_pk, quiz_id=quiz_pk)

    if hasattr(question, 'truefalsequestion'):
        question = question.truefalsequestion
        form_class = TrueFalseQuestionForm
    else:
        question = question.multiplechoicequestion
        form_class = MultipleChoiceQuestionForm
    form = form_class(instance=question)

    if request.method == "POST":
        form = form_class(instance=question, data=request.POST)
        form.save()
        messages.success(request, "Question has been updated")
        return HttpResponseRedirect(question.quiz.get_absolute_url())
    
    cxt = {
        "form": form,
        "quiz": question.quiz,
    }
    return render(request, "courses/question_form.html", cxt)


@login_required
def answer_question(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    form = AnswerQuestionForm()

    if request.method == "POST":
        form = AnswerQuestionForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            messages.success(request, "Answer added!")
            return HttpResponseRedirect(question.get_absolute_url())
    cxt = {
        "form": form,
        "question": question
    }
    return render(request, "courses/answer_form.html", cxt)
