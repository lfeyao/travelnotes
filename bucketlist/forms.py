from django import forms
from bucketlist.models import Page, Category

class CategoryForm(forms.ModelForm):
    #name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    #slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    #category = forms.ModelChoiceField(queryset=Category.objects.all().order_by('name'), help_text="Category:")
    #title = forms.CharField(max_length=128, help_text="Bucket List Item:")
    #views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('date_added',)
        #or specify the fields to include (i.e. not include the category field)
        fields = ('category', 'name', 'country', 'notes')