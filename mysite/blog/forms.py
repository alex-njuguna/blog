from django import forms


class EmailPostForm(forms.Form):
    # form to email a post
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, 
                               widget=forms.Textarea)