from django import forms
from .models import Contact, News, Comment

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'slug', 'body', 'image', 'category', 'status']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']