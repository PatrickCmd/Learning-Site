from django.contrib import admin

from .models import Course, Text, Quiz, Question, MultipleChoiceQuestion, TrueFalseQuestion, Answer


# class TextInline(admin.TabularInline):
#     model  =Text


# class CourseAdmin(admin.ModelAdmin):
#     inlines = [
#         TextInline,
#     ]


admin.site.register(Course)
admin.site.register(Text)
admin.site.register(Quiz)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(TrueFalseQuestion)
admin.site.register(Answer)
