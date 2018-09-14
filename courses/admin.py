from django.contrib import admin

from datetime import date

from .models import Course, Text, Quiz, Question, MultipleChoiceQuestion, TrueFalseQuestion, Answer


def make_published(modeladmin, request, queryset):
    queryset.update(status='p', published=True)


def make_in_review(modeladmin, request, queryset):
    queryset.update(status='r', published=False)


def make_in_progress(modeladmin, request, queryset):
    queryset.update(status='i', published=False)


make_published.short_description = "Mark selected courses as Published"
make_in_progress.short_description = "Mark selected courses as in-progress"
make_in_review.short_description = "Mark selected courses as in-review"


# custom filter to return objects in given year
def get_queryset(query_set, year):
    return query_set.filter(created_at__gte=date(year, 1, 1),
                            created_at__lte=date(year, 12, 31))


class YearListFilter(admin.SimpleListFilter):
    title = 'year created'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        return (
            ('2015', '2015'),
            ('2016', '2016'),
            ('2017', '2017'),
            ('2018', '2018')
        )
    
    def queryset(self, request, queryset):
        # if self.value() == '2015':
        #     return get_queryset(queryset, 2015)
        # elif self.value() == '2016':
        #     return get_queryset(queryset, 2016)
        # elif self.value() == '2017':
        #     return get_queryset(queryset, 2017)
        # elif self.value() == '2018':
        #     return get_queryset(queryset, 2018)
        if self.value():
            return queryset.filter(created_at__gte=date(int(self.value()), 1, 1),
                                   created_at__lte=date(int(self.value()), 12, 31))


class TopicListFilter(admin.SimpleListFilter):
    title = 'topic'
    parameter_name = 'topic'

    def lookups(self, request, model_admin):
        return (
            ('python', 'Python'),
            ('ruby', 'Ruby'),
            ('java', 'Java'),
            ('android', 'Android'),
            ('sql', 'SQL')
        )
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                title__contains=self.value()
            )


class TextInline(admin.TabularInline):
    model  = Text


class QuizInline(admin.TabularInline):
    model = Quiz


class AnswerInline(admin.TabularInline):
    model = Answer


class CourseAdmin(admin.ModelAdmin):
    fields = ('teacher', 'title', 'description', 'subject')
    inlines = [TextInline, QuizInline]
    search_fields = ['title', 'description']
    list_filter = ['created_at', YearListFilter, TopicListFilter]
    list_display = ['title', 'subject', 'published', 'created_at', 'time_to_complete', 'status']
    list_editable = ['status']

    actions = [
        make_published,
        make_in_progress,
        make_in_review
    ]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline,]
    search_fields = ['prompt']
    list_display = ['prompt', 'quiz', 'order']
    list_editable = ['quiz', 'order']


class QuizAdmin(admin.ModelAdmin):
    model = Quiz
    fields = ('course', 'title', 'description', 'order', 'total_questions')
    search_fields = ['title', 'description']
    list_display = ['title', 'course', 'number_correct_needed', 'total_questions', 'order']
    list_editable = ['total_questions', 'order']


class TextAdmin(admin.ModelAdmin):
    model = Quiz
    # fields = ('course', 'title', 'description', 'order', 'content')
    fieldsets = (
        (None, {
            'fields': ('course', ('title', 'order'), 'description')
        }),
        ('Add content', {
            'fields': ('content',),
            'classes': ('collapse',)
        })
    )
    search_fields = ['title', 'description', 'content']


admin.site.register(Course, CourseAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(MultipleChoiceQuestion, QuestionAdmin)
admin.site.register(TrueFalseQuestion, QuestionAdmin)
admin.site.register(Answer)
