from django.shortcuts import render
from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	CreateAPIView,
	DestroyAPIView,
	RetrieveUpdateAPIView
	)
from .models import Question, Category, Upvote, Downvote, Answer, FollowCategory, FollowUser
from .serializers import (
    CategoryListSerializer,
	QuestionListSerializer,
	AnswerListSerializer,
    UpvoteCreateSerializer,
    UpvoteListSerializer,
    DownvoteCreateSerializer,
    DownvoteListSerializer,
    RegisterUserSerializer,
    UserLoginSerializer,
	FollowCategoryCreateSerializer,
    FollowCategoryListSerializer,
	FollowUserCreateSerializer,
    FollowUserListSerializer,
    )
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import requests
from django.urls import reverse
from django.http import JsonResponse
import json

from rest_framework.filters import SearchFilter, OrderingFilter

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


class CategoryListView(APIView):
	permission_classes = [AllowAny,]

	def get(self, request):
		category_list = Category.objects.all()
		categories = CategoryListSerializer(category_list, many=True, context={'request':request}).data
		return Response(categories)


class QuestionListView(APIView):
	permission_classes = [AllowAny,]

	def get(self, request, category_id):
		question_list = Question.objects.filter(category__id=category_id)
		questions = QuestionListSerializer(question_list, many=True, context={'request':request}).data
		return Response(questions)

class AnswerListView(APIView):
	permission_classes = [AllowAny,]
	def get(self, request, question_id):
		answer_list = Answer.objects.filter(question__id=question_id)
		answers = AnswerListSerializer(answer_list, many=True).data
		return Response(answers)



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

class FollowCategoryCreateView(CreateAPIView):
	queryset = FollowCategory.objects.all()
	serializer_class = FollowCategoryCreateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self,serializer):
		serializer.save(user=self.request.user)

class FollowUserCreateView(CreateAPIView):
	queryset = FollowUser.objects.all()
	serializer_class = FollowUserCreateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self,serializer):
		serializer.save(user=self.request.user)
