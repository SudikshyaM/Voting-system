from django.shortcuts import render
from rest_framework import generics,permissions,mixins,status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import *
from .serializers import PostSerializer,VoteSerializer

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# Create your views here.

class PostList(generics.ListCreateAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer

    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self,serializer):
        serializer.save(poster=self.request.user)

class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer

    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def delete(self, request,*args,**kwargs):
        post=Post.objects.filter(pk=self.kwargs['pk'],poster=self.request.user)
        if post.exists():
            return self.destroy(request,*args,**kwargs)
        else:
            raise ValidationError('You are not allowed to delete this post')
        

class VoteCreate(generics.CreateAPIView):
    serializer_class=VoteSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        post=Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user,post=post)
    
    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted for this post')
        else:
            serializer.save(voter=self.request.user,post=Post.objects.get(pk=self.kwargs['pk']))

    def delete(self,request,*args,**kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You have never voted for this post')


@csrf_exempt
def signup(request):
    if request.method=="POST":
        try:
            data=JSONParser().parse(request)
            user=User.objects.create_user(username=data['username'],password=data['password'])
            user.save()

            token=Token.objects.create(user=user)
            return JsonResponse({'token':str(token)},status=status.HTTP_200_OK)
        except IntegrityError:
            return JsonResponse({'error':'Username is already taken,try another'},status=400)
        
@csrf_exempt
def login(request):
    if request.method=="POST":
        data=JSONParser().parse(request)
        user=authenticate(request,username=data['username'],password=data['password'])
        if user is None:
            return JsonResponse({'error','username and password didnot match'},status=400)
        else:
            try:
                token=Token.objects.get(user=user)
            except:
                token=Token.objects.create(user=user)
            return JsonResponse({'token':str(token)},status=200)
        



    