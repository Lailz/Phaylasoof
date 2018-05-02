from django.shortcuts import render
from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	CreateAPIView,
	DestroyAPIView,
	RetrieveUpdateAPIView
	)
from .models import Question, Category, Upvote, Downvote
from .serializers import (
    QuestionListSerializer,
    QuestionDetailSerializer,
    CategoryListSerializer,
    CategoryDetailSerializer,
    UpvoteCreateSerializer,
    UpvoteListSerializer,
    DownvoteCreateSerializer,
    DownvoteListSerializer,
    RegisterUserSerializer,
    UserLoginSerializer
    )
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsAuthorOrStaff
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import requests
from django.urls import reverse
from django.http import JsonResponse
import json

class LoginAPIView(APIView):
	permission_classes = [AllowAny]
	serializer_class = UserLoginSerializer

	def post(self, request, format=None):
		my_data = request.data
		my_serializer = UserLoginSerializer(data=my_data)
		if my_serializer.is_valid(raise_exception=True):
			new_data = my_serializer.data
			return Response(new_data, status=HTTP_200_OK)
		return Response(my_serializer.errors, status=HTTP_400_BAD_REQUEST)



class UserRegisterView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegisterUserSerializer
	permission_classes = [AllowAny]


class QuestionListView(APIView):
    def get(self, request):
        question_list = Question.objects.all()
        questions = QuestionListSerializer(question_list, many=True).data
        return Response(questions)

class QuestionDetailView(RetrieveAPIView):
	queryset = Question.objects.all()
	serializer_class = QuestionDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'question_id'
	permission_classes = [AllowAny,]

class CategoryListView(APIView):
    def get(self, request):
        category_list = Category.objects.all()
        categories = CategoryListSerializer(category_list, many=True).data
        return Response(categories)

class CategoryDetailView(RetrieveAPIView):
	queryset = Category.objects.all()
	serializer_class = CategoryDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'category_id'
	permission_classes = [AllowAny,]

class UpvoteCreateView(CreateAPIView):
	queryset = Upvote.objects.all()
	serializer_class = UpvoteCreateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self,serializer):
		serializer.save(user=self.request.user)


class DownvoteCreateView(CreateAPIView):
	queryset = Downvote.objects.all()
	serializer_class = DownvoteCreateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self,serializer):
		serializer.save(user=self.request.user)
