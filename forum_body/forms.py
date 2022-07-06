from django import forms
from .models import Messages, Topic, Discuss

class MessageForm(forms.ModelForm):
    """Форма добавления сообщения"""

    class Meta:
        model = Messages
        fields = ['owner', 'text']
        labels = {'owner': '', 'text':''}
        widgets = {
                'owner': forms.HiddenInput(),
                'text': forms.Textarea(attrs={
                    'cols':120,
                    'maxlength':20000,
                    'style':'resize:none',
                    })
                }

class EditForm(forms.ModelForm):
    """Форма редактрирования сообщения"""

    class Meta:
        model = Messages
        fields = [ 'text']
        labels = {'text':'Redact message'}
        widgets = {
                'text': forms.Textarea(attrs={
                    'cols':120,
                    'maxlength':20000,
                    'style':'resize:none',
                    })
                }

class TopicAddForm(forms.ModelForm):
    """Форма добавления темы"""

    class Meta:
        model = Topic
        fields = ['name']  
        labels = {'name': 'Type new topic name:'}
        widgets = {'name': forms.Textarea(attrs={
            'style': 'resize:none',
            'cols': 120,
            'rows':1})}       

class NewDiscussionForm(forms.ModelForm):
    class Meta:
        model = Discuss
        fields = ['head']
        labels = {'head': 'Enter a discussion name'}
        widgets = {'head': forms.Textarea(attrs={
            'style': 'resize:none',
            'cols': 120,
            'rows':1,})}
