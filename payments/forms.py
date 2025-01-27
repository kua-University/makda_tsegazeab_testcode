from django import forms
from courses.models import Course


class PaymentForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=True, label="Select Course")
