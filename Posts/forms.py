#POsts
from django import forms
from .models import Post,Comment

class PostModelForm(forms.ModelForm):
    context=forms.CharField(widget=forms.Textarea(attrs={'rows':4}))
    class Meta:
        model=Post
        fields=('context','image',)

class CommentModelForm(forms.ModelForm):
    body=forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Add comment','rows':4}))
    class Meta:
        model=Comment
        fields=('body',)