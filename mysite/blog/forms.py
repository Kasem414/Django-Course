from django import forms
class EmailPostForm(forms.form):
    name = forms.CharFIeld(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)