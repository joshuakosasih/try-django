from django import forms

class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "id": "f-author",
            "class": "form-control",
            "placeholder": "Your Name"
        })
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            "id": "f-body",
            "class": "form-control",
            "placeholder": "Leave a comment!"
        })
    )

