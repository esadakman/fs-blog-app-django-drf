from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView 
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status 
from .serializers import RegisterSerializer, ProfileUpdateForm
from .models import Profile
from rest_framework.permissions import IsAuthenticated
# from django.shortcuts import get_object_or_404

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        if Token.objects.filter(user=user).exists():
            token = Token.objects.get(user=user)
            data['token'] = token.key
        else:
            data['error'] = 'User dont have token. Please login'
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class ProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all() 
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileUpdateForm 

    # def get_object(self):
    #        print(self, 1) 
    #        username= self.kwargs.get("username")
    #        print(username, 11111) 
    #        return get_object_or_404(User, username=username)


    # def get_queryset(self): 
    #     # print('requested data', self.kwargs['pk'])  
    #     return self.queryset.all() 