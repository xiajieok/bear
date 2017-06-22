from django import forms

class TaskForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    task = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    status = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))