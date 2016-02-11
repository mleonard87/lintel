from django import forms
from supportdesk.models import Project, Shift

class ProjectModelForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'support_telephone', 'welcome_message', )
        model = Project

class SupportAgentForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    telephone = forms.CharField(max_length=100)

class ShiftModelForm(forms.ModelForm):
    class Meta:
        fields = ('user', 'day', 'start', 'end', )
        model = Shift
