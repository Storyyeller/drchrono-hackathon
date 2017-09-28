from django import forms

class Patient(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())

    first_name = forms.CharField(label='First name', required=False)
    middle_name = forms.CharField(label='Middle name', required=False)
    last_name = forms.CharField(label='Last name', required=False)



    date_of_birth = forms.DateField(required=False)
    address = forms.CharField(required=False)
    state = forms.CharField(required=False)
    zip_code = forms.CharField(required=False)

    city = forms.CharField(required=False)
    cell_phone = forms.CharField(required=False)
    home_phone = forms.CharField(required=False)
    email = forms.CharField(required=False)
    gender = forms.CharField()
    ethnicity = forms.CharField(required=False)
    race = forms.CharField(required=False)
    social_security_number = forms.CharField(required=False)


