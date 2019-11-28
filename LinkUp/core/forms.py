from django import forms
from django.forms import ModelForm
from .models import Event
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Last Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

class EventForm(ModelForm):
    class Meta:
        model = Event
        widgets = {
            'potential_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
            'potential_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
        }
        fields = ['title', 'description', 'duration', 'potential_start_date', 'potential_end_date']

    def clean(self):
        cleaned_data = super().clean()
        potential_start_date = cleaned_data.get("potential_start_date")
        potential_end_date = cleaned_data.get("potential_end_date")

        if potential_start_date and potential_end_date and potential_start_date > potential_end_date:
            msg = "Potential start date must be larger than potential end date!"
            self.add_error('potential_start_date', msg)
            self.add_error('potential_end_date', msg)

        return self.cleaned_data
