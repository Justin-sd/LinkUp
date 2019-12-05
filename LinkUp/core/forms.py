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
            'title': forms.TextInput(attrs={
                'type': 'text',
                'class': 'input has-background-light',
                'placeholder': 'Please enter a title for your event!'
                }),
            'description': forms.Textarea(attrs={
                'type': 'textarea',
                'class': 'textarea has-background-light',
                'rows': '3',
                'placeholder':  'Please enter a event description! \nThis can be '
                                'anything from what the event is for, where it will '
                                'be located, etc. \nThank you!'
                }),
            'duration': forms.NumberInput(attrs={'type': 'number',
                                                 'class': 'input has-background-light',
                                                 'placeholder': 'Duration'}),
            'potential_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'input has-background-light'}),
            'potential_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'input has-background-light'}),
            'no_earlier_than': forms.NumberInput(attrs={'type': 'time', 'class': 'input has-background-light',
                                                        'placeholder': 'No earlier than'}),
            'no_later_than': forms.NumberInput(attrs={'type': 'time', 'class': 'input has-background-light',
                                                      'placeholder': 'No later than'}),
        }
        fields = ['title',
                  'description',
                  'duration',
                  'potential_start_date',
                  'potential_end_date',
                  'no_earlier_than',
                  'no_later_than']

    def clean(self):
        cleaned_data = super().clean()
        potential_start_date = cleaned_data.get("potential_start_date")
        potential_end_date = cleaned_data.get("potential_end_date")

        if potential_start_date and potential_end_date and potential_start_date > potential_end_date:
            msg = "Potential start date must be larger than potential end date!"
            self.add_error('potential_start_date', msg)
            self.add_error('potential_end_date', msg)

        return self.cleaned_data
