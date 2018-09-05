from django.urls import path


from .views import course_list, course_detail, step_detail

urlpatterns = [
    path('', course_list, name='course_list'),
    path('<int:pk>', course_detail, name='course_detail'),
    path('<int:course_pk>/steps/<int:step_pk>', step_detail, name='step_detail'),
]
