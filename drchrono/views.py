from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from social.apps.django_app.default.models import UserSocialAuth

import requests

from .forms import Patient
from .models import WaitingPatient

def get_access_token():
    return UserSocialAuth.objects.get().extra_data['access_token']

def get_patient(access_token, id):
    response = requests.get('https://drchrono.com/api/patients/{}'.format(id), headers={
        'Authorization': 'Bearer %s' % access_token,
    })
    response.raise_for_status()
    return response.json()



def checkin(request): 
    access_token = get_access_token()
    response = requests.get('https://drchrono.com/api/users/current', headers={
        'Authorization': 'Bearer %s' % access_token,
    })
    response.raise_for_status()
    doctor_id = response.json()['id']

    response = requests.get('https://drchrono.com/api/appointments?doctor={}&date=2017-09-28'.format(doctor_id), headers={
        'Authorization': 'Bearer %s' % access_token,
    })
    response.raise_for_status()
    patient_ids = {appointment['patient'] for appointment in response.json()['results']}

    pairs = []
    for id in patient_ids:
        patient = get_patient(access_token, id)
        pairs.append((id, patient['first_name'] + ' ' + patient['last_name']))

    return render(request, 'redirect.html', context={'data': pairs})

def editdata(request):
    access_token = get_access_token()
    id = request.GET.get('id')

    data = get_patient(access_token, id)
    form = Patient({k: data[k] for k in ['date_of_birth', 'gender', 'address', 'cell_phone', 'city', 'email', 'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation', 'ethnicity', 'first_name', 'home_phone', 'last_name', 'middle_name', 'race', 'social_security_number', 'state', 'zip_code', 'id']})

    return render(request, 'checkin.html', context={'form': form})

def submitdata(request):
    if request.method == 'POST':
        form = Patient(request.POST)
        if form.is_valid():
            data = form.cleaned_data.copy()
            id = data.pop('id')

            access_token = get_access_token()
            response = requests.patch('https://drchrono.com/api/patients/{}'.format(id), headers={
                'Authorization': 'Bearer %s' % access_token,
            }, data=data)
            response.raise_for_status()

            WaitingPatient.objects.update_or_create(id=id, defaults={
                'first_name': data.get('first_name', ''),
                'last_name': data.get('last_name', ''),
            })


            return render(request, 'success.html')
        return render(request, 'checkin.html', context={'form': form})
    else:
        return HttpResponseRedirect('/redirect')



