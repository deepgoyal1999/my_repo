from django import forms
from blog.models import comments
class sendmailform(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)

class commentform(forms.ModelForm):
    class Meta:
        model=comments
        fields=('name','email','body')
