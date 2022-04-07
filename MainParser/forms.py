from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator


class RegisrationForm(UserCreationForm):
    name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'contact-input'})
        self.fields['name'].widget.attrs.update({'class': 'contact-input'})
        self.fields['password1'].widget.attrs.update({'class': 'contact-input', 'onkeyup': 'check();'})
        self.fields['password2'].widget.attrs.update({'class': 'contact-input', 'onkeyup': 'check();'})
