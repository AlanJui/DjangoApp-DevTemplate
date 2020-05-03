from django import forms

from .models import LogMessage


class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ('message',)   # Note: the trailing comma is required
