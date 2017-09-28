from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.template import Context, Template
from social.apps.django_app.default.models import UserSocialAuth

import requests

def get_patient(access_token, id):
    response = requests.get('https://drchrono.com/api/patients/{}'.format(id), headers={
        'Authorization': 'Bearer %s' % access_token,
    })
    response.raise_for_status()
    return response.json()



def home(request):# Create your views here.
    access_token = UserSocialAuth.objects.get().extra_data['access_token']
    response = requests.get('https://drchrono.com/api/users/current', headers={
        'Authorization': 'Bearer %s' % access_token,
    })
    response.raise_for_status()
    doctor_id = response.json()['id']

    # timestamp = (datetime.now() - timedelta(hours=16)).isoformat()

    response = requests.get('https://drchrono.com/api/appointments?doctor={}&date=2017-09-28'.format(doctor_id), headers={
        'Authorization': 'Bearer %s' % access_token,
    })
    response.raise_for_status()
    patient_ids = {appointment['patient'] for appointment in response.json()['results']}

    pairs = []
    for id in patient_ids:
        patient = get_patient(access_token, id)
        pairs.append((id, patient['first_name'] + ' ' + patient['last_name']))
    data = pairs

    context = Context({"data": data})
    return render(request, 'redirect.html', context=context)


