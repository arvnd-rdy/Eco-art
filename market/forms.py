from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Profile, Review, Order

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ProductUploadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'art_style', 'materials', 'dimensions', 'image', 'location', 'artist_statement', 'sustainability_rating']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Artwork title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your artwork...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price in USD'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'art_style': forms.Select(attrs={'class': 'form-select'}),
            'materials': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List the eco-friendly materials used (e.g., recycled paper, natural dyes, reclaimed wood)'}),
            'dimensions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 24" x 36" or 60cm x 90cm'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your city or region'}),
            'artist_statement': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell the story behind your artwork and its environmental message...'}),
            'sustainability_rating': forms.Select(attrs={'class': 'form-select'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f"{i} {'★' * i}") for i in range(1, 6)],
                attrs={'class': 'form-select'}
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control', 
                    'rows': 4, 
                    'placeholder': 'Share your thoughts about this artwork...'
                }
            ),
        }

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'shipping_address', 'shipping_city', 'shipping_state', 
            'shipping_zip_code', 'shipping_country', 'shipping_phone',
            'payment_method', 'notes'
        ]
        widgets = {
            'shipping_address': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Street address, apartment, suite, etc.'
            }),
            'shipping_city': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'City'
            }),
            'shipping_state': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'State/Province'
            }),
            'shipping_zip_code': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'ZIP/Postal code'
            }),
            'shipping_country': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Country'
            }),
            'shipping_phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Phone number'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Special instructions or notes (optional)'
            }),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'profile_picture', 'phone', 'social_link']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your city or region'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number (optional)'}),
            'social_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Social profile link (optional)'}),
        } 