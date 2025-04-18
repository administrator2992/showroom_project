from django import forms
from .models import Mobil, Service
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class MobilForm(forms.ModelForm):
    class Meta:
        model = Mobil
        fields = '__all__'
        widgets = {
            'tahun': forms.NumberInput(attrs={
                'min': 1900, 
                'max': 2100,
                'class': 'form-control',
                'placeholder': 'Contoh: 2016'
            }),
            'merk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Toyota'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Yaris'}),
            'harga_dasar': forms.TextInput(attrs={'class': 'form-control rupiah', 'inputmode': 'numeric', 'placeholder': 'Contoh: 80.000.000'}),
            'pinjaman_bank': forms.TextInput(attrs={
                'class': 'form-control rupiah',
                'placeholder': 'Contoh: 100.000.000',
                'inputmode': 'numeric'
            }),
            'suku_bunga': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: 5.5'
            }),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['tanggal_service', 'deskripsi', 'biaya']
        widgets = {
            'tanggal_service': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'biaya': forms.TextInput(attrs={'class': 'form-control rupiah', 'inputmode': 'numeric'}),
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
