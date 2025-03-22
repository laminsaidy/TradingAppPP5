from django import forms
from .models import ConversationMessage  

class ConversationMessageForm(forms.ModelForm):  
    """
    Form for creating or updating a conversation message.
    """
    class Meta:
        model = ConversationMessage  
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,  
                'placeholder': 'Type your message here...',  
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Add Bootstrap styling to the form.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})