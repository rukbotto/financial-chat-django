from django import forms

from chat.models import Message


class MessageForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'data-ref': 'message-input',
            'rows': 1
        })
    )

    class Meta:
        model = Message
        fields = ['content']
