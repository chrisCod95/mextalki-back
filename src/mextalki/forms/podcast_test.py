from django import forms

from src.mextalki.models import PodcastTest, PodcastTestAnswer, PodcastTestQuestion
from src.mextalki.models.lesson_test import Answer


class PodcastTestForm(forms.Form):
    def __init__(self, test: PodcastTest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test: PodcastTest = test
        self.questions: [PodcastTestQuestion] = test.questions.all() if test else []
        self.correct_answered = 0

        counter: int
        question: PodcastTestQuestion
        for counter, question in enumerate(self.questions):
            answer: PodcastTestAnswer
            choices = [(answer.id, answer.answer) for answer in question.answers.all()]
            self.fields['question_%d' % counter] = forms.ChoiceField(
                label=question,
                choices=choices,
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
            )

    def clean(self):
        counter = 0
        field_name = 'question_%d' % counter
        while self.cleaned_data.get(field_name):
            value = self.cleaned_data[field_name]
            question_id = int(field_name.replace('question_', ''))
            question = self.questions[question_id]
            answer = question.answers.get(id=value)
            if answer.correct_answer:
                self.correct_answered += 1
            else:
                self.add_error(
                    field_name,
                    '"{answer}", was wrong.'.format(
                        answer=answer,
                    ),
                )

            counter += 1
            field_name = 'question_%d' % counter
