from django.forms import ModelForm
from django import forms
from django.db import transaction

from registration.models import RegistrationDetails

class RegistrationDetailsForm(ModelForm):
    fullnames = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    address = forms.CharField()
    
    class Meta:
        model = RegistrationDetails
        fields = "__all__"
        
    def clean(self):
        super(RegistrationDetailsForm, self).clean()
        
        fullnames = self.cleaned_data.get("fullnames")
        email = self.cleaned_data.get("email")
        phone = self.cleaned_data.get("phone")
        address = self.cleaned_data.get("address")
        
        # conditions to be met
        if len(fullnames) < 1:
            self._errors['fullnames'] = self.error_class([
                'Name entered is too short'])
        if '@' not in str(email):
            self._errors['email'] = self.error_class([
                'Email must include @'])
        
        return self.cleaned_data
    
    # @transaction.atomic
    # def save(self):
    #     details = super().save(commit=False)