from django import forms
from django.contrib.auth.models import User
from bucketlist.models import Page, Category, Place, UserProfile
from django.utils.translation import ugettext_lazy as _

class CategoryForm(forms.ModelForm):
    #name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    #slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    # category = forms.ModelChoiceField(queryset=Category.objects.all().order_by('name'))

    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'namefield'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'id': 'countryfield'}), required=False)
    notes = forms.CharField(widget=forms.Textarea(attrs={'id': 'notesfield'}), required=False)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        labels = {
            "category": _("Continent"),
        }

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('date_added',)
        #or specify the fields to include (i.e. not include the category field)
        fields = ('category', 'name', 'country', 'notes')

class PlaceForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'namefield'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'id': 'addressfield'}), required=False)
    notes = forms.CharField(widget=forms.Textarea(attrs={'id': 'notesfield'}), required=False)

    location = forms.ModelChoiceField(queryset=Page.objects.all().order_by('name'))

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Place

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ()
        #or specify the fields to include (i.e. not include the category field)
        fields = ('category', 'location', 'name', 'address', 'notes')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')