from django import forms

from . models import Quiz, MultipleChoiceQuestion, TrueFalseQuestion, Answer


class QuizForm(forms.ModelForm):
    
    class Meta:
        model = Quiz
        fields = [
            'title',
            'order',
            'description',
            'total_questions'
        ]


class TrueFalseQuestionForm(forms.ModelForm):

    class Meta:
        model = TrueFalseQuestion
        fields = [
            'order',
            'prompt'
        ]


class MultipleChoiceQuestionForm(forms.ModelForm):

    class Meta:
        model = MultipleChoiceQuestion
        fields = [
            'order',
            'prompt',
            'shuffle_answer'
        ]


class AnswerQuestionForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = [
            'order',
            'text',
            'correct'
        ]
