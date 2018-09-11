from django.urls import path, re_path


from .views import (course_list, course_detail, text_detail, quiz_detail,
                    quiz_create, quiz_edit, create_question, edit_question,
                    answer_question, courses_by_teacher, search_courses)

urlpatterns = [
    path('', course_list, name='course_list'),
    re_path(r'by/(?P<teacher>[-\w]+)/$', courses_by_teacher, name='courses_by_teacher'),
    path('<int:pk>', course_detail, name='course_detail'),
    # path('<int:course_pk>/steps/<int:step_pk>', step_detail, name='step_detail'),
    path(r'search/', search_courses, name="search_courses"),
    path('<int:course_pk>/texts/<int:step_pk>', text_detail, name='text_detail'),
    path('<int:course_pk>/quizzes/<int:step_pk>', quiz_detail, name='quiz_detail'),
    path('<int:course_pk>/create_quiz', quiz_create, name='create_quiz'),
    path('<int:course_pk>/edit_quiz/<int:step_pk>', quiz_edit, name='edit_quiz'),
    re_path(r'^(?P<quiz_pk>\d+)/create_question/(?P<question_type>mc|tf)/$',
            create_question, name="create_question"),
    re_path(r'^(?P<quiz_pk>\d+)/edit_question/(?P<question_pk>\d+)/$',
            edit_question, name="edit_question"),
    re_path(r'^(?P<question_pk>\d+)/answer_question/$',
            answer_question, name="answer_question"),
]
