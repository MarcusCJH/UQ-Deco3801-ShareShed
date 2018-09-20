from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

class UserCreationForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=False,
        help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False,
        help_text='Optional.')
    email = forms.EmailField(max_length=254,
        help_text='Required. Inform a valid email address.')
    telephone_num = forms.CharField(
        max_length=15,
        validators=[RegexValidator('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}'
                                    '|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}'
                                    '|\d{3}[-\.\s]??\d{4})',
        message="Please enter valid phone number")],
        label='Telephone Number')

    postcode = forms.CharField(
        max_length=4,
        validators=[RegexValidator('\d{4}',
        message="Please enter valid Post Code")])
    address = forms.CharField(max_length=30, label='Street Address')
    city = forms.CharField(max_length=20, required=True)
    county = forms.CharField(max_length=20)
    country = forms.CharField(max_length=30)
    suburb = forms.CharField(max_length=30)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'telephone_num',
                  'postcode', 'address', 'city', 'county', 'country', 'suburb',
                  'password1', 'password2')


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)
