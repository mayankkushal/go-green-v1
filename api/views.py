from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import Http404, HttpResponse

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from bills.serializers import BillSerializer
from bills.models import Bill

import json

# Create your views here.

def get_user_token(request, username, password):
	user = authenticate(username=username, password=password)
	if user:
		token = Token.objects.get_or_create(user=user)
		data = {'token':token[0].key}
		return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		raise Http404

class ClientBillList(APIView):
	"""
	List all Bills of the client
	"""

	def get(self, request, format=None):
		customer = self.request.user.profile
		print(customer.phone_no)
		bills = Bill.objects.filter(customer_no=customer.phone_no.national_number)
		serializer = BillSerializer(bills, many=True)
		return Response(serializer.data)