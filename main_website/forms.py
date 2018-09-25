from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

class UserCreationForm(UserCreationForm):
    """Form for user signup."""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    telephone_num = forms.CharField(
        max_length=15,
        validators=[RegexValidator('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}'
                                    '|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}'
                                    '|\d{3}[-\.\s]??\d{4})',
        message="Please enter valid phone number")],
        label='Telephone Number',
        required=True)

    address = forms.CharField(max_length=30, label='Street Address',
        required=True)
    city = forms.CharField(max_length=20, required=True)
    suburb = forms.CharField(max_length=30, required=True)
    postcode = forms.CharField(
        max_length=4,
        validators=[RegexValidator('\d{4}',
        message="Please enter valid Post Code")],
        required=True)
    state = forms.CharField(max_length=20, required=True)
    country = forms.CharField(max_length=30, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'telephone_num',
                  'address', 'city','suburb', 'state', 'postcode', 'country',
                  'password1', 'password2')


class UserChangeForm(UserChangeForm):
    """Form for changing user."""
    class Meta:
        model = User
        fields = ('email',)
