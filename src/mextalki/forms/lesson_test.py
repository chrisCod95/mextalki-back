from django import forms

from src.mextalki.models import Answer, LessonTest, Question


class LessonTestForm(forms.Form):
    def __init__(self, test: LessonTest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test: LessonTest = test
        self.questions: [Question] = test.questions.all() if test else []
        self.correct_answered = 0

        counter: int
        question: Question
        for counter, question in enumerate(self.questions):
            answer: Answer
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
