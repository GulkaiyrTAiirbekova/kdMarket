from django.shortcuts import render
from rest_framework import viewsets

from user_app.models import User, SMSVerification
from user_app.serializers import UserSerializer, SMSVerificationSerializer


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SMSVerificationView(viewsets.ModelViewSet):
    queryset = SMSVerification.objects.all()
    serializer_class = SMSVerificationSerializer











    # def create(self, request, *args, **kwargs):
    #     name = Product.objects.get(name=request.name)
    #     if len(name) > 20:
    #         return Response("error")
