from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, User, Institution


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


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Voornaam')
    last_name = forms.CharField(max_length=30, required=True, label='Achternaam')
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Geboortedatum')
    function = forms.CharField(max_length=255, required=False, label='Functie')
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Beschrijving')
    ai_knowledge_level = forms.IntegerField(min_value=1, max_value=10, required=False, label='AI kennisniveau (1-10)')
    institution = forms.ModelChoiceField(queryset=Institution.objects.all(), required=False, label='Instelling')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'function', 'description', 'ai_knowledge_level', 'institution', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control'})
        self.fields['function'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['ai_knowledge_level'].widget.attrs.update({'class': 'form-control'})
        self.fields['institution'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=True, label='Voornaam')
    last_name = forms.CharField(max_length=30, required=True, label='Achternaam')
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Geboortedatum')
    function = forms.CharField(max_length=255, required=False, label='Functie')
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Beschrijving')
    ai_knowledge_level = forms.IntegerField(min_value=1, max_value=10, required=False, label='AI kennisniveau (1-10)')
    institution = forms.ModelChoiceField(queryset=Institution.objects.all(), required=False, label='Instelling')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'function', 'description', 'ai_knowledge_level', 'institution')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control'})
        self.fields['function'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['ai_knowledge_level'].widget.attrs.update({'class': 'form-control'})
        self.fields['institution'].widget.attrs.update({'class': 'form-control'})