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
    # url = 'http://developers.gictsystems.com/api/dummy/submit/'
    # headers = {'Content-type': 'application/json','Accept': 'text/plain'}

    if request.POST:
        
        details = RegistrationDetailsForm(request.POST)
        
        if details.is_valid():
            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database  
            user_details = details.save(commit=False)
            user_details.save()
            messages.success(request, "Details entered successfully!" )
            return redirect('/register')
        else:
            messages.error("The data entered is invalid")
            return render(request, "home.html", {'form': details})
    
    else:
        form = RegistrationDetailsForm(None)
        return render(request, 'home.html')


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


class UserRegistrationReport(APIView):
    def get(self, request):
        user_details = RegistrationDetails.objects.all()
        context = {'user_details': user_details}
        return render(request, 'user_details.html', context)
    

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
