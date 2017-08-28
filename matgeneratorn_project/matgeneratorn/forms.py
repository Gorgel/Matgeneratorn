from django import forms

STATUS_CHOICES = (
    (1, ("1")),
    (2, ("2")),
    (3, ("3")),
    (4, ("4")),
    (5, ("5")),
    (6, ("6")),
    (7, ("7")),
    (8, ("8")),
    (9, ("9")),
    (10, ("10"))
)

class portionsForm(forms.Form):

    status = forms.ChoiceField(choices = STATUS_CHOICES, label="", initial='', widget=forms.Select(), required=True)
