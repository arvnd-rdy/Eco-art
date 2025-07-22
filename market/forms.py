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

# Additional forms to meet 5-member team requirements (10 forms total)

class ContactForm(forms.Form):
    """General contact form for customer inquiries"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email address'})
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your message'})
    )

class UserFeedbackForm(forms.Form):
    """User feedback form for website improvements"""
    FEEDBACK_TYPE_CHOICES = [
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
        ('improvement', 'Improvement Suggestion'),
        ('compliment', 'Compliment'),
        ('complaint', 'Complaint'),
        ('other', 'Other'),
    ]
    
    RATING_CHOICES = [
        (5, '5 - Excellent'),
        (4, '4 - Good'),
        (3, '3 - Average'),
        (2, '2 - Poor'),
        (1, '1 - Very Poor'),
    ]
    
    feedback_type = forms.ChoiceField(
        choices=FEEDBACK_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief subject line'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tell us your feedback in detail...'})
    )
    overall_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="How would you rate your overall experience with our platform?"
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email (optional for follow-up)'})
    )
    allow_contact = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Allow us to contact you about this feedback"
    )

class ShippingUpdateForm(forms.Form):
    """Form to update shipping address for existing orders"""
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Street address'})
    )
    shipping_city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    shipping_state = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State/Province'})
    )
    shipping_zip_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP/Postal code'})
    )
    shipping_country = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'})
    )

class ArtistApplicationForm(forms.Form):
    """Form for artists to apply for verification"""
    full_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'})
    )
    artist_statement = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tell us about your artistic journey and eco-friendly practices'})
    )
    portfolio_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link to your portfolio'})
    )
    years_of_experience = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of artistic experience'})
    )
    specialization = forms.ChoiceField(
        choices=Product.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    certifications = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List any relevant certifications or awards'})
    )

class NewsletterSubscriptionForm(forms.Form):
    """Newsletter subscription form"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )
    interests = forms.MultipleChoiceField(
        choices=Product.CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    frequency = forms.ChoiceField(
        choices=[
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly')
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    ) 