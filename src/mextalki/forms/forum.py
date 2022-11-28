from django import forms


class CommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Answer this challenge and earn 20 exp points',
            },
        ),
        max_length=500,
        required=True,
    )
