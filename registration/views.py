import json
import logging
import requests

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RegistrationDetailsForm
from .models import RegistrationDetails
from .serializers import RegistrationDetailsSerializer

LOGGER = logging.getLogger(__name__)

# Create your views here.
def user_registration(request):
    url = 'http://developers.gictsystems.com/api/dummy/submit/'
    headers = {'Content-type': 'application/json','Accept': 'text/plain'}

    if request.method == "POST":
        full_names = request.POST.get("fullnames")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        
        data = {
            "fullnames": full_names,
            "email": email,
            "phone": phone,
            "address": address
        }
        
        response = requests.post(
            url, data=json.dumps(data)
        )
        registration_details = RegistrationDetails(fullnames=full_names, email=email, phone=phone, address=address)
        registration_details.save()
        try:
            response.raise_for_status()
            if response.status_code == 200:
                messages.success(request, "Details entered successfully!" )
                return redirect('/registration_report')
        except Exception as err:
            messages.error("An error {} occurred while posting the data".format(err))
            return redirect('/register')
    else:
        return render(request, "home.html")


def update_record(request, id):
    user_detail = get_object_or_404(RegistrationDetails, id=id)
    if request.method == "POST":
        form = RegistrationDetailsForm(request.POST, instance=user_detail)
        if form.is_valid():
            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database  
            user_details = form.save(commit=False)
            user_details.save()
            messages.success(request, "Details updated successfully!" )
            return redirect('/registration_report')
        else:
            messages.error("The data entered is invalid")
            return render(request, "home.html", {'form': details})
    else:
        form = RegistrationDetailsForm(instance=user_detail)
    return render(request, 'update_record.html', {'form': form})


def get_user_details(request):
    url = 'http://developers.gictsystems.com/api/dummy/items/'
    headers={'Authorization': 'Bearer ALDJAK23423JKSLAJAF23423J23SAD3'}
    response = requests.get(url, headers=headers).json()
    return render(request, 'user_details.html', {'response': response})
        

class RegistrationDetailsAPIView(APIView):
    def get(self, request):
        details = RegistrationDetails.objects.all()
        serializer = RegistrationDetailsSerializer(details, many=True)
        return Response({"details": serializer.data})
    
    def post(self, request):
        user_detail = request.data.get('detail')
        
        serializer_data = RegistrationDetailsSerializer(data=user_detail)
        if serializer_data.is_valid(raise_exception=True):
            user_detail_record = serializer_data.save()
            return Response(status=200, data=user_detail_record)
