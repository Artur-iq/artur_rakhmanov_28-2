from django import forms


class ProductCreateForm(forms.Form):
    title = forms.CharField(max_length=50, min_length=3)
    image = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea, min_length=3)
    rate = forms.IntegerField()
