from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'type',
            'image_path',
            'short_description',
            'long_description',
            'category',
            'target_audience',
        ]
        labels = {
            'title': 'Titel',
            'type': 'Type bijdrage',
            'image_path': 'Afbeelding (optioneel)',
            'short_description': 'Korte omschrijving',
            'long_description': 'Uitgebreide omschrijving',
            'category': 'Categorie',
            'target_audience': 'Doelgroep',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'image_path': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'long_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'target_audience': forms.TextInput(attrs={'class': 'form-control'}),
        }